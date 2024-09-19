from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'A Tool to find an Easy Bounty - CRLFI'
LONG_DESCRIPTION = 'This is a tool used by several security researchers to find CRLFI.'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crlfinjection",
    version=VERSION,
    author="@JUTRM",
    author_email="<admin@jutrm.com>",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'crlfinjection = Crlfi.main:main',
        ],
    },
    install_requires=['argparse', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)