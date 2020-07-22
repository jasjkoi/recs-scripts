from setuptools import setup

setup(
    name='recs-scripts',
    version='0.1',
    install_requires=['boto3', 'pandas', 'requests'],
    description='Collection of python scripts to interact with S3'
)