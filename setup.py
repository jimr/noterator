#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    # Skipping the first line reduces the heading level by 1
    history = ''.join(history_file.readlines()[1:])

with open('requirements.txt') as req_file:
    requirements = req_file.readlines()

test_requirements = [
    'mock==2.0.0',
]

setup(
    name='noterator',
    version='0.4.1',
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
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
