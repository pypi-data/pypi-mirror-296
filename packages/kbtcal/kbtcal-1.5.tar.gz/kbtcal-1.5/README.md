This is a simple library that performs
basic python arithmetic operations.

## Installation
```
pip install kbtcal

```

## Usage:
A guide to using the add_numbers function is as follows

```
import kbtcal
add_num = kbtcal.add_numbers(3, 7) # where 3 and 7 are the number you want to add
print(add_num)

```
The functions in this library are:
1. add_numbers
2. subtract_numbers
3. multiply_numbers 
4. divide_numbers_float 
5. divide_numbers_floor
6. power_numbers
7. mode_numbers


## Update:
This version of the library contains dummy datasets (cpen and fpen) for learning and demonstration purposes.

```
from kbtcal import datasets
data = datasets.load_cpen() # loads the cpen dataset
print(data)

```

## Video Usage Guide
A video usage guide is provided via this link [YouTube Link](https://www.youtube.com/channel/UCsI1eKRkwDGKwBgwTD6_hnQ)

## License
Copyright 2024 KenBroTech

This repository is licensed under MIT license.
See LICENSE for details.
