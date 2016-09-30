=============
Configuration
=============

Available notification methods
==============================

Currently, The Noterator supports email, HipChat, Twilio (SMS), and desktop notifications.

Desktop notifications are only supported on Mac & Linux. On Linux, the ``notify-send`` binary must be on your ``$PATH``.

Here is the full set of configuration options available for all notification methods:

.. literalinclude:: ../config.example.ini
    :language: ini

The only settings that have a default are:

* ``email.port``: ``25``
* ``hipchat.from_name``: ``The Noterator``
* ``hipchat.message_colour``: ``green``
* ``desktop.sound``: ``false``


Configuration in ``.ini`` files
===============================

By default, ``noterator`` will look in ``$HOME/.config/noterator/config.ini`` for configuration.
See config.example.ini_ to get started.

If you want to keep your configuration file somewhere else, you can pass the ``config_file`` parameter to ``noterator``:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, method=EMAIL, config_file='/path/to/config.ini'):
    ...     do_something_slow(obj)
    ...
    >>>

.. _config.example.ini: https://github.com/jimr/noterator/blob/master/config.example.ini

Configuration in code
=====================

If you set up a ``Noterator`` class, you can override your file-based configuration per iteration:

.. code-block:: pycon

    >>> from noterator import Noterator, EMAIL
    >>> noterator = Noterator(method=EMAIL, every_n=100, start=True)
    >>> noterator.configure_plugin('email', recipient='someone@example.org')
    >>> for obj in noterator(my_objects)
    ...     do_something_slow(obj)
    ... 
    >>> noterator.configure_plugin('email', recipient='someone_else@example.org')
    >>> for obj in noterator(my_other_objects)
    ...     do_something_slow(obj)
    ... 
    >>>

You can go a step further and avoid using files at all.
The following code would work even if no configuration file could be found:

.. code-block:: pycon

    >>> from noterator import Noterator, EMAIL
    >>> noterator = Noterator(my_objects, method=EMAIL, every_n=100, start=True)
    >>> noterator.configure_plugin('email', recipient='you@example.org', from_mail='postmaster@example.org', host='smtp.example.org')
    >>> for obj in noterator:
    ...     do_something_slow(obj)
    ... 
    >>>
