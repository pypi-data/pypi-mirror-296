# setup.py
from setuptools import setup, find_packages

setup(
    name="databricks_package_t_2",  # Your package name
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    author="Shashank",
    author_email="shashank.b@hoonartek.com",
    description="A package to load and display CSV data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
