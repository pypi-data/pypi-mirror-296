from setuptools import setup, find_packages

setup(
    name="deeper_search",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    python_requires=">=3.6",
    author_email="abubakarilyas624@gmail.com",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
