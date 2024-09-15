from setuptools import setup, find_packages

setup(
    name="varphi-tape",
    version="1.2",
    description="A package for parsing tape symbols for a Turing machine model using ANTLR.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    url="https://github.com/hassanelsheikha/varphi-tape",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    include_package_data=True,
)
