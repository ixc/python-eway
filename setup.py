"""
Based entirely on Django's own ``setup.py``.
"""
import os
import re
from distutils.command.install import INSTALL_SCHEMES
# from distutils.core import setup
from setuptools import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

def pep386(v):
    """
    Take a long version string in the format "A.B.C alpha D" and turn it
    into "A.B.CaD" to satisfy PEP386 for packaging version numbers.
    """
    regex = re.compile(r' (?:([ab])\w+) (\d+)$')
    if regex.search(v):
        base = regex.sub('', v)
        minor = ''.join(regex.search(v).groups())
        return base + minor
    return v

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
tagging_dir = os.path.join(root_dir, 'eway')
pieces = fullsplit(root_dir)
if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)

for dirpath, dirnames, filenames in os.walk(tagging_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

# Dynamically calculate the version based on tagging.VERSION
version = __import__('eway').__version__

setup(
    name = 'python-eway',
    version = pep386(version),
    description = 'eWay API client library',
    author = 'John D\'Agostino',
    author_email = 'john.dagostino@gmail.com',
    url = 'http://code.google.com/p/python-eway/',
    packages = packages,
    data_files = data_files,
    classifiers = ['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules'])
