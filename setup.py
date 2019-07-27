from setuptools import setup, find_packages

setup(
    name='viperdriver',
    author='vipervit',
    author_email='vitolg1@gmail.com',
    license='Apache',
    description='Collection of tools and libraries including custom expansion of Selenium WebDriver.',
    version='0.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests", "test*"])
)
