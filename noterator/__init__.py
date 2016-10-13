# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from noterator.config import load_config, ConfigParser, ConfigurationError
from noterator.plugins import desktop, email, hipchat, twilio
from noterator.utils import catch_all, now

__author__ = 'James Rutherford'
__email__ = 'jim@jimr.org'
__version__ = '0.4.1'


QUIET = 0
EMAIL = 1
TWILIO = 1 << 1
HIPCHAT = 1 << 2
DESKTOP = 1 << 3


class Noterator(object):
    """Base class for setting up & configuring your noteration.

    You only really need to interact with this class directly (rather than just
    using ``noterator.noterate``) is if you want to build a re-usable
    ``Noterator`` or you want to build one without using a configuration file.

    For example, you could define a ``Noterator`` for use on two iterables, and
    use a different description for each one::

        >>> from noterator import Noterator, EMAIL
        >>> noterator = Noterator(method=EMAIL, every_n=100, start=True)
        >>> for obj in noterator(my_objects, desc="loop 1")
        ...     do_something_slow(obj)
        ...
        >>> for obj in noterator(my_other_objects, desc="loop 2")
        ...     do_something_else_slow(obj)
        ...
        >>> 

    And if you want to build a Noterator without using a configuration file (or
    if you just want to override some configured options)::

        >>> from noterator import Noterator, EMAIL
        >>> noterator = Noterator(my_objects, method=EMAIL, every_n=100)
        >>> noterator.configure_plugin('email', recipient='you@example.org')
        >>> for obj in noterator
        ...     do_something_slow(obj)
        ... 
        >>> 

    If `iterable` isn't set on class initialisation, it must be set before
    looping, or as a parameter to the ``noterate`` method.

    When iteration begins, the configuration will be validated.

    Args:
        Technically none, but ``iterable``, ``method``, and ``desc`` are often
        passed as positional arguments, and such usage is encouraged for
        brevity.

    Kwargs:
        iterable (iterable): The iterable we're going to wrap
        desc (str): Description to include in the notification.
        start (bool): Send a notification when iteration starts
        finish (bool): Send a notification when iteration completes
        every_n (int): Send a notification every ``every_n`` iterations
        method (int): Method(s) to use (e.g. ``EMAIL|HIPCHAT``)
        head (string): Header for notification message
        body (string): Body for notification message. We call `.format` on this
                       string with the iteration count at the point of
                       notification.
        config_file (string): Path to alternative configuration file.

    """
    index = 0
    methods = (
        (DESKTOP, 'desktop', desktop),
        (EMAIL, 'email', email),
        (TWILIO, 'twilio', twilio),
        (HIPCHAT, 'hipchat', hipchat),
    )

    def __init__(self, iterable=None, method=QUIET, desc=None, head=None,
                 body=None, start=False, finish=True, every_n=None,
                 config_file=None):
        self.iterable = iterable
        self.method = method

        self.desc = desc or 'Iteration'
        self.head = head or 'Noterator alert'
        self.body = body or 'progress: {} iterations.'

        self.start = start
        self.finish = finish
        self.every_n = every_n

        # If the configuration file isn't present, build an empty configuration
        # that can be populated with `self.configure_plugin`.
        self.cfg = ConfigParser()
        try:
            self.cfg = load_config(config_file)
        except IOError:
            pass

    def __call__(self, iterable=None, method=None, desc=None, **kwargs):
        """Allow any parameter to be set at execution time.

        For example::

            >>> from noterator import Noterator, EMAIL
            >>> noterator = Noterator(my_objects, EMAIL, every_n=100)
            >>> for obj in noterator(desc="loop 1")
            ...     do_something_slow(obj)
            ... 

        """
        if iterable is not None:
            self.iterable = iterable

        if method is not None:
            self.method = method

        if desc is not None:
            self.desc = desc

        for key, value in kwargs.items():
            setattr(self, key, value)

        return self

    def __iter__(self):
        self._validate_config()
        self._notify(started=True)

        for obj in self.iterable:
            yield obj
            self._notify()
            self.index += 1

        self._notify(finished=True)

    def next(self):
        if self.index == 0:
            self._validate_config()
            self._notify(started=True)

        try:
            result = next(self.iterable)
            self.index += 1
            self._notify()
            return result
        except StopIteration:
            self._notify(finished=True)
            raise

    def configure_plugin(self, name, **kwargs):
        """Optionally set up plugins without using a configuration file.

        You can also use this to override defaults set in a configuration file.

        Args:
            name (str): the name of the plugin (e.g. 'email')

        Kwargs: any keyword arguments accepted by the named plugin.

        """
        if not self.cfg.has_section(name):
            self.cfg.add_section(name)

        for key, value in kwargs.items():
            self.cfg.set(name, key, value)

    def _validate_config(self):
        for flag, config_key, module in self.methods:
            if self.method & flag:
                # If we're using a given notification method, make sure it's
                # configured.
                if config_key not in self.cfg.sections():
                    if len(module.REQUIRED_CONFIG):
                        raise ConfigurationError(
                            '{} is not configured'.format(config_key),
                        )
                else:
                    # Make sure all required configuration parameters are set
                    configured = set(self.cfg.options(config_key))
                    required = set(module.REQUIRED_CONFIG)
                    if configured & required != required:
                        raise ConfigurationError(
                            '{} is missing required settings: {}'.format(
                                config_key, ', '.join(required - configured),
                            )
                        )

    @catch_all
    def _notify(self, started=False, finished=False):
        send = False

        if self.start and started:
            send = True

        if self.finish and finished:
            send = True
        elif self.every_n:
            # We don't send `every_n` notifications on iteration completion
            # where that would be a duplicate notification hence the `elif`
            # with `self.finish and finished`
            if self.index > 0 and self.index % self.every_n == 0:
                send = True

        if send:
            for method, config_key, module in self.methods:
                if self.method & method:
                    body = self._get_body(method, started, finished)
                    cfg = {}
                    if config_key in self.cfg.sections():
                        cfg = dict(self.cfg.items(config_key))
                    module.notify(self.head, body, **cfg)

    def _get_body(self, method, started=False, finished=False):
        body = self.body.format(self.index)

        if started:
            body = '{} started'.format(self.desc)

        if finished:
            body = '{} finished (total iterations: {})'.format(
                self.desc, self.index,
            )
        elif self.every_n and self.index > 0:
            body = '{} completed {} iterations'.format(
                self.desc, self.index,
            )

        # If it's a desktop notification you don't need a timestamp because
        # it's immediate. All other mechanisms may be delayed for some reason
        # so a timestamp is potentially useful.
        if not method & DESKTOP:
            body = '{} at {}'.format(body, now())

        return body


def noterate(iterable, *args, **kwargs):
    """Wrap any iterable with `noterate` and you'll be notified when the iteration
    completes, for example::

        >>> from noterator import noterate, EMAIL
        >>> for obj in noterate(my_objects, EMAIL, "My super-slow iteration"):
        ...     do_something_slow(obj)
        ... 
        >>> 

    By default you only find out when the iteration completes, but sometimes
    it's useful to know when these things start too::

        >>> from noterator import noterate, EMAIL, HIPCHAT
        >>> for obj in noterate(my_objects, EMAIL|HIPCHAT, start=True):
        ...     do_something_slow(obj)
        ... 
        >>> 

    This function is a convenience wrapper around the ``Noterator`` class. The
    code above is equivalent to::

        >>> from noterator import Noterator, EMAIL, HIPCHAT
        >>> noterator = Noterator(my_objects, EMAIL|HIPCHAT, start=True)
        >>> for obj in noterator:
        ...     do_something_slow(obj)
        ... 
        >>> 

    Positional and Keyword arguments are the same as for ``Noterator.__init__``
    except that ``iterable`` is required.

    """
    return Noterator(iterable, *args, **kwargs)
