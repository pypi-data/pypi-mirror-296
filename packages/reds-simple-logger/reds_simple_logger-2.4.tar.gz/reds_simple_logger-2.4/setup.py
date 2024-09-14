from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='reds_simple_logger',
    version='2.4',
    packages=["reds_simple_logger"],
    install_requires=["termcolor", "datetime"],
    author="Red_Wolf2467",
    author_email="support@pyropixle.com",
    description="Allows you to make console logging more simple.",
    long_description=long_description,  # Setze die lange Beschreibung
    long_description_content_type="text/markdown",
    python_requires='>=3.8'
)