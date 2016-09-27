# -*- coding: utf-8 -*-

import unittest

from .utils import all_available_methods, get_config_path

from noterator import Noterator
from noterator.config import ConfigurationError


class TestConfigValidation(unittest.TestCase):
    def test_valid_config(self):
        noterator = Noterator(
            method=all_available_methods(),
            config_file=get_config_path('config-full.ini')
        )
        noterator._validate_config()

    def test_invalid_config(self):
        noterator = Noterator(
            method=all_available_methods(),
            config_file=get_config_path('config-bad.ini')
        )
        with self.assertRaises(ConfigurationError):
            noterator._validate_config()