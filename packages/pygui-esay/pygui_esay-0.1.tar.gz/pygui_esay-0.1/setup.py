# setup.py
from setuptools import setup, find_packages

setup(
    name='pygui-esay',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    description='Uma biblioteca de interface gráfica simples.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Seu Nome',
    author_email='seuemail@example.com',
    url='https://github.com/seuusuario/interface_lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
