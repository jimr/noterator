#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    # Skipping the first line reduces the heading level by 1
    history = ''.join(history_file.readlines()[1:])

with open('requirements/base.txt') as req_file:
    requirements = req_file.readlines()

with open('requirements/test.txt') as req_file:
    test_requirements = req_file.readlines()[1:]

setup(
    name='noterator',
    version='0.5.0',
    description="The Noterator: bringing notification to iteration.",
    long_description=readme + '\n\n' + history,
    author="James Rutherford",
    author_email='jim@jimr.org',
    url='https://github.com/jimr/noterator',
    packages=['noterator'],
    package_dir={'noterator': 'noterator'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='noterator',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
