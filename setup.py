from setuptools import setup, find_packages

setup(
    name='viperbox',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    licence='MIT',
    description='Collection of tools and libraries including custom expansion of Selenium WebDriver.',
    version='0.53.3',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test*"])
)
