from setuptools import setup, find_packages

setup(
    name='docklz',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'argparse', 
        'datetime',
        'rpaframework[selenium]',
        'matplotlib',
        'ssvc',
    ],
    entry_points={
        'console_scripts': [
            'docklz = docklz.docklz:main',
        ],
    },
)