from setuptools import setup, find_packages

setup(
    name="intuned_sdk",
    version="0.0.4",
    description="Intuned Python SDK",
    author="Intuned",
    author_email="infra@intuned.com",
    url="https://github.com/intuned/intuned-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3",
        "botocore",
        "playwright==1.44.0",
        "python-dotenv==1.0.1",
    ],
)
