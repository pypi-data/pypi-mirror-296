from setuptools import setup, find_packages

setup(
    name='ergo_angle',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.3',
        'torch==2.2.0',
        'ultralytics==8.2.8'
    ] 
)