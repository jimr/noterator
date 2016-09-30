# -*- coding: utf-8 -*-

import subprocess
import sys

REQUIRED_CONFIG = []


def notify(head, body, **cfg):
    if sys.platform == 'darwin':
        import objc
        NSUserNotification = objc.lookUpClass('NSUserNotification')
        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

        notification = NSUserNotification.alloc().init()
        notification.setTitle_(head)
        notification.setInformativeText_(body)

        if cfg.get('sound', False) not in ['false', False]:
            notification.setSoundName_("NSUserNotificationDefaultSoundName")

        nc = NSUserNotificationCenter.defaultUserNotificationCenter()
        nc.scheduleNotification_(notification)
    elif sys.platform == 'linux2':
        subprocess.Popen(['notify-send', head, body])
