from setuptools import setup, find_packages

setup(
    name='envcrypt',
    version='0.1.1',
    description='A Python library for managing encrypted environment files using Base64 and AES, with support for backups and integrity checks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ali Crafty',
    author_email='aaasdujkkofe@gmail.com',
    url='https://alicrafty1191.github.io/EnvCrypt/',
    packages=find_packages(),
    install_requires=[
        'cryptography',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)