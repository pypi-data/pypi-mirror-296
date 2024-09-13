from setuptools import setup, find_packages

setup(
    name='aspirart',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests'],
    author='Liam Attwood',
    author_email='liam@liamattwood.com',
    description='A simple Python wrapper for the Aspirart API',
)
