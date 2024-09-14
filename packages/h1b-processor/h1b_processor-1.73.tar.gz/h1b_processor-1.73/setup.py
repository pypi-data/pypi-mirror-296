from setuptools import setup, find_packages 

setup(
    name='h1b_processor',  # Update this to a unique name
    version='1.73',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'beautifulsoup4',
        'tqdm'
    ],
    author='Aravind Satyanarayanan', 
    author_email='aravind.bedean@gmail.com',
    description='A package for cleaning data frames.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AravindSatyan/data-warehousing/tree/main',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
