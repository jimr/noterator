# -*- coding: utf-8 -*-

import unittest

from noterator.utils import catch_all


class TestUtils(unittest.TestCase):
    def test_catch_all(self):
        @catch_all
        def exceptional_function():
            raise Exception("No-one should notice this")

        try:
            exceptional_function()
        except Exception:
            self.fail("Exception not caught")
