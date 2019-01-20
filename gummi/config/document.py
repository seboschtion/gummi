import gummi
from gummi.config import Base

class Document(Base):
    def __init__(self):
        super().__init__(gummi.constants.CONFIG_FILENAME)

    def create(self):
        self.set([], ["packages"])
        self.set({}, ["template"])

