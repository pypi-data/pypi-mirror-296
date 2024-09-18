from setuptools import setup, find_packages

setup(
    name='sharepoint-to-df',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'office365-rest-python-client'
    ],
    author='Mutaz Younes',
    author_email='mutazyounes@gmail.com',
    description='A library to read SharePoint lists into pandas DataFrames.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sharepoint-to-df',
)
