# -*- coding: utf-8 -*-

from __future__ import absolute_import

import smtplib
from email.mime.text import MIMEText

REQUIRED_CONFIG = [
    'from', 'to', 'host',
]


def notify(head, body, **kwargs):
    mail_from = kwargs['from']
    mail_to = kwargs['to']

    msg = MIMEText(body)
    msg['Subject'] = head
    msg['From'] = mail_from
    msg['To'] = mail_to

    s = smtplib.SMTP(kwargs['host'], kwargs.get('port', 25))
    if kwargs['username'] and kwargs['password']:
        s.login(kwargs['username'], kwargs['password'])

    s.sendmail(mail_from, [mail_to], msg.as_string())
    s.quit()
