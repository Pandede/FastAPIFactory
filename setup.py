from setuptools import setup, find_packages

setup(
    name='fastapi-factory',
    version='0.1.0',
    description='Some simple utilities for building `FastAPI` application.',
    author='Pandede',
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette-exporter'
    ]
)
