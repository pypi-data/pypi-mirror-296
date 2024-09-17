from setuptools import setup, find_packages

setup(
    name='standlib',              
    version='0.0.8',               
    description='A custom standard library module for Python',
    long_description=open(file='docs/documentation.md', encoding='utf-8').read(),
    author='BrunoCiccarino',           
    author_email='ciccabr9@gmail.com',  
    url='https://github.com/BrunoCiccarino/standlib',      
    packages=find_packages(),    
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',     
)
