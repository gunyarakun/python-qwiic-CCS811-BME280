#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from logging import basicConfig, getLogger, DEBUG, FileHandler, Formatter
from time import sleep

import slack_notifier
from CCS811 import CCS811

class AirConditionMonitor:
    CO2_LOWER_LIMIT  =  400
    CO2_HIGHER_LIMIT = 8192

    LOG_FILE = '{script_dir}/logs/air_condition_monitor.log'.format(
        script_dir = os.path.dirname(os.path.abspath(__file__))
    )

    def __init__(self):
        self._ccs811 = CCS811()
        self.slack_notifier = slack_notifier.SlackNotifier()
        self.init_logger()

    def init_logger(self):
        self._logger = getLogger(self.__class__.__name__)
        file_handler = FileHandler(self.LOG_FILE)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        self._logger.setLevel(DEBUG)

    def status(self, co2):
        if co2 < self.CO2_LOWER_LIMIT or co2 > self.CO2_HIGHER_LIMIT:
            return self.CO2_STATUS_CONDITIONING
        elif co2 < self.CO2_PPM_THRESHOLD_1:
            return self.CO2_STATUS_LOW
        elif co2 < self.CO2_PPM_THRESHOLD_2:
            return self.CO2_STATUS_HIGH
        else:
            return self.CO2_STATUS_TOO_HIGH

    def execute(self):
        while not self._ccs811.available():
            pass

        while True:
            if not self._ccs811.available():
                sleep(1)
                continue

            try:
                if not self._ccs811.readData():
                    co2 = self._ccs811.geteCO2()

                    if co2 < self.CO2_LOWER_LIMIT or co2 > self.CO2_HIGHER_LIMIT:
                        self._logger.debug("Under Conditioning...")
                        sleep(2)
                        continue

                    self.slack_notifier.update_co2(co2)

                    self._logger.info("CO2: {0}ppm, TVOC: {1}".format(co2, self._ccs811.getTVOC()))
                else:
                    self._logger.error('ERROR!')
            except:
                self._logger.error(sys.exc_info())

            sleep(2)

if __name__ == '__main__':
    air_condition_monitor = AirConditionMonitor()
    air_condition_monitor.execute()
