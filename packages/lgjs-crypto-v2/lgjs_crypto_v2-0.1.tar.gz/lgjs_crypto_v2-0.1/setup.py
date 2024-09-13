# setup.py

from setuptools import setup, find_packages

setup(
    name='lgjs_crypto_v2',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ccxt',
        'pandas',
    ],
    description='A package to search cryptocurrency data using Kraken',
    author='liamgen.js',
    author_email='liamgen.js@proton.me',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)