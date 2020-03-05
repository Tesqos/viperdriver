from setuptools import setup, find_packages

from viperdriver import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='viperdriver',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    license='Apache',
    description='A custom expansion of Selenium WebDriver.',
    long_description = long_description,
    version=__version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test*"]),
    install_requires='[viperlib', 'keyring']'
    description='Custom expansion of Selenium WebDriver.',
    version=__version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test*"])
)
