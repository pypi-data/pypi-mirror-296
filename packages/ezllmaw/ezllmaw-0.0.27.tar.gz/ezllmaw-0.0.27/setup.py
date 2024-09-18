# setup.py

from setuptools import setup, find_packages

setup(
    name='ezllmaw',
    version='0.0.27',
    packages=find_packages(),
    install_requires=[],
    description='Easy LLM-Agentic Workflow',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/datanooblol/ezllmaw',
    author='data.noob.lol',
    license='MIT',
)