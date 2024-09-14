import os, re
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("herdcalls/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

setup(
    name="herdcalls",
    version=version,
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/OnTheHerd/herdcalls",
    author="OnTheHerd",
    author_email="oth@pyroherd.org",
    license="LGPL-3.0",
    license_file="LICENSE",
    classifiers=[
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.3",
        "ntgcalls>=1.1.2",
        "psutil",
        "screeninfo",
        "deprecation",
        "setuptools",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    universal=True,
    zip_safe=False,
)