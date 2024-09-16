from setuptools import setup, find_packages

setup(
    name='pystdlib',              
    version='0.0.2',               
    description='A custom standard library module for Python',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Disoft',           
    author_email='ciccabr9@gmail.com',  
    url='https://github.com/disoft-io/pystdlib/tree/main',      
    packages=find_packages(),    
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',     
)
