import os
import json

import constants

class ConfigBase:
    def get(self, keys):
        config = self.get_config()
        for k in keys:
            if k in config:
                config = config[k]
        return config

    def get_config(self):
        if self.exists():
            with open(self.get_config_file()) as json_data:
                data = json.load(json_data)
                return data
        else:
            return {}

    def get_config_file(self):
        return os.path.join(os.getcwd(), constants.CONFIG_FILENAME)

    def set(self, value, keys):
        config = self.get_config()
        self.nested_set(config, keys, value)
        with open(self.get_config_file(), 'w') as out_file:
            json.dump(config, out_file, sort_keys=True, indent=4, separators=(',', ': '))

    def nested_set(self, dictionary, keys, value):
        for key in keys[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[keys[-1]] = value

    def exists(self):
        return os.path.isfile(self.get_config_file())

