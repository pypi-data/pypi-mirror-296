from typing import Type, get_type_hints, Optional, TypeVar, Generic
from dataclasses import dataclass
import json

T = TypeVar('T', bound=dataclass)

# JSON Data Class Loader
class JSDC_Loader(Generic[T]):
    def __init__(self, config_path: str, config_class: Type[T]):
        self.config_path = config_path
        self.config: T = config_class()
        self.load_config()
    
    def update(self, config_path: str):
        self.config_path = config_path 
        self.load_config()

    def load_config(self, config_path: str = None, encoding: str = 'utf-8'):      
        if config_path is None:
            config_path = self.config_path
        
        with open(config_path, 'r', encoding=encoding) as f:
            if config_path.endswith('.json'):
                import json
                config = json.load(f)
            else:
                raise ValueError('not supported file format, only json is supported')

        for key, value in config.items():
            key = key.lower()
            if hasattr(self.config, key):
                if isinstance(value, dict):
                    _config = getattr(self.config, key)
                    self._update_nested_config(_config, value)
                else:
                    setattr(self.config, key, value)
            else:
                raise ValueError(f'unknown config key: {key}')

    def _update_nested_config(self, obj, config):
        type_hints = get_type_hints(type(obj))
        
        for sub_key, sub_value in config.items():
            if hasattr(obj, sub_key):
                expected_type = type_hints.get(sub_key)
                if isinstance(sub_value, dict):
                    sub_obj = getattr(obj, sub_key)
                    self._update_nested_config(sub_obj, sub_value)
                else:
                    if expected_type is not None:
                        try:
                            from enum import Enum
                            if issubclass(expected_type, Enum):
                                sub_value = expected_type[sub_value]
                            else:
                                sub_value = expected_type(sub_value)
                        except (ValueError, KeyError):
                            raise ValueError(f'invalid type for key {sub_key}, expected {expected_type}, got {type(sub_value)}')
                    setattr(obj, sub_key, sub_value)
            else:
                raise ValueError(f'unknown config key: {sub_key}')

    def dump_json(self, output_path: str):
        config_dict = self._dataclass_to_dict(self.config)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f)

    def _dataclass_to_dict(self, obj):
        if isinstance(obj, list):
            return [self._dataclass_to_dict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return {key: self._dataclass_to_dict(value) for key, value in vars(obj).items()}
        return obj

if __name__ == '__main__':
    from dataclasses import dataclass, field
    from typing import Optional
    @dataclass
    class CA:
        a: int = 0
        b: str = ''

        def to_dict(self):
            return {
                'a': self.a,
                'b': self.b
            }


    @dataclass
    class Demo:
        inherit_demo: CA = field(default_factory=lambda: CA())
        a: int = 0
        b: str = ''
        c: list[int] = field(default_factory=lambda: [0, 0, 0])
        d: Optional[int] = None

        def to_dict(self):
            return {
                'inherit_demo': self.inherit_demo.to_dict(),
                'a': self.a,
                'b': self.b,
                'c': self.c,
                'd': self.d
            }

    config = Demo()
    config.inherit_demo.a = 9
    config.a = 1
    config.b = '1'
    config.c = [1, 2, 3]
    config.d = None
    with open('demo.json', 'w', encoding='utf-8') as f:
        json.dump(config.to_dict(), f)

    JSDC_Loader = JSDC_Loader('demo.json', Demo)
    print(JSDC_Loader.config)

    JSDC_Loader.config.a = 2
    JSDC_Loader.dump_json('demo_modified.json')

    JSDC_Loader.update('demo_modified.json')
    print(JSDC_Loader.config)

    JSDC_Loader.config.e = 'test'
    JSDC_Loader.dump_json('demo_error.json')

    try:
        JSDC_Loader = JSDC_Loader('demo_error.json', Demo)
    except ValueError as e:
        print(e)

    import os
    os.remove('demo.json')
    os.remove('demo_modified.json')
    os.remove('demo_error.json')

