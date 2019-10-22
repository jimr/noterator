# -*- coding: utf-8 -*-

import mock
import unittest

from noterator import Noterator, TWILIO
from noterator.plugins.twilio import BASE_URL


class TestEmailPlugin(unittest.TestCase):
    @mock.patch('noterator.plugins.twilio.requests')
    def test_twilio_settings(self, requests):
        cfg = {
            'account_sid': '123456',
            'token': 'twilio-token',
            'from_number': '+987654',
            'to_number': '+13579',
        }

        n = Noterator(range(5), TWILIO, config_file=None)
        n.configure_plugin('twilio', **cfg)
        for _ in n:
            pass

        url = '{}/Accounts/{}/Messages.json'.format(
            BASE_URL, cfg['account_sid'],
        )
        payload = {
            "From": cfg['from_number'],
            "To": cfg['to_number'],
            "Body": "{}: {}".format(
                n.head, n._get_body(TWILIO, finished=True),
            ),
        }
        auth = (cfg['account_sid'], cfg['token'])

        requests.post.assert_called_once_with(url, payload, auth=auth)
