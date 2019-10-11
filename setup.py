#!/usr/bin/env python
# coding: utf-8

import setuptools
# from setuptools import setup

setuptools.setup(
    name='heroku_code',
    author='Airscope',
    author_email='capstonedesign57@gmail.com',
    install_requires=[],
    # install_requires=['keras-contrib @ git+https://www.github.com/keras-team/keras-contrib.git',
    # 'en-coref-md @ https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_md-3.0.0/en_coref_md-3.0.0.tar.gz'],
    dependency_links=['git+https://www.github.com/keras-team/keras-contrib.git'],
    # 'https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_md-3.0.0/en_coref_md-3.0.0.tar.gz'],
    url='https://github.com/capstonedesign57/heroku-airscope'
)
