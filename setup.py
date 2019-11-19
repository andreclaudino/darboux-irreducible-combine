from setuptools import setup
from setuptools import find_packages

setup(
    name='combina-dataset',
    version='1.0',
    packages=find_packages(),
    url='',
    license='',
    author='André Claudino',
    author_email='',
    description='',
    install_requires = [
        'sympy',
        'scipy',
        'twine'
    ],
    entry_points = {
        'console_scripts': ['combina-irredutiveis=main:main']
    }
)
