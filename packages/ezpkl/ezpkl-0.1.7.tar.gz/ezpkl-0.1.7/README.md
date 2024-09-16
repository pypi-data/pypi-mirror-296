# EZPKL: lovely pickling🥒 for context manager hater👊

 [![PyPI version](https://badge.fury.io/py/ezpkl.svg)](https://badge.fury.io/py/ezpkl) [![Python Downloads](https://static.pepy.tech/badge/ezpkl)](https://pepy.tech/project/ezpkl)

<h4 align="center">
    <p>
        English |
        <a href="https://github.com/yesinkim/ezpkl/blob/main/README_ko.md">한국어</a>
    </p>
</h4>

![EZPKL character](https://raw.githubusercontent.com/yesinkim/ezpkl/main/assets/banner.png)
I hate `with open(file_path) as file...` and I don't want to google `how to save pickle in python` anymore. 
then, i made it.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ezpkl.

```bash
pip install ezpkl
```

## Usage

### Save Object to pkl

```python
from ezpkl import save_pkl

a = [1, 2, 3, 4, 5]

# 'a.pkl' will be saved in the current directory.
save_pkl(var=a)

# 'a_list_temp.pkl' will be saved in the current directory.
save_pkl(var=a, file_name='a_list_temp')
```

### Load Object

```python
from ezpkl import load_pkl

a = load_pkl('a.pkl')
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
