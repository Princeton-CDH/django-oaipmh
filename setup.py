import os
from setuptools import find_packages, setup
from django_oaipmh import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

TEST_REQUIREMENTS = ['pytest', 'pytest-django', 'pytest-cov']

setup(
    name="django_oaipmh",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='Apache License, Version 2.0',
    description='Django app for exposing content through OAI-PMH protocol',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/Princeton-CDH/django-oaipmh',
    install_requires=[
        'django',
        'inflection',
        'eulxml',
        'python-dateutil'
    ],
    tests_require=TEST_REQUIREMENTS,
    extras_require={
        'test': TEST_REQUIREMENTS,
        'docs': ['sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme']
    },
    author='CDH @ Princeton',
    author_email='digitalhumanities@princeton.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
