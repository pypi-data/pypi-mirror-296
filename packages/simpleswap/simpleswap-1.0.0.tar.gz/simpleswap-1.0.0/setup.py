from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "1.0.0"
DESCRIPTION = "A package to enable API calls to the simpleswap.io API"
LONG_DESCRIPTION = "A package to enable API calls to the simpleswap.io API"

# Setting up
setup(
    name="simpleswap",
    version=VERSION,
    author="drkhedr (Abdelrahman Khedr)",
    author_email="<dev@drkhedr.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "simpleswap", "api", "cryptocurrency", "exchange", "crypto api", "simpleswap api", "cryptocurrency exchange api"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
