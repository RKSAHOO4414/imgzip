from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imgzip",
    version="0.1.0",
    author="RKSAHOO4414",
    author_email="your_email@example.com",
    description="A lightweight Python library for compressing images with ease",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RKSAHOO4414/imgzip",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=9.0.0",
    ],
)
