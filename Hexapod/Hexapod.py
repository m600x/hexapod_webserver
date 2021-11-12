#!/usr/bin/env python3
# coding:utf-8

import logging
from Hexapod.Ultrasonic import Ultrasonic
from Hexapod.Buzzer import Buzzer
from Hexapod.ADS7830 import ADS7830
from Hexapod.MPU6050 import MPU6050
from Hexapod.Leds import Led


class Hexapod:
    def __init__(self):
        """Entry point of the Hexapod mother class. Ignite subclasses
        """
        logger = logging.getLogger('root')
        logger.info('Ignition of Hexapod class')
        self.ultrasonic = Ultrasonic()
        self.buzzer = Buzzer()
        self.adc = ADS7830()
        self.mpu = MPU6050()
        self.led = Led()

    def get_sensors(self):
        pitch, roll, yaw = self.mpu.get_mpu()
        return {'battery1': self.adc.get_battery_1_voltage(),
                'battery2': self.adc.get_battery_2_voltage(),
                'ultrasonic': self.ultrasonic.get_distance(),
                'pitch': pitch,
                'roll': roll,
                'yaw': yaw}
