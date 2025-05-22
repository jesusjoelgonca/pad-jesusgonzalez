from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="edu_pad",
    version="0.0.1",
    author="Jesus Gonzalez",
    author_email="jesus.gonzalezc@est.iudigital.edu.co",
    description="ETL para análisis de celular samsung en mercadolibre",
    py_modules=["actividad1", "actividad2"],
    install_requires=requirements,
)
