from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

setup(
    name="simple_dependency_injector",
    version="0.1.0",
    description="A simple dependency injection framework for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="José Manuel Carretero",
    author_email="josemanuelcarreterocuenca@gmail.com",
    url="https://github.com/josemanuelcarretero/python-simple-dependency-injector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements("requirements.txt"),
)
