# setup.py

from setuptools import setup, find_packages

setup(
    name='auto_fix',
    version='1.0.5211',
    description='使用AI模型的自动代码修复库.',
    author='Feicell',
    author_email='a@love-me.vip',
    packages=find_packages(),
    install_requires=[
        'openai',
        'loguru',
    ],
)
