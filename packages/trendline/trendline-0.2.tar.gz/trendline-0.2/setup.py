# setup.py

from setuptools import setup, find_packages

setup(
    name='trendline',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
    ],
    description='Trendline is a Python library designed for automatic estimation of financial asset price trendlines.',
    author='Ryan L',
    author_email='rylu.lubis@gmail.com',
    url='https://github.com/ryanllu/trendline',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
