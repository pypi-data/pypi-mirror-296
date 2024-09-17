# setup.py

from setuptools import setup

setup(
    name='pynacci',  
    version='2.1.1',  
    description='Una librería para trabajar con la serie de Fibonacci',
    long_description=open('README.txt', encoding='utf-8').read(),  
    long_description_content_type='text/plain',  
    author='Pablo Álvaro',  
    author_email='palvaroh2000@gmail.com',  
    license='MIT',  
    py_modules=['pynacci'], 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent', 
    ],
    python_requires='>=3.6',  
    keywords='fibonacci mathematics generator', 
)
