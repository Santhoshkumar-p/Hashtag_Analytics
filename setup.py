from setuptools import setup, find_packages

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name="social-media-analytics",
    version="0.1",
    description="Keyword and Trends Analytics Platform for social media",
    author="Santhoshkumar Panneerselvam",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)