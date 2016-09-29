# -*- coding: utf-8 -*-

import os

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:  # py3k
    from configparser import ConfigParser


class ConfigurationError(Exception):
    pass


def load_config(fname=None):
    """Load and return configuration from a file.

    Args:
        fname (str): Path to the ini file we should use. If not provided, we
            default to $HOME/.config/bocho/config.ini

    Returns:
        The parsed configuration

    Raises:
        ConfigurationError: if the file can't be found.

    """
    if not fname:
        fname = os.path.join(
            os.getenv('HOME', ''), '.config', 'noterator', 'config.ini'
        )

    if not os.path.exists(fname):
        raise IOError(
            "Unable to find configuration file."
        )

    config = ConfigParser()
    config.read(fname)

    return config
