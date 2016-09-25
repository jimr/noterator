# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

REQUIRED_CONFIG = [
    'token', 'room_id',
]


def notify(head, body, **kwargs):
    token = kwargs['token']
    room_id = kwargs['room_id']
    from_name = kwargs.get('from_name', 'The Noterator')
    message_colour = kwargs.get('message_colour', 'green')

    url = 'https://api.hipchat.com/v2/room/{}/notification'.format(room_id)
    payload = {
        "message": "{}: {}".format(head, body),
        "from": from_name,
        "color": message_colour,
    }
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }

    requests.post(url, payload, headers=headers)
