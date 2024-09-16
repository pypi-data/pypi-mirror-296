from setuptools import setup, find_packages

setup(
    name="ip_fetcher",
    version="0.3.3",
    packages=find_packages(),
    description="A Python library to fetch public and private IP addresses.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'ip-fetcher=ip_fetcher.cli:main',  # Update to reference cli in ip_fetcher package
        ],
    },
    python_requires='>=3.9.7',
    keywords="IP address, public IP, private IP, network utilities, Python library, CLI tool, IP fetching",
)
