from setuptools import setup, find_packages

setup(
    name="forest-visualization",
    version="0.1.3",
    author="Ganesh Bhagwat,Shristi Kumari,Vaishnavi Patekar",
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
        "Pillow"  # Add other dependencies here
    ],
)