# -*- coding: utf-8 -*-

import mock
import unittest

from noterator import Noterator, HIPCHAT


class TestEmailPlugin(unittest.TestCase):
    @mock.patch('noterator.plugins.hipchat.requests')
    def test_hipchat_settings(self, requests):
        cfg = {
            'token': 'hipchat-token',
            'room_id': '123456',
            'from_name': 'Testy McTesterson',
            'message_colour': 'neon pink',
        }

        n = Noterator(range(5), HIPCHAT, config_file=None)
        n.configure_plugin('hipchat', **cfg)
        for _ in n:
            pass

        url = 'https://api.hipchat.com/v2/room/{}/notification'.format(
            cfg['room_id'],
        )
        payload = {
            "message": "{}: {}".format(
                n.head, n._get_body(HIPCHAT, finished=True),
            ),
            "from": cfg['from_name'],
            "color": cfg['message_colour'],
        }
        headers = {
            'Authorization': 'Bearer {}'.format(cfg['token']),
        }

        requests.post.assert_called_once_with(url, payload, headers=headers)
