from setuptools import setup, find_packages

setup(
    name='bluepm',  
    version='0.1.0',
    description='A Python client for interacting with the Blue project management GraphQL API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Emanuele Faja',
    author_email='manny@blue.cc',
    url='https://gitlab.com/bloohq/blue-python-module',  
    packages=find_packages(),
    install_requires=[
        'anyio',
        'backoff',
        'certifi',
        'charset-normalizer',
        'gql',
        'graphql-core',
        'idna',
        'multidict',
        'requests',
        'requests-toolbelt',
        'sniffio',
        'urllib3',
        'yarl',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
