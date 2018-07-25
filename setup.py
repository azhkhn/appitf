#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='appitf',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    requires=['flask', 'backlight'],
    py_modules=['appitf'],
    scripts=['appitfd'],
    description='Digital Signage Application System Interface.')
