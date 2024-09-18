from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="miguel_paquete",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Miguel Rodil",
    description="Consultar cursos",
    long_description=long_description,
    long_description_content_type="text/markdown",
)