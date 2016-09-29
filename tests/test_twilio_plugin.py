# -*- coding: utf-8 -*-

import mock
import unittest

from noterator import Noterator, TWILIO


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

        url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(
            cfg['account_sid'],
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
