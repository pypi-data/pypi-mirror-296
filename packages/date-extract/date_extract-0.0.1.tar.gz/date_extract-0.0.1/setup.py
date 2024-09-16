from setuptools import setup, find_packages

setup(
    name="date_extractor",
    version="0.1.0",
    author="Eric Ellingson",
    author_email="god@eric.wtf",
    description="A package for detecting and extracting date suggestions text.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/e-e/date_extractor",  # Replace with your package's URL
    packages=find_packages(),
    install_requires=[
        "spacy>=3.7.6",
        "pytest>=8.3.3",  # For testing purposes
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)