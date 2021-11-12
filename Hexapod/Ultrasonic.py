#!/usr/bin/env python3
# coding:utf-8

import time
import logging
import RPi.GPIO as GPIO

TRIGGER_PIN = 27
ECHO_PIN = 22
TIMEOUT_POLL = 10000


class Ultrasonic:
    def __init__(self):
        """Entry point of the ultrasonic class. Set GPIOs pin in correct mode.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of ultrasonic class')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)

    @staticmethod
    def send_trigger_pulse():
        """Trigger a reading to the ultrasonic sensor by pulsing a signal on the GPIO pin
        """
        GPIO.output(TRIGGER_PIN, True)
        time.sleep(0.00015)
        GPIO.output(TRIGGER_PIN, False)

    @staticmethod
    def wait_for_echo(value):
        """Wait for the ultrasonic sensor to get back a value from the echo pulse.
        """
        count = TIMEOUT_POLL
        while GPIO.input(ECHO_PIN) != value and count > 0:
            count = count - 1

    def get_distance(self):
        """Poll the ultrasonic sensor and return the middle reading
        :return: [integer] mean value of 3 reading from the sensor
        """
        distance_cm = [0, 0, 0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True)
            start = time.time()
            self.wait_for_echo(False)
            finish = time.time()
            pulse_len = finish - start
            distance_cm[i] = pulse_len / 0.000058
            self.logger.debug("Read value from the ultrasonic sensor: %d" % distance_cm[i])
        distance_cm = sorted(distance_cm)
        self.logger.debug("Return final value from the ultrasonic sensor: %d" % distance_cm[1])
        return int(distance_cm[1])
