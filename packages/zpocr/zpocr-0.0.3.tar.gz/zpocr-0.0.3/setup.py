from setuptools import setup, find_packages

setup(
    name='zpocr',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'easyocr'
    ],
)