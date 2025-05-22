from setuptools import setup, find_packages

#setup(
 #   name="edu_pad",
  #  version="0.0.1",
   # author="Jesus Gonzaez",
    #author_email="",
    #description="ETL para análisis de datos del dólar",
    #py_modules=["actividad1", "actividad2"],
    #install_requires=[
     #   "pandas",
      #  "openpyxl",
       # "requests",
        #"beautifulsoup4"
    #]
#)

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="edu_pad",
    version="0.0.1",
    author="Jesus Gonzalez",
    author_email="",
    description="ETL para análisis de datos del dólar",
    py_modules=["actividad1", "actividad2"],
    install_requires=requirements,
)
