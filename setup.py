#!/usr/bin/env python

import os
from setuptools import setup, find_packages

with open("README.md", encoding="utf8") as readme_file:
    readme = readme_file.read()

install_requirements = [
    "wheel",
    # "ocean-lib==1.0.0a2",
    "ocean-lib==0.8.5",
    "huggingface_hub",
    "hub",
    "torch",
    "PyNaCl",
    "notebook",
    "python-dotenv"
]

setup(
    name = "dhub",
    version = "0.0.1",
    author = "Algovera",
    author_email = "hello@algovera.ai",
    description = ("🧠 A decentralized hub for AI assets."),
    license = "Apache",
    keywords = "web3 model-hub machine-learning models deep-learning pytorch pretrained-models",
    url = "https://github.com/AlgoveraAI/dHub",
    packages=find_packages('dhub'),
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=install_requirements,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)


