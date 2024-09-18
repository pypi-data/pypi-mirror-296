from setuptools import find_packages, setup

setup(
    name="ussr",
    version="0.1",
    description="A library for sentence search using DistilBERT and All-MiniLM embeddings",
    author="Bryan Mwangi",
    maintainer="Bryan Mwangi",
    url="https://github.com/BryanMwangi/ussr",
    packages=find_packages(),
    install_requires=[
        "torch>=2.2.2",
        "transformers>=4.44.2",
        "numpy>=1.26.4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
