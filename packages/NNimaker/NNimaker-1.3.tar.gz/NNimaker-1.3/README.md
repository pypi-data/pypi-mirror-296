## The NN input maker (Now just from QE)

The path to make the this package in python!
### 1. Make  a virtual environment!
As I found lately, without virtual environment, installing some packages may create some troubles in Debian12. 
There were some suggestions out there to solve the issue, but the safe and trust-able method would be using the virtual ENV. 
```
pip install virtualenv              #if you did not have the module for virtual environment!
python3 -m venv ~/venv/venvp        #python<version> -m venv <virtual-environment-name>
source ~/venv/venvp/bin/activate    #activate the virtual environment
```
### 2. Installing the libraries needed to make a package:

```
 pip install setuptools wheel twine
```
 ### 3. make a directory for the root and the package with specific files (`__init__.py` & `setup.py`)!
```
NNimaker/             ### ROOT directory
│
├── NNimaker/         ### Package is here
│   ├── __init__.py
│   ├── read_outputs.py
│   
├── setup.py
└── README.md
```
Where `__init__.py` will be:
```
### __init__.py
from .read_outputs import create_json   
```

And `setup.py` :

```
from setuptools import setup, find_packages

setup(
    name='NNimaker',
    version='1.0',
    packages=find_packages(where='.'),
    package_dir={'NNimaker': 'NNimaker'},
    install_requires=[
        #'numpy',
        #'pandas',
        #'json',
        #'collections',
        #'collections.abc',
        #'ase.data',
        #'glob',
    ],
    entry_points={
        'console_scripts': [
            'NNimake_QE = NNimaker:create_json',
        ],
    },
    author='Mandana Safari',
    author_email='m.safari@cineca.it',
    description='A module for processing user data to NN input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.hpc.cineca.it/msafari1/nnimaker.git',
)

```
Just to emphasise on important and error-prone part: 
### 1. `packages=find_packages(where='.')`

-   **Purpose**: This line tells setuptools to automatically find all packages and sub-packages that should be included in the distribution.
-   **Explanation**:
    -   `find_packages()` is a utility function from setuptools that searches for packages.
    -   `where='.'` specifies that the search for packages should start in the current directory (the directory where `setup.py` is located).
    -   In this case, this allows setuptools to find the `NNimaker` package directory within the root project directory.

### 2. `package_dir={'NNimaker': 'NNimaker'}`

-   **Purpose**: This line maps the package name to its directory location in the filesystem.
-   **Explanation**:
    -   `package_dir` is a dictionary where the keys are package names and the values are the corresponding directories in the filesystem where those packages can be found.
    -   `{'NNimaker': 'NNimaker'}` means that the package named `NNimaker` is located in the directory `NNimaker` relative to the location of `setup.py`.
    -   This mapping helps setuptools understand that when you refer to `NNimaker` in your code and in the `entry_points`, it should look in the `NNimaker` directory to find the package contents.
   
  The package built and installed smoothly.
  It also can run with the terminal command:
```
  #terminal
  RUN: NNimake_QE ../work/ --outname results1.json --algoname "davidson"
```
 And from a file:
```
  #file.py
from NNimaker import create_json, main

create_json("../work", outname="results2.json", algoname='davidson')

 RUN: python ~/file.py

```
