from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='seaturtle_db',
    version="2.0.0",
    license="MIT",
    description="Python files used as databases.",
    long_description=long_description,
    author="Tathya Garg",
    author_email="coding.tathya@gmail.com",
    packages=["seaturtle_db"]
)