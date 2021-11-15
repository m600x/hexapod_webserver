#!/usr/bin/env python3
# coding:utf-8

import time
import logging
from adafruit_servokit import ServoKit

"""
                 00
                _01_
LEG1  18 17 16 |    | 15 14 13  LEG6
LEG2  21 20 19 |    | 12 11 10  LEG5
LEG3  27 23 22 |____| 09 08 31  LEG4

"""

PCA9685_LEFT_ADDRESS = 0x40
PCA9685_RIGHT_ADDRESS = 0x41

LEFT_SHOULDER = [16, 19, 22]
LEFT_ELBOW = [17, 20, 23]
LEFT_TIP = [18, 21, 27]
RIGHT_SHOULDER = [9, 12, 15]
RIGHT_ELBOW = [8, 11, 14]
RIGHT_TIP = [31, 10, 13]
HEAD = [1, 0]

POSITION = {
    'ready': [90, 140, 120, 90],
    'install': [90, 90, 0, 90],
    'dead': [90, 180, 180, 90]
}


class Servo:
    def __init__(self):
        """Entry point of the Servo class.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of servo class')
        self.servo_left = ServoKit(channels=16, address=PCA9685_LEFT_ADDRESS)
        self.servo_right = ServoKit(channels=16, address=PCA9685_RIGHT_ADDRESS)
        self.servo_enabled = True

    def enable_servo(self):
        self.set_position('install')
        time.sleep(1)
        self.set_position('ready')
        self.servo_enabled = True

    def disable_servo(self):
        for servo in range(16):
            self.servo_left.servo[servo].angle = None
            self.servo_right.servo[servo].angle = None
        self.servo_enabled = False

    def set_position(self, pos):
        """Move servos to predefined position
        """
        if pos in POSITION:
            self.logger.info("Servos move to %s position" % pos)
            self.set_servo_group(LEFT_SHOULDER + RIGHT_SHOULDER, POSITION[pos][0])
            self.set_servo_group(LEFT_ELBOW + RIGHT_ELBOW, POSITION[pos][1])
            self.set_servo_group(LEFT_TIP + RIGHT_TIP, POSITION[pos][2])
            self.set_servo_group(HEAD, POSITION[pos][3])
        else:
            self.logger.error("Servos set_position received an unknown position: %s" % pos)

    def set_servo_group(self, sets, angle):
        """Move array of servos to a certain angle
        """
        for servo in sets:
            self.set_servo_angle(servo, angle)

    def set_servo_angle(self, channel, angle):
        """Set the servo angle to the desired position.
        Check the channel from 0 to 32 and direct to the correct controller.
        If the angle is set for the right side, the angle value is inverted.
        """
        if channel in range(16, 24) or channel == 27:
            angle = 180 - angle
        self.logger.debug("Move servo %d to angle %d", channel, angle)
        if channel < 16:
            self.servo_right.servo[channel].angle = angle
        elif 16 <= channel < 32:
            channel -= 16
            self.servo_left.servo[channel].angle = angle
