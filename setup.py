#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path
import pyblue

setup(name='pyblue',
      version=pyblue.VERSION,
      description='PyBlue',
      author='Istvan Albert',
      author_email='istvan.albert@gmail.com',
      url='https://github.com/ialbert/pyblue',
      packages = ['pyblue', 'pyblue.bio'],
      scripts = ["pyblue/pyblue"],
      include_package_data = True,
      test_suite="tests",
      data_files=[
          ('pyblue/templates/', [
              'pyblue/templates/extensions.mako',
              'pyblue/templates/base.boot.mako',
              'pyblue/templates/base.md.mako',
          ]),
        ],
      long_description=file("README.rst").read(),
      keywords="",
      license="MIT",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.6',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          ],
      install_requires=[
        "bottle >= 0.11.6",
        "mako >= 0.8.0",
        "argparse",
        "markdown",
        "waitress",
        "docutils",
        ],
     )

