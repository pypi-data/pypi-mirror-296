from abc import ABC, abstractmethod

class Command(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.aliases = []

    @abstractmethod
    def onExecute(self, args):
        pass

    @abstractmethod
    def onAutoComplete(self, partialCommand):
        pass
