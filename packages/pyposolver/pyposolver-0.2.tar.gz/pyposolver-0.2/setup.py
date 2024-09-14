from setuptools import setup, find_packages

setup(
    name='pyposolver',
    version='0.2',
    author='Prakhar Doneria',
    author_email='prakhardoneria3@gmail.com',
    description='A Python library for mathematical and physics calculations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/prakhardoneria/pyposolver-prod',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
