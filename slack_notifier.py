#!/usr/bin/env python

import json
import requests

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def notify(self, fallback, title, text, username, channel, color):
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

        response = requests.post(self.webhook_url, json = payload, headers = headers)

        return {
            'status_code': response.status_code,
            'text': response.text
        }
