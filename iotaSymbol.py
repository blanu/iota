from storage import *
from noun import Noun, MetaNoun

class MetaSymbol(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        return obj

class Symbol(Noun, metaclass=MetaSymbol):
    @staticmethod
    def new(x):
        return Word(x, NounType.USER_SYMBOL)
