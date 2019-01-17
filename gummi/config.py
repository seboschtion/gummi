import os
import json

import constants

class Config:
    def get_source_url(self):
        return self.get(["source", "url"])

    def set_source_url(self, value):
        self.set(value, ["source", "url"])

    def get_source_name(self):
        return self.get(["source", "name"])

    def set_source_name(self, value):
        self.set(value, ["source", "name"])

    def get_build_start(self):
        return self.get(["build", "start"])

    def get(self, keys):
        config = self.config()
        for k in keys:
            if k in config:
                config = config[k]
        return config

    def config(self):
        if self.exists():
            with open(self.get_config_file()) as json_data:
                data = json.load(json_data)
                return data
        else:
            return {}

    def set(self, value, keys):
        config = self.config()
        self.nested_set(config, keys, value)
        with open(self.get_config_file(), 'w') as out_file:
            json.dump(config, out_file, sort_keys=True, indent=4, separators=(',', ': '))

    def nested_set(self, dictionary, keys, value):
        for key in keys[:-1]:
            dictionary = dictionary.setdefault(key, {})
        dictionary[keys[-1]] = value

    def exists(self):
        return os.path.isfile(self.get_config_file())

    def get_config_file(self):
        return os.path.join(os.getcwd(), constants.CONFIG_FILENAME)

