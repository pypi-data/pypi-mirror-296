# Readable Passcode
A human-readable passcode generator that creates secure, easy-to-remember passcodes using a combination of common words, numbers, and optional special characters.

## Installation

You can install the package via PyPI using pip.

### 1. Install via PyPI

Run the following command to install the package:

```sh
pip install readable-passcode
```

### 2. Install from Source

Alternatively, you can install the package from the source code. First, clone the repository:

```sh
git clone https://github.com/dedenbangkit/readable-passcode.git
cd readable-passcode
pip install .
```

## Example Usage

### 1. Using the Python API

You can use the passcode_generator function directly in your Python code to generate human-readable passcodes. Customize the number of words, the length of the random number, and whether or not to include a special character.

```python
from readable_passcode import passcode_generator

# Generate a passcode with 4 words
passcode = passcode_generator(word=4)
print(passcode)  # Example output: 'apple-tree-cloud-mountain'

# Generate a passcode with 3 words and a 6-digit number
passcode = passcode_generator(word=3, number=6)
print(passcode)  # Example output: 'apple-tree-cloud-123456'

# Generate a passcode with 2 words, a 4-digit number, and a special character
passcode = passcode_generator(word=2, number=4, special_char=True)
print(passcode)  # Example output: 'apple-tree-1234$'
```
### 2. Using the Command Line Interface (CLI)

You can also generate passcodes directly from the command line. The CLI provides options to specify the number of words, number length, and whether to include a special character.

```sh
# Generate a passcode with the default 3 words
$ readable-passcode
apple-tree-cloud

# Generate a passcode with 4 words
$ readable-passcode --word 4
apple-tree-cloud-mountain

# Generate a passcode with 3 words and a 5-digit number
$ readable-passcode --word 3 --number 5
apple-tree-cloud-12345

# Generate a passcode with 2 words, a 4-digit number, and a special character
$ readable-passcode --word 2 --number 4 --special-char
apple-tree-1234$
```

*CLI Options*

    --word: Specify the number of words in the passcode (default: 3).
    --number: Add a random number of a given length at the end.
    --special-char: Append a random special character to the passcode.

## Key Features

- **Efficient Word Retrieval**: Optimized for performance, allowing you to retrieve random words without needing to load the entire word list into memory, which is particularly useful for large datasets.
- **Command Line Interface (CLI) Support**: Easily generate passcodes or retrieve random words directly from your terminal using simple CLI commands, making it convenient for quick use cases.
- **Lightweight Package**: With a small package size, it ensures minimal overhead and fast installation times, making it suitable for resource-constrained environments or quick setups.
- **Customizable Passcode Generation**: Supports generating human-readable passcodes with customizable options like word count, number length, and inclusion of special characters.
- **Cross-Platform Compatibility**: Works seamlessly across different operating systems, including Linux, macOS, and Windows, whether used as a CLI tool or a Python package.
- **Extensible**: Easy to integrate with other Python applications, making it a flexible tool for developers needing word-based randomization.
- **High Performance**: Designed for both speed and memory efficiency, ensuring smooth performance even with high word retrieval frequencies or large-scale operations.
