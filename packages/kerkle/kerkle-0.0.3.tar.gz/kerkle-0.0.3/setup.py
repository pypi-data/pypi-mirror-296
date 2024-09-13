#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
$ python setup.py register sdist upload

First Time register project on pypi
https://pypi.org/manage/projects/


Pypi Release
$ pip3 install twine

$ python3 setup.py sdist
$ twine upload dist/kerkle-0.0.1.tar.gz

Create release git:
$ git tag # lists all tags
$ git tag -a v0.6.11 -m "new feature"
$ git show v0.6.11
$ git push --tags # pushes tags to default remote
$ git push wot --tags   # pushes tags to wot remote

$ git tag -a v0.4.2 -m "bump version"
$ git push --tags
$ git checkout -b release_0.4.2
$ git push --set-upstream origin release_0.4.2
$ git checkout master

Best practices for setup.py and requirements.txt
https://caremad.io/posts/2013/07/setup-vs-requirement/
"""

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages, setup

setup(
    name='kerkle',
    version='0.0.3',  # also change in src/keri/__init__.py
    license='Apache Software License 2.0',
    description='A KERI Event Sparse Merkle Tree',
    long_description="Kerkle",
    author='Phil Feairheller',
    author_email='phil@healthKERI.com',
    url='https://github.com/WebOfTrust/sparse-kerkle-tree',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: PyPy',
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://kerkle.readthedocs.io/',
        'Changelog': 'https://kerkle.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/WebOfTrust/sparse-kerkle-tree/issues',
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires='>=3.12.2',
    install_requires=[
        'keri>=1.2.0-rc1',
        'lmdb>=1.4.1',
        'pysodium>=0.7.17',
        'blake3>=0.4.1'
    ],
    extras_require={
    },
    tests_require=[
        'coverage>=7.4.4',
        'pytest>=8.1.1',
        'pytest-shell>=0.3.2'
    ],
    setup_requires=[
    ],
    entry_points={
    },
)
