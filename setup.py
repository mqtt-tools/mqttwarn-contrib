# -*- coding: utf-8 -*-
# (c) 2014-2021 The mqttwarn developers
import os
import platform

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'requests>=2.22.0',
]

extras = {}

# Packages needed for running the tests.
extras["test"] = [
    'mqttwarn[test]',
]


setup(name='mqttwarn-contrib',
      version='0.2.0',
      description='mqttwarn-contrib - community contributions to mqttwarn',
      long_description=README,
      license="EPL 2.0",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
        "Topic :: Education",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Pre-processors",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Archiving",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: Text Processing",
        "Topic :: Utilities",
      ],
      author='Jan-Piet Mens, Ben Jones, Andreas Motl',
      author_email='andreas.motl@panodata.org',
      url='https://github.com/daq-tools/mqttwarn-contrib',
      keywords='mqttwarn contributions mqtt notification plugins data acquisition push transformation engine ' +
               'mosquitto ',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires=requires,
      extras_require=extras,
      tests_require=extras['test'],
)
