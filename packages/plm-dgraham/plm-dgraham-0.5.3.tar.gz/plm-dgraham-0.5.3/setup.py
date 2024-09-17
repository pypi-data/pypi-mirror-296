#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree
from plm.__version__ import version

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'plm-dgraham'
DESCRIPTION = 'player lineup manager'
URL = 'https://github.com/dagraham/plm-dgraham'
EMAIL = 'dnlgrhm@gmail.com'
AUTHOR = 'Daniel A Graham'
REQUIRES_PYTHON = '>=3.7.3'
VERSION = version

# What packages are required for this module to be executed?
REQUIRED = [
    'prompt-toolkit>=3.0.24',
    'ruamel.yaml>=0.15.88',
    'python-dateutil>=2.7.3',
    'requests>=2.25.1',
    'pyperclip>=1.7.0',
    'termcolor>=2.2.0',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace('-', '_').replace(' ', '_')
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
    CLASSIFIERS = [
        'Development Status :: 2 - Pre-Alpha',
    ]
else:
    about['__version__'] = VERSION
    if 'a' in VERSION:
        CLASSIFIERS = [
            'Development Status :: 3 - Alpha',
        ]
    elif 'b' in VERSION:
        CLASSIFIERS = [
            'Development Status :: 4 - Beta',
        ]
    else:
        CLASSIFIERS = [
            'Development Status :: 5 - Production/Stable',
        ]

    CLASSIFIERS.extend(
        [
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Office/Business',
            'Topic :: Office/Business :: News/Diary',
            'Topic :: Office/Business :: Scheduling',
        ]
    )


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError as e:
            print('error removing dist tree:', e)

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable)
        )

        self.status('Uploading the package to PyPI via Twine…')
        os.system(
            'twine upload --verbose --repository-url https://upload.pypi.org/legacy/ dist/*'
        )

        sys.exit()


# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # packages=['plm'],
    packages=find_packages(exclude=('tests', 'test', 'tmp')),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        'console_scripts': [
            'plm=plm.__main__:main',
        ],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPL',
    classifiers=CLASSIFIERS,
    cmdclass={
        'upload': UploadCommand,
    },
)
