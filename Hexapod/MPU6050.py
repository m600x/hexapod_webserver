#!/usr/bin/env python3
# coding:utf-8

import time
import math
import logging
import threading
from mpu6050 import mpu6050

MPU6050_DEFAULT_ADDRESS = 0x68

POLLING_INTERVAL = 1


class MPU6050:
    def __init__(self):
        """Entry point of the MPU6050 class.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of MPU6050 class')
        self.Kp = 100
        self.Ki = 0.002
        self.halfT = 0.001
        self.q0 = 1
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.exInt = 0
        self.eyInt = 0
        self.ezInt = 0
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.sensor = mpu6050(address=MPU6050_DEFAULT_ADDRESS, bus=1)
        self.sensor.set_accel_range(mpu6050.ACCEL_RANGE_2G)
        self.sensor.set_gyro_range(mpu6050.GYRO_RANGE_250DEG)
        self.kalman_filter = KalmanFilter(0.001, 0.1)
        self.Error_value_accel_data, self.Error_value_gyro_data = self.average_filter(self.sensor)

        self.current_pitch = 0.0
        self.current_roll = 0.0
        self.current_yaw = 0.0
        self.mpu_poller = threading.Thread(target=self.poller_mpu)
        self.mpu_poller.start()

    def poller_mpu(self):
        """Threaded poller
        """
        while True:
            self.logger.debug("Polling MPU sensor")
            self.current_pitch, self.current_roll, self.current_yaw = self.get_mpu()
            time.sleep(POLLING_INTERVAL)

    @staticmethod
    def average_filter(sensor):
        """Compute the average filter to apply on MPU reading over 100 samples
        """
        sum_accel_x = 0
        sum_accel_y = 0
        sum_accel_z = 0
        sum_gyro_x = 0
        sum_gyro_y = 0
        sum_gyro_z = 0
        for i in range(100):
            accel_data = sensor.get_accel_data()
            gyro_data = sensor.get_gyro_data()
            sum_accel_x += accel_data['x']
            sum_accel_y += accel_data['y']
            sum_accel_z += accel_data['z']
            sum_gyro_x += gyro_data['x']
            sum_gyro_y += gyro_data['y']
            sum_gyro_z += gyro_data['z']
        accel_data = {'x': sum_accel_x / 100,
                      'y': sum_accel_y / 100,
                      'z': (sum_accel_z / 100) - 9.8}
        gyro_data = {'x': sum_gyro_x / 100,
                     'y': sum_gyro_y / 100,
                     'z': sum_gyro_z / 100}
        return accel_data, gyro_data

    def get_mpu(self):
        accel_data = self.sensor.get_accel_data()
        gyro_data = self.sensor.get_gyro_data()
        axe_x = self.kalman_filter.compute(accel_data['x'] - self.Error_value_accel_data['x'])
        axe_y = self.kalman_filter.compute(accel_data['y'] - self.Error_value_accel_data['y'])
        axe_z = self.kalman_filter.compute(accel_data['z'] - self.Error_value_accel_data['z'])
        gx = self.kalman_filter.compute(gyro_data['x'] - self.Error_value_gyro_data['x'])
        gy = self.kalman_filter.compute(gyro_data['y'] - self.Error_value_gyro_data['y'])
        gz = self.kalman_filter.compute(gyro_data['z'] - self.Error_value_gyro_data['z'])
        norm = math.sqrt(axe_x * axe_x + axe_y * axe_y + axe_z * axe_z)
        axe_x = axe_x / norm
        axe_y = axe_y / norm
        axe_z = axe_z / norm
        velocity_x = 2 * (self.q1 * self.q3 - self.q0 * self.q2)
        velocity_y = 2 * (self.q0 * self.q1 + self.q2 * self.q3)
        velocity_z = self.q0 * self.q0 - self.q1 * self.q1 - self.q2 * self.q2 + self.q3 * self.q3
        ex = (axe_y * velocity_z - axe_z * velocity_y)
        ey = (axe_z * velocity_x - axe_x * velocity_z)
        ez = (axe_x * velocity_y - axe_y * velocity_x)
        self.exInt += ex * self.Ki
        self.eyInt += ey * self.Ki
        self.ezInt += ez * self.Ki
        gx += self.Kp * ex + self.exInt
        gy += self.Kp * ey + self.eyInt
        gz += self.Kp * ez + self.ezInt
        self.q0 += (-self.q1 * gx - self.q2 * gy - self.q3 * gz) * self.halfT
        self.q1 += (self.q0 * gx + self.q2 * gz - self.q3 * gy) * self.halfT
        self.q2 += (self.q0 * gy - self.q1 * gz + self.q3 * gx) * self.halfT
        self.q3 += (self.q0 * gz + self.q1 * gy - self.q2 * gx) * self.halfT
        norm = math.sqrt(self.q0 * self.q0 + self.q1 * self.q1 + self.q2 * self.q2 + self.q3 * self.q3)
        self.q0 /= norm
        self.q1 /= norm
        self.q2 /= norm
        self.q3 /= norm
        pitch = math.asin(-2 * self.q1 * self.q3 + 2 * self.q0 * self.q2) * 57.3
        roll = math.atan2(2 * self.q2 * self.q3 + 2 * self.q0 * self.q1,
                          -2 * self.q1 * self.q1 - 2 * self.q2 * self.q2 + 1) * 57.3
        yaw = math.atan2(2 * (self.q1 * self.q2 + self.q0 * self.q3),
                         self.q0 * self.q0 + self.q1 * self.q1 - self.q2 * self.q2 - self.q3 * self.q3) * 57.3
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        return self.pitch, self.roll, self.yaw


class KalmanFilter:
    def __init__(self, q, r):
        self.Q = q
        self.R = r
        self.P_k_k1 = 1
        self.Kg = 0
        self.P_k1_k1 = 1
        self.x_k_k1 = 0
        self.x_k1_k1 = 0
        self.ADC_OLD_Value = 0
        self.Z_k = 0
        self.kalman_adc_old = 0

    def compute(self, adc_value):
        self.Z_k = adc_value
        if abs(self.kalman_adc_old - adc_value) >= 60:
            self.x_k1_k1 = adc_value * 0.400 + self.kalman_adc_old * 0.600
        else:
            self.x_k1_k1 = self.kalman_adc_old
        self.x_k_k1 = self.x_k1_k1
        self.P_k_k1 = self.P_k1_k1 + self.Q
        self.Kg = self.P_k_k1 / (self.P_k_k1 + self.R)
        kalman_adc = self.x_k_k1 + self.Kg * (self.Z_k - self.kalman_adc_old)
        self.P_k1_k1 = (1 - self.Kg) * self.P_k_k1
        self.P_k_k1 = self.P_k1_k1
        self.kalman_adc_old = kalman_adc
        return kalman_adc
