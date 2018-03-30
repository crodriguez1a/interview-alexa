#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import shutil
import sys
from os.path import dirname, join

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('interview_alexa')


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep twine"):
        print("twine not installed.\nUse `pip install twine`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('interview-alexa.egg-info')
    sys.exit()


setup(
    name='interview-alexa',
    version=version,
    url='https://github.com/crodriguez1a/interview-alexa',
    license='BSD',
    description='A Python Testing Framework for Alexa Skills using ASK CLI',
    author='Carlos Rodriguez',
    author_email='crodriguez1a@gmail.com',  # SEE NOTE BELOW (*)
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
