# -*- coding: utf-8 -*-

import mock
import unittest

from email.mime.text import MIMEText
from freezegun import freeze_time
from noterator import Noterator, EMAIL


class TestEmailPlugin(unittest.TestCase):
    @freeze_time("2016-10-01 09:20:00")
    @mock.patch('noterator.plugins.email.smtplib')
    def test_email_settings(self, smtplib):
        cfg = {
            'recipient': 'to@example.com',
            'from_mail': 'from@example.com',
            'host': 'smtp.example.com',
            'port': '250',  # not 25 because that's the default value
            'username': 'smtpuser',
            'password': 'smtppass',
        }

        smtp = mock.Mock()
        smtplib.SMTP = mock.Mock(return_value=smtp)

        n = Noterator(range(5), EMAIL, config_file=None)
        n.configure_plugin('email', **cfg)
        for _ in n:
            pass

        msg = MIMEText(n._get_body(EMAIL, finished=True))
        msg['Subject'] = n.head
        msg['From'] = cfg['from_mail']
        msg['To'] = cfg['recipient']

        smtplib.SMTP.assert_called_once_with(cfg['host'], cfg['port'])
        smtp.sendmail.assert_called_once_with(
            cfg['from_mail'], [cfg['recipient']], msg.as_string(),
        )
