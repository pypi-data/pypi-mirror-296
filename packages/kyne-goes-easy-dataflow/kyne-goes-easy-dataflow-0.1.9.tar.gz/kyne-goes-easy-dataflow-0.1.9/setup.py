from setuptools import setup, find_packages

setup(
    name='kyne-goes-easy-dataflow',      # Nombre del paquete
    version='0.1.9',                 # Versión
    packages=find_packages(),        # Encuentra automáticamente los paquetes en la estructura
    install_requires=[               # Lista de dependencias necesarias
        # Ejemplo: 'numpy', 'pandas'
    ],
    author='Kynegos - Capital Energy',
    author_email='digital.data@capitalenergy.com',
    description='Automatización de procesos de Data para Kynegos',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/GabiAnt95/kynegoeasy-dataflow',  # Repositorio de GitLab
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

