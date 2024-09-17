from setuptools import setup, find_packages

setup(
    name='smartup',
    version='0.0.1',  # Update this for new versions
    description='A Python package for interacting with the SmartUp API and Platform.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Marcelo Arias',
    author_email='marcelo@smartup.lat',
    packages=find_packages(),
    install_requires=[],  # List your package dependencies here
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Choose a license
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
