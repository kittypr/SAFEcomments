from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SAFEcomments',
    version='1.0',

    description='Script to transfer annotations from one doc to another.',
    long_description=long_description,

    url='https://github.com/kittypr/SAFEcomments',

    author='Kharisov Damir, Julia Zhuk',
    author_email='nsu.kharisov.damir@gmail.com, julettazhuk@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='comments transfer annotations notes',

    install_requires=['lxml==4.1.1'],

    scripts=['safecomments/SAFEcomments.py'],

    packages=find_packages()
)
