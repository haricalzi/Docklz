from setuptools import setup, find_packages

setup(
    name='docklz',
    version='1.0.0',
    description='Strumento che effettua analisi di sicurezza relative a immagini e container Docker in modo automatizzato',
    author='Hari Calzi',
    author_email='calzihari@gmail.com',
    download_url='https://github.com/haricalzi/Docklz',
    python_requires='>=3.11',
    packages=find_packages(),
    install_requires=[
        'argparse', 
        'datetime',
        'aiohttp',
        'asyncio',
        'matplotlib',
        'ssvc',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'docklz = docklz.docklz:main',
        ],
    },
)