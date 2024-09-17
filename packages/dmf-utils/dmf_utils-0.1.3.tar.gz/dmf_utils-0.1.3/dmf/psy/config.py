
from typing import Union, Optional
from pathlib import Path
from ..io import load
from ..env import getenv


DEFAULT_CONFIG_VARIABLE = "DMF_CONFIG"

CONFIG : Optional["Config"] = None


def load_config(filename: Optional[Union[str, Path]]=None, force: bool = False) -> "Config":
    """Load the configuration file."""
    global CONFIG
    if CONFIG is None or force:
        CONFIG = Config(filename)
    
    return CONFIG

class Config:
    """General class for configuration parameters."""
    def __init__(self, filename: Union[str, Path] = None):
        self._config = {}

        filename = getenv(DEFAULT_CONFIG_VARIABLE, None)
        self.filename = filename
        if filename is not None:
            loaded = load(filename)
            self._config.update(loaded)

    def get(self, key: str, default=None):
        """Get a value from the content."""
        # The key is a path separated by dots.
        # For example, "experiment.instructions.welcome"
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def __getitem__(self, key):
        return self._config[key]
    
    def __setitem__(self, key, value):
        self._config[key] = value

    def __contains__(self, key):
        return key in self._config
    
    def keys(self):
        return self._config.keys()
    
    def values(self):
        return self._config.values()

    def items(self):
        return self._config.items()
    
    def update(self, other):
        self._config.update(other)

    def __repr__(self):
        return f"Config('{self.filename}')"
    
    def setdefault(self, key, value):
        return self._config.setdefault(key, value)
    

