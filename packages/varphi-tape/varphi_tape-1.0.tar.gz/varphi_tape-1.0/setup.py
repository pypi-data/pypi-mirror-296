from setuptools import setup, find_packages

setup(name="varphi-tape", 
      version="1.0", 
      packages=find_packages(),
      install_requires=[
        "antlr4-python3-runtime",
      ]
    )