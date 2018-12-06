#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import requests
from logging import getLogger, DEBUG, FileHandler, Formatter

class SlackNotifier:
    CO2_PPM_THRESHOLD_1 = 1000
    CO2_PPM_THRESHOLD_2 = 2000

    CO2_STATUS_LOW          = 'LOW'
    CO2_STATUS_HIGH         = 'HIGH'
    CO2_STATUS_TOO_HIGH     = 'TOO HIGH'

    CO2_LOW_MESSAGE = u'''
室内の二酸化炭素濃度は{0:,}ppmに落ち着きました。
換気してくれた方ありがとう。
'''
    CO2_HIGH_MESSAGE = u'''
室内の二酸化炭素濃度は{0:,}ppmで、{1:,}ppmを超えています。
眠気・倦怠感・頭痛・耳鳴り・息苦しさ等の原因となります。
換気しましょう！
'''
    CO2_TOO_HIGH_MESSAGE = u'''
室内の二酸化炭素濃度は{0:,}ppmで、{1:,}ppmを超えています。
換気！換気！さっさと換気！
'''

    SLACK_USERNAME = u'二酸化炭素濃度測るくん'
    SLACK_WEBHOOK_URL    = 'https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX'
    SLACK_CHANNEL_NOTIFY = '#channel'

    LOG_FILE = '{script_dir}/logs/slack.log'.format(
        script_dir = os.path.dirname(os.path.abspath(__file__))
    )

    def __init__(self):
        self.init_logger()
        self.co2_status = self.CO2_STATUS_LOW

    def init_logger(self):
        self._logger = getLogger(self.__class__.__name__)
        file_handler = FileHandler(self.LOG_FILE)
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)
        self._logger.setLevel(DEBUG)

    def convert_co2_status(self, co2):
        if co2 < self.CO2_PPM_THRESHOLD_1:
            return self.CO2_STATUS_LOW
        elif co2 < self.CO2_PPM_THRESHOLD_2:
            return self.CO2_STATUS_HIGH
        else:
            return self.CO2_STATUS_TOO_HIGH

    def notify(self, co2, tvoc):
        co2_status = self.convert_co2_status(co2)
        if co2_status != self.co2_status:
            self.notify_to_slack(co2, co2_status)
            self.co2_status = co2_status

    def notify_to_slack(self, co2, co2_status):
        channel = self.SLACK_CHANNEL_NOTIFY
        title = u'二酸化炭素濃度botからのお知らせ'

        if co2_status == self.CO2_STATUS_LOW:
            color = 'good'
            fallback = self.CO2_LOW_MESSAGE.format(co2, self.CO2_PPM_THRESHOLD_1)
        elif co2_status == self.CO2_STATUS_HIGH:
            color = 'warning'
            fallback = self.CO2_HIGH_MESSAGE.format(co2, self.CO2_PPM_THRESHOLD_1)
        elif co2_status == self.CO2_STATUS_TOO_HIGH:
            color = 'danger'
            fallback = self.CO2_TOO_HIGH_MESSAGE.format(co2, self.CO2_PPM_THRESHOLD_2)
        else:
            return

        text = fallback

        res = self.call_slack_api(
            fallback, title, text, self.SLACK_USERNAME, channel, color
        )
        self._logger.debug(
            'Notified to Slack. STATUS_CODE - {status_code}, MSG - {msg}'.format(
                status_code = res['status_code'], msg = res['text']
            )
        )


    def call_slack_api(self, fallback, title, text, username, channel, color):
        headers = {
            'Content-Type': 'application/json'
        }

        payload = {
            'username': username,
            'channel': channel,
            'attachments': [
                {
                    'fallback': fallback,
                    'title': title,
                    'text': text,
                    'color': color
                }
            ]
        }

        response = requests.post(self.SLACK_WEBHOOK_URL, json = payload, headers = headers)

        return {
            'status_code': response.status_code,
            'text': response.text
        }
