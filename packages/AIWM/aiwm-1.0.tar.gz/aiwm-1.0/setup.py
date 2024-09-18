# setup.py

from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

extensions = [
    Extension("Predict", ["AIWM/Predict.py"]),
]

setup(
    name='AIWM',
    version='1.0',
    packages=['AIWM'],
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'pmdarima',
        'statsmodels',
        'requests',
        'prophet',
        'sklearn',
    ],
)
