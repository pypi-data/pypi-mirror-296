
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mockdata",
    version="1.0.3",
    author="半只程序员",
    description="mockdata生产数据",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joyamon/mockdata",
    packages=find_packages(where='.', exclude=(), include=('*',)),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['Faker',  'Pillow'],
    python_requires='<3.13',
    include_package_data=True,
    install_package_data=True,
)