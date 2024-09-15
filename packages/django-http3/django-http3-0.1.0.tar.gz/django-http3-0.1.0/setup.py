from setuptools import setup, find_packages

setup(
    name='django-http3',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=3.0',
        'aioquic',
        'asgiref',
    ],
    author='Ibrahim Muhaisen',
    author_email='ibrahim.muhaisen.2015@gmail.com',
    description='A Django package for automatic HTTP/3 support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hemaxox/django-http3-package',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)