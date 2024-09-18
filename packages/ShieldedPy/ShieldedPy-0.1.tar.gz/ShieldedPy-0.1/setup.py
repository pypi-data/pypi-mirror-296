from setuptools import setup, find_packages

setup(
    name='ShieldedPy',
    version='0.1',
    description='A simple library for security tasks like password hashing, token management, and encryption.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tamilselvan Sudalai',
    author_email='tamil.sdl@gmamil.com',
    url='https://github.com/tamilsud/pysecurity',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=[
        'cryptography',
        'PyJWT',
        'passlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
