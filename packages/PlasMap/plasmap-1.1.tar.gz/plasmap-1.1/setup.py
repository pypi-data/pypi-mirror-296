from setuptools import setup, find_packages

setup(
    name='PlasMap',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'gdown>=5.2.0',
        'pycirclize==0.0.1',
        'bio>=1.7.1'
    ],
    entry_points={
        "console_scripts":[
            "PlasAnn = PlasAnn:PlasAnn",
        ],
    },
)