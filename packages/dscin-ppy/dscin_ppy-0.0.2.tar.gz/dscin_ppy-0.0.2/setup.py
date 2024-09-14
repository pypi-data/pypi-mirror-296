from setuptools import find_packages, setup

setup(
    name="dscin_ppy",
    version="0.0.2",
    author="Andrea Chiappo",
    author_email="chiappo.andrea@gmail.com",
    description="Collection of utility functions",
    packages=find_packages(include=["dscin_ppy"]),
    test_suite="tests",
    install_requires=[
        "boto3==1.24.59",
        "pandas==2.0.1",
        "numpy==1.23.5",
        "hdbcli==2.17.22"
    ]
)