# -*- coding: utf-8 -*-

import mock
import unittest

from .utils import all_available_methods, get_config_path

from noterator import Noterator, noterate, EMAIL


class TestNoterator(unittest.TestCase):
    @mock.patch('noterator.plugins.email.notify')
    def test_function(self, notify):
        cfg = get_config_path('config-full.ini')
        for _ in noterate(range(3), EMAIL, config_file=cfg):
            pass
        
        notify.assert_called_once()

    @mock.patch('noterator.plugins.email.notify')
    def test_iterable(self, notify):
        cfg = get_config_path('config-full.ini')
        it = noterate(iter(range(3)), EMAIL, config_file=cfg)
        while True:
            try:
                it.next()
            except StopIteration:
                break
        
        notify.assert_called_once()

    @mock.patch('noterator.plugins.email.notify')
    def test_callable(self, notify):
        noterator = Noterator(
            config_file=get_config_path('config-full.ini')
        )
        for _ in noterator(range(3), EMAIL, 'abc'):
            pass

        notify.assert_called_once()

    @mock.patch('noterator.plugins.email.notify')
    def test_start(self, notify):
        noterator = Noterator(
            method=EMAIL,
            start=True,
            config_file=get_config_path('config-full.ini')
        )
        for _ in noterator(range(3)):
            pass

        self.assertEqual(len(notify.mock_calls), 2)

    @mock.patch('noterator.plugins.email.notify')
    def test_finish(self, notify):
        noterator = Noterator(
            method=EMAIL,
            start=True,
            finish=True,
            config_file=get_config_path('config-full.ini')
        )
        for _ in noterator(range(3)):
            pass

        self.assertEqual(len(notify.mock_calls), 2)

        for _ in noterator(range(3), start=False):
            pass

        self.assertEqual(len(notify.mock_calls), 3)

    @mock.patch('noterator.plugins.email.notify')
    def test_every_n(self, notify):
        noterator = Noterator(
            method=EMAIL,
            every_n=1,
            config_file=get_config_path('config-full.ini')
        )
        for _ in noterator(range(3)):
            pass

        self.assertEqual(len(notify.mock_calls), 3)
