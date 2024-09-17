from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='lik',
    version='0.0.1',
    url='https://github.com/psychAo/lik',
    author='psychAo',
    author_email='psychao@outlook.com',
    description='test my lik package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['numpy'],
)