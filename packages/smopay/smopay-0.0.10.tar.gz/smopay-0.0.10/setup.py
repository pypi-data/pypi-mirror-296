from setuptools import setup, find_packages


NAME = "smopay"
VERSION = "0.0.10"

REQUIRES = [
  "requests",
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,    
    description="Package for payment gateways SMO uses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omi-paulalmerino/smo-pay",
    author="Paul Almerino",
    author_email="paul.almerino@smsupermalls.com",
    license="BSD 2-clause",
    packages=find_packages(),
    install_requires=REQUIRES,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",  
        "Operating System :: POSIX :: Linux",    
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)