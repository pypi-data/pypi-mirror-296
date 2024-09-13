from setuptools import find_packages, setup

setup(
    name="dscin_ppy",
    version="0.0.1",
    author="Andrea Chiappo",
    author_email="chiappo.andrea@gmail.com",
    description="Collection of utility functions",
    packages=find_packages(include=["dscin_ppy"]),
    install_requires=[
        "boto3==1.35.15",
        "pandas==2.0.1",
        "numpy==1.23.5",
        "hdbcli==2.17.22"
    ]
)