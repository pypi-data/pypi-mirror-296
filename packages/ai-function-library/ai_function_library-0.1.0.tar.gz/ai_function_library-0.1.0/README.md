# ai_function_library

This is a simple Python library that provides a decorator to convert functions into their source code as a string.

## Installation

```bash
pip install ai_function_library
```
Usage

```python
from ai_function_library import ai_function
@ai_function
def my_function(x: int) -> int:
    """
    This is a docstring.
    """
    return x + 1
print(my_function(5))  # Output: the source code of my_function as a string
```
Example

```python
from ai_function_library import ai_function

@ai_function
def add_numbers(a: int, b: int) -> int:
    return a + b

result = add_numbers(3, 4)
print(result)  # Output: The source code of the add_numbers function as a string
```

# Contributing

Contributions are welcome! Please open an issue or submit a pull request.

# License
This project is licensed under the MIT License - see the LICENSE file for details.