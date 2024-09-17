from setuptools import setup, find_packages
import subprocess
import sys
import os

# Leer el archivo README.md de forma segura
this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = ""
readme_path = os.path.join(this_directory, 'README.md')

if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()

install_requires = ["opencv-python>=4.5.3.56"]

# Añadir Jetson.GPIO solo si se detecta que estás en una Jetson
import subprocess

def is_jetson():
    try:
        # Ejecuta el comando `lscpu` y captura su salida
        cpu_info = subprocess.check_output("lscpu", shell=True).decode()
        # Verifica si el procesador es ARM (usado por Jetson)
        return 'aarch64' in cpu_info or 'arm' in cpu_info
    except subprocess.CalledProcessError:
        return False

if is_jetson():
    install_requires.append('Jetson.GPIO>=2.0.0')

setup(
    name="larva_lib",
    version="0.0.0.3",
    packages=find_packages(),
    install_requires=install_requires,
    author="HectorVR-Dev",
    author_email="hectordaniel1112@gmail.com",
    description="A library for controlling stepper motors and lighting for larva motion experiments",
    long_description=long_description,  # Usamos el contenido del README si existe
    long_description_content_type='text/markdown',
    url="https://github.com/HectorVR-Dev/larva_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
