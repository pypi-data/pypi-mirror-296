from setuptools import setup, find_packages

setup(
    name='aws_wand',
    version='1.0.2',
    author='Rodion S.',
    author_email='rodion.shyshkin@gmail.com',
    description='Simple API to train ML models on AWS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    pyhton_requires='>=3.12',
)