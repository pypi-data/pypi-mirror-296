from setuptools import setup, find_packages

setup(
    name="intuned-sdk",
    version="0.0.1",
    description="Intuned Python SDK",
    author="Intuned",
    author_email="infra@intuned.com",
    url="https://github.com/intuned/intuned-python-sdk",
    packages=find_packages(),  # Automatically finds sub-packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version requirement
    install_requires=[  # Dependencies
        # List your package dependencies here
    ],
)
