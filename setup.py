from setuptools import setup, find_packages

setup(
    name='fastapi-factory',
    version='0.1.0',
    license='MIT',
    description='Some simple utilities for building `FastAPI` application.',
    author='Pandede',
    url='https://github.com/Pandede/FastAPIFactory',
    download_url='https://github.com/Pandede/FastAPIFactory/archive/refs/tags/v0.1.0.tar.gz',
    keywords=['fastapi', 'utility'],
    packages=find_packages(),
    install_requires=[
        'fastapi',
        'starlette-exporter'
    ],
    classifiers=[
        'Developer Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
