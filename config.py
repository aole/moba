import json

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self._config = json.load(f)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def __getattr__(self, name):
        if name in self._config:
            # If the value is a dictionary, convert it to a Config object as well
            if isinstance(self._config[name], dict):
                return Config.from_dict(self._config[name])
            return self._config[name]
        raise AttributeError(f"'Config' object has no attribute '{name}'")

    @classmethod
    def from_dict(cls, data):
        instance = cls.__new__(cls)
        instance._config = data
        return instance

# Global instance
config = Config('config.json')
