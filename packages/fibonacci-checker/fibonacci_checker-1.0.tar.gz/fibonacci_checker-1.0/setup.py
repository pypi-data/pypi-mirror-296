from setuptools import setup, find_packages

setup(
    name='fibonacci_checker',
    version='1.0',
    packages=find_packages(),
    description='A library to check if a number is in the Fibonacci sequence',
    long_description=open('README.txt').read(),
    long_description_content_type='text/plain',
    author='Pablo Álvaro',
    author_email='palvaroh2000@example.com',
    url='https://www.linkedin.com/in/pabblo2000/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent']
)
    