from setuptools import setup, find_packages
import os

# Reading the README file
def read_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()
    return ""

setup(
    name="ip_fetcher",
    version="0.3.4.1",
    packages=find_packages(),
    description="A Python library to fetch public and private IP addresses.",
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",  
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        'requests>=2.20.0',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'ip-fetcher=ip_fetcher.cli:main',
        ],
    },
    python_requires='>=3.6',
    keywords="IP address, public IP, private IP, network utilities, Python library, CLI tool, IP fetching, IP",
)
