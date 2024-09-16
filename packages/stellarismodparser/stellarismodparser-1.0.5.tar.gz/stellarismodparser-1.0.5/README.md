# StellarisModParser

[<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/stellarismodparser">](https://pypi.org/project/stellarismodparser/)
[<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/stellarismodparser">](https://pypi.org/project/stellarismodparser/)
[<img alt="PyPI - License" src="https://img.shields.io/pypi/l/stellarismodparser">](https://www.coastalcommits.com/Seaswimmer/StellarisModParser/src/branch/master/LICENSE/)  
This package provides a simple parser for Stellaris's mod descriptor format.

## Usage

```python-repl
>>> import stellarismodparser
>>> path = "/home/seaswimmer/Projects/StellarisMods/No Menacing Ships.mod"
>>> mod = stellarismodparser.parse(path)
>>> mod.name
'No Menacing Ships'
>>> str(mod.supported_version)
'Andromeda 3.12.4'
>>> mod.tags
['Balance', 'Gameplay']
```
