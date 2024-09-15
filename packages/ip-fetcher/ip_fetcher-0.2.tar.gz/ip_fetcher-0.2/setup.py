# setup.py

from setuptools import setup, find_packages

setup(
    name="ip_fetcher",
    version="0.2",  # Increment version for updates
    packages=find_packages(),
    description="A Python library to fetch public and private IP addresses.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'requests',
    ],
)
