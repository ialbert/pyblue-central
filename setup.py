#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path

setup(name='pyblue',
      version='1.0.3',
      description='PyBlue',
      author='Nicolas Vanhoren, Istvan Albert',
      author_email='nicolas.vanhoren@unknown.com, istvan.albert@gmail.com',
      url='https://github.com/ialbert/pyblue',
      py_modules = ['pyblue'],
      packages=[],
      scripts=["pyblue"],
      long_description="A bioinformatics oriented micro web framework/static web site generator based on PyGreen.",
      keywords="",
      license="MIT",
      classifiers=[
          ],
      install_requires=[
        "bottle >= 0.11.6",
        "mako >= 0.8.0",
        "argparse",
        "markdown",
        "waitress",
        ],
     )

