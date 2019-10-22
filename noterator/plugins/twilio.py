# -*- coding: utf-8 -*-

from __future__ import absolute_import

import requests

REQUIRED_CONFIG = [
    'account_sid', 'token', 'from_number', 'to_number',
]
BASE_URL = 'https://api.twilio.com/2010-04-01'


def notify(head, body, **kwargs):
    account_sid = kwargs['account_sid']
    token = kwargs['token']
    from_number = kwargs['from_number']
    to_number = kwargs['to_number']

    url = '{}/Accounts/{}/Messages.json'.format(BASE_URL, account_sid)
    payload = {
        "From": from_number,
        "To": to_number,
        "Body": "{}: {}".format(head, body),
    }
    auth = (account_sid, token)

    requests.post(url, payload, auth=auth)
