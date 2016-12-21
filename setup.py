# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='django-rest-framework-helpers',
    version='0.0.1',
    description='Helper collections for django-rest-framework',
    author='Apkawa',
    author_email='apkawa@gmail.com',
    url='https://github.com/Apkawa/django-rest-framework-helpers',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.8,<1.11',
        'djangorestframework>=3,<=4',
        'django-filter',
    ],
    classifiers=[
        'Development Status :: Pre Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
