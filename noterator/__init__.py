# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

from noterator import config
from noterator.plugins import email, hipchat, twilio
from noterator.utils import catch_all, now

__author__ = 'James Rutherford'
__email__ = 'jim@jimr.org'
__version__ = '0.1.0'


QUIET = 0
EMAIL = 1
TWILIO = 1 << 1
HIPCHAT = 1 << 2


class noterate(object):
    """Adding notification to iteration.

    Wrap any iterable with `noterate` and you'll be notified when the iteration
    completes, for example::

        >>> from noterator import noterate, EMAIL
        >>> for obj in noterate(my_objects, "My super-slow iteration", EMAIL):
        ...     do_something_slow(obj)
        ... 
        >>> 

    By default you only find out when the iteration completes, but sometimes
    it's useful to know when these things start too::

        >>> from noterator import noterate, EMAIL, HIPCHAT
        >>> for obj in noterate(my_objects, method=EMAIL|HIPCHAT, start=True):
        ...     do_something_slow(obj)
        ... 
        >>> 

    For any of this to work, you'll need to define some things in
    ``$HOME/.config/noterator/config.ini`` (or some other file, as defined by
    the ``config_file`` parameter.

    You can customise the messages by setting `desc`, `head`, and `body`
    accordingly.

    Args:
        iterable (iterable): The iterable we're going to wrap

    Kwargs:
        desc (str): Description to include in the notification.
        start (bool): Send a notification when iteration starts
        finish (bool): Send a notification when iteration completes
        method (int): Method(s) to use (e.g. ``EMAIL|HIPCHAT``)
        head (string): Header for notification message
        body (string): Body for notification message. We call `.format` on this
                       string with the iteration count at the point of
                       notification.
        config_file (string): Path to alternative configuration file.

    """
    def __init__(self, iterable, desc=None, method=QUIET, head=None, body=None,
                 start=False, finish=True, config_file=None):
        self.iterable = iterable
        self.start = start
        self.finish = finish
        self.method = method
        self.index = 0
        self.head = head or 'Noterator alert'
        self.body = body or 'progress: {} iterations.'
        self.desc = desc or 'Iteration'

        self.cfg = config.load(config_file)

        if method & EMAIL:
            assert 'email' in self.cfg.sections(), 'email config missing'

        if method & HIPCHAT:
            assert 'hipchat' in self.cfg.sections(), 'hipchat config missing'

    def __iter__(self):
        self._notify(started=True)

        for obj in self.iterable:
            yield obj
            self._notify()
            self.index += 1

        self._notify(finished=True)

    def next(self):
        if self.index == 0:
            self._notify(started=True)

        try:
            result = next(self.iterable)
            self.index += 1
            self._notify()
            return result
        except StopIteration:
            self._notify(finished=True)
            raise

    @catch_all
    def _notify(self, started=False, finished=False):
        send = False
        body = self.body.format(self.index)

        if self.start and started:
            send = True
            body = '{} started at {}'.format(self.desc, now())

        if self.finish and finished:
            send = True
            body = '{} finished at {} (total iterations: {}).'.format(
                self.desc, now(), self.index,
            )

        methods = (
            (EMAIL, 'email', email),
            (TWILIO, 'twilio', twilio),
            (HIPCHAT, 'hipchat', hipchat),
        )

        if send:
            for method, config_key, module in methods:
                if self.method & method:
                    module.notify(
                        self.head, body, **dict(self.cfg.items(config_key))
                    )
