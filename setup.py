#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'bittrex_v2',
    version = '1.0.1',
    url = 'https://github.com/mondeja/bittrex_v2',
    download_url = 'https://github.com/mondeja/bittrex_v2/archive/master.zip',
    author = 'Álvaro Mondéjar Rubio <mondejar1994@gmail.com>',
    author_email = 'mondejar1994@gmail.com',
    license = 'BSD License',
    packages = ['bittrex_v2'],
    description = 'Python wrapper for Bittrex API V2, currently in beta.',
    long_description = open('README.md','r').read(),
    keywords = ['python', 'bittrex', 'exchange', 'cryptocurrency', 'API', 'wrapper', 'V2'],
    install_requires = ['requests']
)
