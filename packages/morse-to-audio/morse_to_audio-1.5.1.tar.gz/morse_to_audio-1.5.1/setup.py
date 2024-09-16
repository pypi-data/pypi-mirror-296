import os

import platform

import pkg_resources

from setuptools import find_packages, setup


setup(
    name="morse-to-audio",
    version="1.5.1",  # Increment the version number here
    description="The **Morse-to-Audio** project converts Morse code into audio files. Users can input Morse code (using dots, dashes, and spaces), and the program generates an audio output in `.wav` format. The project allows customization of tone frequency and dot duration for flexibility.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    readme="README.md",
    python_requires=">=3.10",
    author="kindahex",
    url="https://github.com/kindahex/morse-to-audio",
    license="MIT",
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rep', '*.pickle']},
    install_requires=[
        "pydub",
    ],
    include_package_data=True,
)
