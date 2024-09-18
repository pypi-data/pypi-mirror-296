from setuptools import setup, find_packages

setup(
    name='sharepoint_to_df',
    version='0.2.0',
    description='A library to fetch SharePoint list data and return it as a Pandas DataFrame.',
    author='Mutaz Younes',
    author_email='mutazyounes@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'office365-rest-python-client'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
