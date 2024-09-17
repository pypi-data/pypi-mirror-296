from setuptools import setup
setup(
    install_requires = [
    'numpy>=1.26.4',
    'pandas>=2.2.2',
    'dask>=2024.7.0',
    'xarray>=2024.6.0',
    'netcdf4>=1.7.1.post1',
    'py4ease>=v0.0.13',
    ],
    python_requires = '==3.10.4',
    scripts=["bin/combine_delta"]
)
