from setuptools import setup, find_packages

setup(
    name='to_parquet_to_aws',
    version='0.3',
    packages=find_packages(),
    install_requires=[ 'pandas', 'boto3' ],
)