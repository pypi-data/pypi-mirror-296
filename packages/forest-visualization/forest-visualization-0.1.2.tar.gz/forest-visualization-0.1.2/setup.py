from setuptools import setup, find_packages

setup(
    name="forest-visualization",
    version="0.1.2",
    author="Ganesh Bhagwat",
    author_email="bhagwatganesh716@gmail.com",
    description="A Python package for forest structure visualization and traversals",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ganeshb15/forest-visualization",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "turtle==0.0.1"  # Add other dependencies here
    ],
)