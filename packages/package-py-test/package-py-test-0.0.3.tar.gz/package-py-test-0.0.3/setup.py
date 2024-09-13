from setuptools import setup, find_packages

# from package-py-test import __version__ as version
setup(
    name="package-py-test",
    version="0.0.3",
    description='test client',
    long_description=open('README.md').read(),
    author='nowhere',
    author_email='contact@nowhereservices.com',
    url='https://github.com/nowherelearn/package-py-test',
    packages=find_packages(),
    license="MIT",
    long_license=open('LICENSE').read(),
    python_requires="~=3.6",
    license_files=('LICENSE'),
    install_requires=[  # List your dependencies here
        'grpcio==1.48.2',
        'protobuf==3.19.6'
    ],
)
