# vim: expandtab tabstop=4 shiftwidth=4

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='dspftw',
    version='2020.250.0',
    author='Bill Allen',
    author_email='photo.allen@gmail.com',
    description='Utilities for digital signal processing (DSP) fundamentals.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='dsp sinusoid'.split(),
    url='https://github.com/gershwinlabs/dspftw',
    packages=['dspftw'],
    package_data={'dspftw': ['doc/*']},
    install_requires=['numpy', 'matplotlib'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License'
    ]
)
