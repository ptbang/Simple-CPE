# Simple-CPE
A simple script to parse CPE 2.3 string format

## Requirements
- Python 3.10 (tested)
- Install CPE - the official package supported by NIST `pip install cpe` (latest version 1.2.1)

## Usage
Shell command line:
```console
python3 simple_cpe.py 'cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*'
```

To get a python dict from fs string:
```python
from simple_cpe import SimpleCPE


fs = 'cpe:2.3:a:microsoft:internet_explorer:8.0.6001:beta:*:*:*:*:*:*'
cpe = SimpleCPE(fs)
cpe_dict = cpe.get_values()  # returns a dict
```

Tests:
```console
python3 tests.py
```
