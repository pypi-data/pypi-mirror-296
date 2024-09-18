from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pacote_matrizes",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    author="Fábio Wood",
    author_email="fabio.wood.rs@gmail.com",
    description="A package for summing rows and columns in Pandas DataFrames",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/woodfabio/DIO-Criando-um-pacote-com-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
