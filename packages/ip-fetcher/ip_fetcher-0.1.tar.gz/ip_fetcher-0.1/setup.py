# setup.py

from setuptools import setup, find_packages

setup(
    name="ip_fetcher",
    version="0.1",
    packages=find_packages(),
    description="A simple library to fetch public and private IP addresses",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/anonymous/ip_fetcher",  # Replace with actual URL if available
    author="Anonymous",
    author_email="anonymous@example.com",
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
