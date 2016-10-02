# -*- coding: utf-8 -*-

import mock
import sys
import unittest

from noterator import Noterator, DESKTOP


class TestDesktopPlugin(unittest.TestCase):
    """Not really testing anything here - needs work.

    All we're really testing is that the mocks don't raise exceptions.

    """
    def test_desktop_plugin_mac(self):
        objc = mock.Mock()
        sys.modules['objc'] = objc
        sys.platform = 'darwin'

        nc = mock.Mock()
        cls1, cls2 = mock.Mock(), mock.Mock()
        cls2.defaultUserNotificationCenter = mock.Mock(return_value=nc)
        objc.lookUpClass = mock.Mock(side_effect=[cls1, cls2])

        n = Noterator(range(5), DESKTOP, config_file=None)
        n.configure_plugin('desktop', sound='true')
        for _ in n:
            pass

        nc.scheduleNotification_.assert_called_once()

    def test_desktop_plugin_linux(self):
        gi = mock.Mock()
        repository = mock.Mock()
        sys.modules['gi'] = gi
        sys.modules['gi.repository'] = repository
        sys.platform = 'linux2'

        n = Noterator(range(5), DESKTOP, config_file=None)
        for _ in n:
            pass
