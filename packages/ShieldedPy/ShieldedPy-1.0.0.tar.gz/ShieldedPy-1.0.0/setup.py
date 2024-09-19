from setuptools import setup, find_packages

setup(
    name='ShieldedPy',
    version='1.0.0',
    description='A simple library for security tasks like password hashing, token management, and encryption.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tamilselvan Sudalai',
    author_email='tamil.sdl@gmail.com',
    url='https://github.com/tamilsud/ShieldedPy',  # Replace with your repository URL
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
