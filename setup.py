# Copyright (c) 2014 Per Unneberg
# Modelled on bokeh setup script
# --------------------------------------------------
# Imports
# --------------------------------------------------

from __future__ import print_function

# stdlib
import os
from setuptools import setup
from os.path import realpath, dirname, relpath, join

# Extensions
import versioneer

# --------------------------------------------------
# globals and constants
# --------------------------------------------------

ROOT = dirname(realpath(__file__))

# --------------------------------------------------
# classes and functions
# --------------------------------------------------

package_data = []


def package_path(path, filters=()):
    if not os.path.exists(path):
        raise RuntimeError("packaging non-existent path: %s" % path)
    elif os.path.isfile(path):
        package_data.append(relpath(path, 'snakemakelib_rules'))
    else:
        for path, dirs, files in os.walk(path):
            path = relpath(path, 'snakemakelib_rules')
            for f in files:
                if not filters or f.endswith(filters):
                    package_data.append(join(path, f))

rule_suffixes = ('.rules', '.rule')
                    
package_path(join(ROOT, 'snakemakelib_rules', 'rules'), rule_suffixes)
scripts = []

REQUIRES = [
    'biopython>=1.64',
    'pyyaml>=3.11',
    'snakemake>=3.4.2',
    'sphinx>=1.3',
    'pandas>=0.16.0',
    'mock>=1.0.1',
    'pysam>=0.8.3',
    'pytest',
    'pytest-cov>=1.8.1',
]

try:
    # Hack for readthedocs
    if not 'readthedocs' in os.path.dirname(os.path.realpath(__file__)):
        pass
    else:
        print("readthedocs in path name; assuming we're building docs @readthedocs")
        REQUIRES.append('sphinx-bootstrap-theme')
except:
    pass

# Integrating pytest with setuptools: see
# https://pytest.org/latest/goodpractises.html#integrating-with-distutils-python-setup-py-test
from distutils.core import setup, Command
# you can also import from setuptools

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        import sys
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

_version = versioneer.get_version()
_cmdclass = versioneer.get_cmdclass()
_cmdclass.update({'test': PyTest})
setup(
    name="snakemakelib-rules",
    version=_version,
    cmdclass=_cmdclass,
    author="Per Unneberg",
    author_email="per.unneberg@scilifelab.se",
    description="Snakemake rule library",
    license="MIT",
    url="http://github.com/percyfal/snakemakelib-rules",
    scripts=scripts,
    packages=[
        'snakemakelib_rules',
    ],
    # namespace_packages = [
    #     'snakemakelib',
    #     'snakemakelib.rules',
    # ],
    package_data={'snakemakelib_rules': package_data},
    #setup_requires=SETUP_REQUIRES,
    install_requires=REQUIRES,
    #dependency_links=DEPENDENCY_LINKS,
)
