from setuptools import setup, find_packages

setup(
    name='easychrono',  
    version='0.1.3', 
    author='Alexander Roberts',
    author_email='ale.roberts@live.ca',
    description='A Python package for working with timedelta objects and more',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/legendofpokemon/easychrono',  # Your project URL
    packages=find_packages(),  # Automatically find packages in the directory
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        
    ],
)
