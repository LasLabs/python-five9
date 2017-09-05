# -*- coding: utf-8 -*-
# Copyright 2016-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from setuptools import Command, setup
from setuptools import find_packages
from unittest import TestLoader, TextTestRunner

from os import environ, path


PROJECT = 'five9'
SHORT_DESC = 'This library allows for you to integrate with Five9 Cloud ' \
             'Contact Center using Python.'
README_FILE = 'README.rst'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

version = environ.get('RELEASE') or environ.get('VERSION') or '0.0.0'

if environ.get('TRAVIS_BUILD_NUMBER'):
    version += 'b%s' % environ.get('TRAVIS_BUILD_NUMBER')


setup_vals = {
    'name': PROJECT,
    'author': 'LasLabs Inc.',
    'author_email': 'support@laslabs.com',
    'description': SHORT_DESC,
    'url': 'https://laslabs.github.io/python-%s' % PROJECT,
    'download_url': 'https://github.com/LasLabs/python-%s' % PROJECT,
    'license': 'MIT',
    'classifiers': CLASSIFIERS,
    'version': version,
}


if path.exists(README_FILE):
    with open(README_FILE) as fh:
        setup_vals['long_description'] = fh.read()


install_requires = []
if path.exists('requirements.txt'):
    with open('requirements.txt') as fh:
        install_requires = fh.read().splitlines()


class FailTestException(Exception):
    """ It provides a failing build """
    pass


class Tests(Command):
    """ Run test & coverage, save reports as XML """

    user_options = []  # < For Command API compatibility

    def initialize_options(self, ):
        pass

    def finalize_options(self, ):
        pass

    def run(self, ):
        loader = TestLoader()
        tests = loader.discover('.', 'test_*.py')
        t = TextTestRunner(verbosity=1)
        res = t.run(tests)
        if not res.wasSuccessful():
            raise FailTestException()


if __name__ == "__main__":
    setup(
        packages=find_packages(exclude=('tests')),
        cmdclass={'test': Tests},
        tests_require=[
            'mock',
        ],
        install_requires=install_requires,
        **setup_vals
    )
