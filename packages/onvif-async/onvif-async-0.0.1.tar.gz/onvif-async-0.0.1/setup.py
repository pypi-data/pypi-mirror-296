"""Package Setup."""
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, "onvif/version.txt")
version = open(version_path).read().strip()

requires = [
    "httpx~=0.27.2",
    "zeep[async]>=4.2.1,<5.0.0",
    "ciso8601>=2.1.3"
]

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Customer Service",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Telecommunications Industry",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Multimedia :: Sound/Audio",
    "Topic :: Utilities",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
]

setup(
    name="onvif-async",
    version=version,
    description="Async Python Client for ONVIF Camera",
    long_description=open("README.rst").read(),
    author="Zou Guang Yu",
    author_email="zoulee24@qq.com",
    maintainer="zoulee24",
    maintainer_email="zoulee24@qq.com",
    license="MIT",
    keywords=["ONVIF", "Camera", "IPC"],
    url="http://github.com/hunterjm/python-onvif-zeep-async",
    zip_safe=False,
    python_requires=">=3.9",
    packages=find_packages(exclude=["docs", "examples", "tests"]),
    install_requires=requires,
    package_data={
        "": ["*.txt", "*.rst"],
        "onvif": ["*.wsdl", "*.xsd", "*xml*", "envelope", "include", "addressing"],
        "onvif.wsdl": ["*.wsdl", "*.xsd", "*xml*", "envelope", "include", "addressing"],
    },
    entry_points={"console_scripts": ["onvif-cli = onvif.cli:main"]},
)
