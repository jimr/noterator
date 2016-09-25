=====
Usage
=====

The simplest usage of The Noterator is inside a ``for`` loop.

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, method=EMAIL):
    ...     do_something_slow(obj)
    ...
    >>>

By default, it will notify you by your chosen methods when the iteration completes.
You can also provide a description of the iteration that will be included (handy if you're doing several).

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, "Slow loop 1", method=EMAIL):
    ...     do_something_slow(obj)
    ...
    >>>

You can combine notification methods and get notified when iteration begins:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL, TWILIO
    >>> for obj in noterate(my_objects, start=True, method=EMAIL|TWILIO):
    ...     do_something_slow(obj)
    ...
    >>>

If you want to hear about progress before completion, you can use the ``every_n`` parameter:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> for obj in noterate(my_objects, every_n=100, method=EMAIL):
    ...     do_something_slow(obj)
    ...
    >>>

If the sequence you're iterating over is an iterator, you can also use ``noterate`` as one:

.. code-block:: pycon

    >>> from noterator import noterate, EMAIL
    >>> it = noterate(iter([1,2,3]), method=EMAIL)
    >>> while True:
    ...     try:
    ...         result = it.next()
    ...     except StopIteration:
    ...         break
    ...
    >>>
