import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "binutils_gen",
    version = "1.0",
    author = "Chris 'fakedrake' Perivolaropoulos",
    author_email = "darksaga2006@gmail.com",
    description = ("Generate binutils."),
    license = "GPL",
    keywords = "",
    url = "http://packages.python.org/binutils_gen",
    packages=['binutils_gen', 'binutils_gen.test'],
    install_requires=['Pyrametros'],
    dependency_links=["https://github.com/fakedrake/Pyrametros/tarball/master"],
    tests_require=['nose'],
    long_description=read('README.org'),
    test_suite='binutils_gen.test',
    entry_points={'console_scripts':['libsymbol = binutils_gen:libsymbols.main', 'binutils_gen = binutils_gen:binutils.main'] },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    ],
)
