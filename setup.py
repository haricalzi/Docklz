from setuptools import setup, find_packages

setup(
    name='docklz',
    version='1.0.0',
    python_requires='>=3.11',
    packages=find_packages(),
    install_requires=[
        'argparse', 
        'datetime',
        'requests',
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