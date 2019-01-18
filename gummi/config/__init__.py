from gummi.config.config_base import ConfigBase

class Config(ConfigBase):
    def init(self):
        self.set([], ["packages"])
        self.set({}, ["template"])
        

