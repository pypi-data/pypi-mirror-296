from setuptools import setup, find_packages

setup(
    name='delibtools',
    version='0.1.0',
    author='Arman Irani', 
    author_email='airan002@ucr.edu',
    description='A package for calculating Deliberation Intensity based on Reddit or similar datasets.',
    long_description='Includes tools for generating unique thread IDs, calculating deliberation intensity, and visualizing results.',
    url='https://github.com/armaniii/delibtools',  
    packages=find_packages(),  
    install_requires=[
        'pandas>=1.0',      
        'numpy>=1.18',
        'tqdm>=4.0',
        'sentence-transformers>=2.0',
        'seaborn>=0.11',
        'matplotlib>=3.0',
        'scipy>=1.4',
        'nltk>=3.5'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version
)