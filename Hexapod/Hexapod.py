#!/usr/bin/env python3
# coding:utf-8

import time
import logging
from Hexapod.Ultrasonic import Ultrasonic
from Hexapod.Buzzer import Buzzer
from Hexapod.ADS7830 import ADS7830
from Hexapod.MPU6050 import MPU6050
from Hexapod.Leds import Led
from Hexapod.Servo import Servo


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
        self.servo = Servo()
        self.test()
        self.dummy = 6.4
        self.dummy_pct = 100

    def test(self):
        self.servo.set_position('dead')
        time.sleep(1)
        self.servo.set_position('ready')

    def get_sensors(self):
        if self.dummy >= 8.4:
            self.dummy = 6.4
        self.dummy += 0.05
        if self.dummy_pct <= 0:
            self.dummy_pct = 100
        self.dummy_pct -= 1
        return {'b1_volt': self.adc.current_b1_volt,
                'b2_volt': self.adc.current_b2_volt,
                'b1_pct': self.adc.current_b1_pct,
                'b2_pct': self.adc.current_b2_pct,
                'ultrasonic': self.ultrasonic.current_distance,
                'pitch': self.mpu.current_pitch,
                'roll': self.mpu.current_roll,
                'yaw': self.mpu.current_yaw,
                'servo': self.servo.servo_enabled,
                'dummy': self.dummy,
                'dummy_pct': self.dummy_pct
                }
