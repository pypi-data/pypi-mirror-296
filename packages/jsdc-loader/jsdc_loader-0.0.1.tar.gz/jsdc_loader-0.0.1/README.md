
# JSDC Loader (JSON Data Class Loader)

JSDC Loader is a Python utility for loading JSON configuration files into dataclass objects. It provides a simple and type-safe way to manage configuration data in your Python applications by forcing the use of dataclass and type hinting.

## Features

- Load JSON configuration files into dataclass objects
- Support for nested dataclass structures
- Type checking and conversion for configuration values
- Easy updating of configuration from different files
- Ability to dump modified configurations back to JSON

## Installation

To install JSDC Loader, you can use pip:

```bash
pip install jsdc_loader
```

## Usage

Here's an example of how to use JSDC Loader:

### Example 1
```python
from dataclasses import dataclass
from jsdc_loader import JSDC_Loader

@dataclass
class DatabaseConfig:
    host: str = 'localhost' # default value must be provided
    port: int = 3306
    user: str = 'root'
    password: str = 'password'


config = JSDC_Loader('config.json', DatabaseConfig)
print(config.host)
```

### Example 2
```python
from dataclasses import dataclass, field
from jsdc_loader import JSDC_Loader

# Database Config ...

@dataclass
class UserConfig:
    name: str = 'John Doe'
    age: int = 30

@dataclass
class AppConfig:
    user: UserConfig = field(default_factory=lambda: UserConfig())
    database: DatabaseConfig = field(default_factory=lambda: DatabaseConfig())

config = JSDC_Loader('config.json', AppConfig)
print(config.user.name)
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.