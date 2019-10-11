#!/usr/bin/env python
# coding: utf-8

# import setuptools
from setuptools import setup

setup(
    name='heroku_code',
    author='Airscope',
    author_email='capstonedesign57@gmail.com',
    install_requires=['keras_contrib'],
    url=['https://github.com/keras-team/keras-contrib/tarball/master#egg=keras_contrib',
    'https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_md-3.0.0/en_coref_md-3.0.0.tar.gz']
)
