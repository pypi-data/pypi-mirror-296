from setuptools import setup, find_packages

setup(
    name='sheet-logger',  # The name of your package
    version='0.1.1',  # Initial version
    description='A Google Sheets log printer with batching and API rate limit checks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Thorsten Brueckner',  
    author_email='thorsten.brueckner@locaria.com',
    url='https://github.com/Locaria/SheetLogger',  # URL to the project
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        'google-auth',  # Add required dependencies here
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python version
)