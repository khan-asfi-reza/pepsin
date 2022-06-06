from pipcx import version
from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = version.get_version()

setup(
    name='pipcx',
    version=VERSION,
    include_package_data=True,
    description="Python PIP Toolchain cli",
    author="Khan Asfi Reza",
    author_email="khanasfireza10@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests*",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    entry_points='''
        [console_scripts]
        pipcx=pipcx.main:main
    ''',
    python_requires=">=3.6",
)
