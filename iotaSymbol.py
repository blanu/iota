from storage import *
from noun import Noun, MetaNoun

def builtin_symbol_equal_builtin_symbol(i, x):
    if i.i == x.i:
        return Word.true()
    else:
        return Word.false()

class MetaSymbol(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.BUILTIN_SYMBOL, StorageType.WORD)] = {
            # Dyads
            Dyads.equal: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): builtin_symbol_equal_builtin_symbol,
            },
        }

        return obj

class Symbol(Noun, metaclass=MetaSymbol):
    @staticmethod
    def new(x):
        return Word(x, NounType.USER_SYMBOL)
