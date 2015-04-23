#! /usr/bin/python
# -*- coding: utf-8 -*-
from setuptools import setup
import os.path, sys
import pyblue

setup(
      name='pyblue',
      version=pyblue.VERSION,
      description='PyBlue',
      author='Istvan Albert',
      author_email='istvan.albert@gmail.com',
      url='https://github.com/ialbert/pyblue',
      packages=['pyblue'],
      scripts=["pyblue/pyblue"],
      include_package_data=True,
      test_suite="tests",
      data_files=[
          ('pyblue/templates/', [
              'pyblue/templates/pyblue-base.html',
          ]),
      ],
      long_description=open("README.rst").read(),
      keywords="",
      license="MIT",

      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],

      install_requires=[
          "django >= 1.7, < 1.8",
          "bottle",
          "markdown2",
          "waitress",
          "pygments",
          "bleach",
          "requests",
      ],
)

