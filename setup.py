from setuptools import setup, find_packages

setup(
    name='docalzi',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docalzi = docalzi.docalzi:main',
        ],
    },
)