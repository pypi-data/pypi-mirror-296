from setuptools import setup, find_packages

setup(
    name="johnlock",
    version="0.3",
    packages=find_packages(),
    description="A simple package that says hello",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/johnlock/johnlock",
    author="John Lock",
    author_email="john.lock@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

