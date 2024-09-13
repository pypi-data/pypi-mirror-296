from setuptools import setup, find_packages

setup(
    name='tcra',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0,<3.0.0',  # Allows any version of NumPy from 1.21.0 to below 3.0.0
        'pandas>=1.3.0',  # Requires at least pandas version 1.3.0 or higher
        'matplotlib>=3.4.0',  # Ensures compatibility with newer matplotlib versions
        'scipy>=1.6.0',  # Allows SciPy 1.6.0 or higher
        'folium>=0.12.0',  # Ensures folium 0.12.0 or higher
    ],
    description='A Python package for estimating cyclone hazard parameters and calculating wind speeds at structure sites.',  # Make sure this is under 512 characters
    long_description=open('README.md').read(),  # Detailed description is handled by this field
    long_description_content_type='text/markdown',
    url='https://github.com/rxm562/TCRA.git',
    author='Ram Krishna Mazumder',
    author_email='rkmazumder@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    )