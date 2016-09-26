# -*- coding: utf-8 -*-

from __future__ import absolute_import

import smtplib
from email.mime.text import MIMEText

REQUIRED_CONFIG = [
    'from_mail', 'recipient', 'host',
]


def notify(head, body, **kwargs):
    from_mail = kwargs['from_mail']
    recipient = kwargs['recipient']

    msg = MIMEText(body)
    msg['Subject'] = head
    msg['From'] = from_mail
    msg['To'] = recipient

    s = smtplib.SMTP(kwargs['host'], kwargs.get('port', 25))
    if kwargs['username'] and kwargs['password']:
        s.login(kwargs['username'], kwargs['password'])

    s.sendmail(from_mail, [recipient], msg.as_string())
    s.quit()
