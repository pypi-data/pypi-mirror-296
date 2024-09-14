from setuptools import setup, find_packages

setup(
    name="cam_ilt",  
    version="0.1.0",    
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy"],  
    author="Julian Beckmann",
    author_email="jbbb2@cantab.ac.uk",
    description="A Python package for the inversion of magnetic resonance datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jbbb2/cam_ilt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
