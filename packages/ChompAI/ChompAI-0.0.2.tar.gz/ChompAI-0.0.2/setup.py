from setuptools import setup, find_packages
import codecs
import os



VERSION = '0.0.2'
DESCRIPTION = 'Chomp computer'

# Setting up
setup(
    name="ChompAI",
    version=VERSION,
    author="purple-ish",
    include_package_data=True,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['chomp'],
)