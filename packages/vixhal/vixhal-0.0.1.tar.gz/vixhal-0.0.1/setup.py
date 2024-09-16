from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A library for secure key-value pair storage and AES encryption.'
LONG_DESCRIPTION = 'A library for secure key-value pair storage and AES encryption.'

# Setting up
setup(
    name="vixhal",
    version=VERSION,
    author="Vishal Singh Baraiya",
    author_email="<thevishal010@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pycryptodome'],
    keywords=['python', 'vixhal', 'encrypt', 'decrypt', 'bytes', 'AES'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)