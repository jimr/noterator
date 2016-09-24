#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_noterator
----------------------------------

Tests for `noterator` module.
"""

from noterator import noterate


class TestNoterator(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_nothing(self):
        for x in noterate(range(5)):
            pass

    @classmethod
    def teardown_class(cls):
        pass
