=======
History
=======

0.4.1 (2016-10-13)
------------------

* Minor cleanups & fixes

0.4.0 (2016-09-30)
------------------

* Desktop notification (Mac & Linux)
* Improvements to testing
* Test coverage reporting to codecov.io

0.3.0 (2016-09-28)
------------------

* Allow the construction of re-usable Noterators with the ``Noterator`` class
* Configuration is now possible without a config file (``instance.configure_plugin``)
* Plugin validation is now triggred when iteration begins, not when the Noterator is built
* Changed email plugin configuration keys to be consistent with, e.g. Django
* Added tests for configuration file validation & all plugins
* Travis CI + coverage / Coveralls integration

0.2.2 (2016-09-26)
------------------

* Fixed a packaging error

0.2.1 (2016-09-25)
------------------

* More appropriate exception usage in config loading / checking

0.2.0 (2016-09-25)
------------------

* More safety checks in configuration
* Added the ``every_n`` parameter to ``noterate``

0.1.0 (2016-09-24)
------------------

* First release on PyPI.
