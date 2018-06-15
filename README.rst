django-oaipmh
======

.. sphinx-start-marker-do-not-remove

.. image:: https://travis-ci.org/Princeton-CDH/django-oaipmh.svg?branch=master
   :target: https://travis-ci.org/Princeton-CDH/django-oaipmh
   :alt: Build Status
.. image:: https://readthedocs.org/projects/django-oaipmh/badge/?version=latest
   :target: https://django-oaipmh.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://codecov.io/gh/Princeton-CDH/django-oaipmh/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Princeton-CDH/django-oaipmh
   :alt: Code Coverage
.. image:: https://requires.io/github/Princeton-CDH/django-oaipmh/requirements.svg?branch=master
   :target: https://requires.io/github/Princeton-CDH/django-oaipmh/requirements/?branch=master
   :alt: Requirements Status
.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
   :target: https://saythanks.io/to/cdhdevteam


**django-oaipmh** is intended to be a reusable `Django`_ application for
providing content to be harvested via the `Open Archives Initiative Protocol for
Metadata Harvesting`_ (OAI-PMH) version 2.0.

.. _Django: https://www.djangoproject.com/
.. _Open Archives Initiative Protocol for Metadata Harvesting: https://www.openarchives.org/pmh/

Installation
------------

Use pip to install::

    pip install django_oaipmh


You can also install from GitHub.  Use a branch or tag name, e.g.
``@develop`` or ``@1.0``, to install a specific tagged release or branch::

    pip install git+https://github.com/Princeton-CDH/django-oaipmh.git@develop#egg=django-oaipmh


Configuration
-------------

Add `django-oaipmh` to installed applications::

    INSTALLED_APPS = (
        ...
        'django_oaipmh',
        ...
    )

Extend OAIProvider and customize, similar to the way you would 
``django.contrib.sitemaps.Sitemap``::

  class MyOAIProvider(OAIProvider):
    def identify(self):
        ...

Bind your customized OAI provider to your desired url, e.g.::

    urlpatterns = [
        ...
        url(r'^oai/', MyOAIProvider.as_view()),
        ...
    ]

Development instructions
------------------------

This git repository uses `git flow`_ branching conventions. Where possible,
OAIprovider should be modeled on django.contrib.sitemap for easy extensibility 
and familiarity to Django developers.

.. _git flow: https://github.com/nvie/gitflow

Initial setup and installation:

- recommended: create and activate a python 3.5 virtualenv::

    python3 -m venv venv
    source venv/bin/activate

- pip install the package with its python dependencies::

    pip install -e .


Testing
^^^^^^^^^^^^

Unit tests are written with `py.test <http://doc.pytest.org/>`_ but use some
Django test classes for convenience and compatibility with django test suites.
Running the tests requires a minimal settings file for Django required
configurations.

- Copy sample test settings and add a **SECRET_KEY**::

    cp ci/testsettings.py testsettings.py

- To run the tests::

    python -m pytest

OAI provider implementations can be tested using the `OAI Repository Explorer 
<http://re.cs.uct.ac.za/>`_.