#!/usr/bin/env python3
# coding:utf-8

import time
import logging
from rpi_ws281x import *

LED_COUNT = 7         # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHAN = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Led:
    def __init__(self):
        """Entry point of the Led class. Set GPIO pin in correct mode.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of leds class')
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHAN)
        self.strip.begin()

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if 0 < pos > 255:
            return 0
        red, green, blue = 0, 0, 0
        if pos < 85:
            red = pos * 3
            green = 255 - pos * 3
        elif pos < 170:
            pos -= 85
            red = 255 - pos * 3
            blue = pos * 3
        else:
            pos -= 170
            green = pos * 3
            blue = 255 - pos * 3
        return Color(Color(red, green, blue) >> 16 & 255,
                     Color(red, green, blue) >> 8 & 255,
                     Color(red, green, blue) & 255)
