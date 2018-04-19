# ckanext-unhcr

[![Build Status](https://travis-ci.org/okfn/ckanext-unhcr.svg?branch=master)](https://travis-ci.org/okfn/ckanext-unhcr)
[![Coverage Status](https://coveralls.io/repos/github/okfn/ckanext-unhcr/badge.svg?branch=master)](https://coveralls.io/github/okfn/ckanext-unhcr?branch=master)

CKAN extension for the UNHCR RIDL project

## Requirements

This extension is being developed against CKAN 2.7.x

## Installation

To install ckanext-unhcr for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/okfn/ckanext-unhcr.git
    cd ckanext-unhcr
    python setup.py develop
    pip install -r requirements.txt

## Running the Tests

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.unhcr --cover-inclusive --cover-erase --cover-tests
