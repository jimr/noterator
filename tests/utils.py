# -*- coding: utf-8 -*-

import os

from noterator import Noterator


def get_config_path(fname):
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'data',
        fname,
    )


def all_available_methods():
    # Take a list of, e.g [EMAIL, HIPCHAT, TWILIO] and turn it into
    # EMAIL|HIPCHAT|TWILIO
    available_methods = [method for (method, _, _) in Noterator.methods]
    method = available_methods.pop(0)
    while len(available_methods):
        method |= available_methods.pop(0)

    return method
