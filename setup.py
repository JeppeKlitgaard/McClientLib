try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from McClient import VERSION


setup(
    name="McClient",
    version=".".join(VERSION),
    description="A library for interfacing with a MineCraft server.",
    author="Jeppe Klitgaard",
    author_email="jeppe@dapj.dk",
    url="https://github.com/dkkline/McClientLib",
    packages=["McClient",
              "McClient.networking"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :" +
            ": GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: System :: Networking"
    ]
)
