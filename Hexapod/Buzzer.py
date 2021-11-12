#!/usr/bin/env python3
# coding:utf-8

import time
import logging
import RPi.GPIO as GPIO

BUZZER_PIN = 17


class Buzzer:
    def __init__(self):
        """Entry point of the buzzer class. Set GPIO pin in correct mode.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of buzzer class')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        self.status_buzzer = False

    def toggle(self):
        """Toggle buzzer status
        """
        if self.status_buzzer:
            self.status_buzzer = False
            GPIO.output(BUZZER_PIN, True)
        else:
            self.status_buzzer = True
            GPIO.output(BUZZER_PIN, False)

    @staticmethod
    def active_ms(time_ms):
        """Activate the buzzer for time_ms arguments as milliseconds.
        Cap the max value to 10.000ms
        """
        if int(time_ms) < 0:
            return
        if int(time_ms) > 10000:
            time_ms = 10000
        GPIO.output(BUZZER_PIN, True)
        time.sleep(int(time_ms) / 1000)
        GPIO.output(BUZZER_PIN, False)
