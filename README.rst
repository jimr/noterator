=============
The Noterator
=============


.. image:: https://img.shields.io/pypi/v/noterator.svg
    :target: https://pypi.python.org/pypi/noterator
    :alt: Latest Release

.. image:: https://img.shields.io/travis/jimr/noterator.svg
    :target: https://travis-ci.org/jimr/noterator
    :alt: Build Status

.. image:: https://codecov.io/gh/jimr/noterator/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jimr/noterator
    :alt: Test Coverage

.. image:: https://readthedocs.org/projects/noterator/badge/?version=latest
    :target: https://noterator.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jimr/noterator/shield.svg
    :target: https://pyup.io/repos/github/jimr/noterator/
    :alt: Updates


Adding notification to your iteration.

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL, TWILIO
    >>> for obj in noterate(my_objects, EMAIL|HIPCHAT|TWILIO):
    ...     do_something_slow(obj)
    ... 
    >>> 

When the loop completes, The Noterator will notify you by all the methods you passed in.
In this case it'll email you and send an SMS to your configured number with Twilio.
Other supported notification methods are HipChat (send a notification to a room) and desktop.

You can find more usage information in the `usage docs`_.

.. _`usage docs`: http://noterator.readthedocs.io/en/latest/usage.html


Configuration
-------------

Before The Noterator can do anything, you'll need a ``config.ini`` file (see config.example.ini_ or the example below to get started).

It's possible to use The Noterator without a configuration file, but it's a little less concise.
See the `configuration docs`_ for more detail.

By default, we check for ``$HOME/.config/noterator/config.ini``, so it's probably best to keep your config there, but you can pass the ``config_file`` parameter to ``noterate`` with the path to an alternative location.

You only need to define settings for the methods you wish to use.

.. _config.example.ini: https://github.com/jimr/noterator/blob/master/config.example.ini
.. _`configuration docs`: http://noterator.readthedocs.io/en/latest/configuration.html

.. code-block:: ini

    [desktop]
    sound = true

    [email]
    from_mail = The Noterator <noterator@example.org>
    recipient = you@example.org
    host = smtp.example.org
    port = 25
    username = postmaster@example.org
    password = password123

    [hipchat]
    token = abc123
    room_id = 123456
    from_name = The Noterator
    message_colour = green

    [twilio]
    account_sid = abc123
    token = abc123
    from_number = +123456
    to_number = +456789

TODO
----

* New notification plugins: logging, ...
* Notication during iteration, a la `tqdm.write`_

.. _`tqdm.write`: https://github.com/tqdm/tqdm#writing-messages

License
-------

MIT.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
