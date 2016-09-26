=====
Usage
=====

The simplest usage of The Noterator is inside a ``for`` loop.

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, EMAIL):
    ...     do_something_slow(obj)
    ...
    >>>

By default, it will notify you by your chosen methods when the iteration completes.
You can also provide a description of the iteration that will be included (handy if you're doing several).

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, EMAIL, "Slow loop 1"):
    ...     do_something_slow(obj)
    ...
    >>>

You can combine notification methods and get notified when iteration begins:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL, TWILIO
    >>> for obj in noterate(my_objects, EMAIL|TWILIO, start=True):
    ...     do_something_slow(obj)
    ...
    >>>

If you want to hear about progress before completion, you can use the ``every_n`` parameter:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, EMAIL, every_n=100):
    ...     do_something_slow(obj)
    ...
    >>>

Advanced
========

If the sequence you're iterating over is an iterator, you can also use ``noterate`` as one:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> it = noterate(iter([1,2,3]), EMAIL)
    >>> while True:
    ...     try:
    ...         result = it.next()
    ...     except StopIteration:
    ...         break
    ...
    >>>

The ``noterate`` function is just a wrapper around the ``noterator.Noterator`` class.
If you want to set up a reuesable ``Noterator``, you can also do that as follows:

.. code-block:: pycon

    >>> from noterator import Noterator, EMAIL
    >>> noterator = Noterator(method=EMAIL, every_n=100, start=True)
    >>> for obj in noterator(my_objects, desc="loop 1")
    ...     do_something_slow(obj)
    ...
    >>> for obj in noterator(my_other_objects, desc="loop 2")
    ...     do_something_else_slow(obj)
    ...
    >>>
