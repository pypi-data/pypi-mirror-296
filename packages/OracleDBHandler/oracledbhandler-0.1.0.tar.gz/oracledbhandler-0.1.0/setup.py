from setuptools import setup, find_packages

setup(
    name="OracleDBHandler",
    version="0.1.0",
    description="A simple OracleDB handler for executing queries with pandas.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="pvdphong",
    author_email="phong.phamvd@homecredit.vn",
    url="https://github.com/pvdphong/OracleDBHandler",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "oracledb"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
