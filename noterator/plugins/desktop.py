# -*- coding: utf-8 -*-

from noterator.utils import enum

Platforms = enum('UNKNOWN', 'MAC', 'WINDOWS', 'LINUX')

PLATFORM = Platforms.UNKNOWN
try:
    import objc
    PLATFORM = Platforms.MAC
except ImportError:
    pass

REQUIRED_CONFIG = []


def notify(head, body, **cfg):
    if PLATFORM == Platforms.MAC:
        NSUserNotification = objc.lookUpClass('NSUserNotification')
        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(head)
        notification.setInformativeText_(body)

        if cfg.get('sound', False) not in ['false', False]:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")

        nc = NSUserNotificationCenter.defaultUserNotificationCenter()
        nc.scheduleNotification_(notification)
