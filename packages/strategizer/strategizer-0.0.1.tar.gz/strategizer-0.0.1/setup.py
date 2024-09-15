from setuptools import setup, find_packages

setup(
    name='strategizer',
    version='0.0.1',
    author='Nathan Schmidt',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nathanschmidt89/strategizer',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)