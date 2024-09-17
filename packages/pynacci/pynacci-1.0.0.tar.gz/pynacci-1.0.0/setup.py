from setuptools import setup

setup(
    name='pynacci',  
    version='1.0.0',  
    description='Una librería para trabajar con la serie de Fibonacci',
    long_description=open('README.txt', encoding='utf-8').read(),
    long_description_content_type='text/plain', 
    author='Pablo Álvaro', 
    author_email='palvaroh2000@gmail.com',  
    url='https://www.linkedin.com/in/pabblo2000/', 
    py_modules=['pynacci'],  
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',  
)