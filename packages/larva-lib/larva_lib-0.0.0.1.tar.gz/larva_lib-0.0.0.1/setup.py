from setuptools import setup, find_packages
import os
import platform

# Leer el archivo README.md de forma segura
this_directory = os.path.abspath(os.path.dirname(__file__))
long_description = ""
readme_path = os.path.join(this_directory, 'README.md')

if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()

install_requires = ["opencv-python>=4.5.3.56"]

# Añadir Jetson.GPIO solo si se detecta que estás en una Jetson
def is_jetson():
    try:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().lower()
        return 'jetson' in model
    except FileNotFoundError:
        # El archivo no existe, no es una Jetson
        return False

if is_jetson():
    install_requires.append("Jetson.GPIO>=2.0.17")

setup(
    name="larva_lib",
    version="0.0.0.1",
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
