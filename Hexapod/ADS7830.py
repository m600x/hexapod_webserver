#!/usr/bin/env python3
# coding:utf-8

import smbus
import logging

ADS7830_CMD = 0x84
ADS7830_DEFAULT_ADDRESS = 0x48


class ADS7830:
    def __init__(self):
        """Entry point of the ADS7830 class.
        """
        self.logger = logging.getLogger('root')
        self.logger.info('Ignition of ADS7830 class')
        self.bus = smbus.SMBus(1)
        self.battery1_flag = False
        self.battery2_flag = False
        self.battery1Voltage = [0] * 25
        self.battery2Voltage = [0] * 25

    def voltage(self, channel):
        battery_voltage = 0
        if channel == 0 or channel == 4:
            data = [0] * 25
            if self.battery1_flag is False or self.battery2_flag is False:
                for i in range(25):
                    for j in range(25):
                        data[j] = self.read_adc(channel)
                    if channel == 0:
                        self.battery1Voltage.pop(0)
                        self.battery1Voltage.append(max(data))
                        battery_voltage = (sum(self.battery1Voltage) / len(self.battery1Voltage)) / 255.0*5.0
                        self.battery1_flag = True
                    else:
                        self.battery2Voltage.pop(0)
                        self.battery2Voltage.append(max(data))
                        battery_voltage = (sum(self.battery2Voltage) / len(self.battery2Voltage)) / 255.0*5.0
                        self.battery2_flag = True
            else:
                for j in range(25):
                    data[j] = self.read_adc(channel)
                if channel == 0:
                    self.battery1Voltage.pop(0)
                    self.battery1Voltage.append(max(data))
                    battery_voltage = (sum(self.battery1Voltage) / len(self.battery1Voltage)) / 255.0 * 5.0
                else:
                    self.battery2Voltage.pop(0)
                    self.battery2Voltage.append(max(data))
                    battery_voltage = (sum(self.battery2Voltage) / len(self.battery2Voltage)) / 255.0 * 5.0
        else:
            data = [0] * 9
            for i in range(9):
                data[i] = self.read_adc(channel)
            data.sort()
            battery_voltage = data[4] / 255.0 * 5.0
        return battery_voltage

    def read_adc(self, channel):
        command_set = ADS7830_CMD | ((((channel << 2) | (channel >> 1)) & 0x07) << 4)
        self.bus.write_byte(ADS7830_DEFAULT_ADDRESS, command_set)
        data = self.bus.read_byte(ADS7830_DEFAULT_ADDRESS)
        return data

    def battery_power(self):
        battery1 = round(self.voltage(0) * 3, 2)
        battery2 = round(self.voltage(4) * 3, 2)
        return battery1, battery2

    def get_battery_1_voltage(self):
        return round(self.voltage(0) * 3, 2)

    def get_battery_2_voltage(self):
        return round(self.voltage(4) * 3, 2)
