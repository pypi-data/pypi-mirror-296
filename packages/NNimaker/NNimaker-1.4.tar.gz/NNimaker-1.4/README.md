# Neural Network inputs  MAKER
### Description
 This python package will detect the output of other codes (still Quantum Espresso) and create a `json` file that can be used as the raw input for Neural Networks. 
## Prerequisite 
The python libraries which are needed to install:
```
numpy,
pandas,
json,
collections,
collections.abc,
ase.data,
glob
```
### Other codes and necessary files:
This package designed in a way that needs 2 inputs. 

**QE output**
It takes the input from Quantum Espresso  OUTPUT (PWSCF).

**SYSINFO.JSON**
This file has the information about the hardware details and creates by `IDENTIKEEP` [plugin](https://github.com/msafari0/Identikeep).
 Make sure that the corresponding files exist in the directory. 

## How to install
#### Method 1:
Installation is based on **Python Package Index** (PyPI) repository.
 ```
pip install NNimaker
```

#### Method 2:
However, if you prefer to create the wheel of package on your laptop, you just need to download the source code from the origin [repository](https://gitlab.hpc.cineca.it/msafari1/nnimaker) . Then follow the path below to create the wheel on your system and then install it.
(Note that you may need use virtual environment to install the necessary packages)
```
pip install setuptools wheel
python setup.py sdist bdist_wheel
pip install dist/NNimaker-<VERSION>-py3-none-any.whl 
```
## How to USE
It is possible to use terminal commands ( The console point is provided).
Since it supports just Quantum Espresso output (till this moment), the command is:
```
NNimake_QE  --folder [DIRECTORY] --outname [OUTPUT] --netinfo [NETWORK INFORMATION] --algname [ALGORITHM]
```
All of the arguments have default values. Default for directory is `./` , Default for output name is `data.json`, Default for netinfo is `Unknown`, and Default for algorithm name is `DAVIDSON`. 
For example, I put the `sysinfo.json` and output file of QE in `../work/` directory. The command line would be:
```
NNimake_QE --folder ../work/ --netinfo "DrogonFly..."
```
You can import the package in your python code directly:
```
from NNimaker import create_json

create_json("../work", outname="data.json", net_info="Unknown", algoname='davidson')
```
Good luck!
_____

