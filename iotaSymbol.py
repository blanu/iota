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

            # Extension Monads

            Monads.erase: Word.erase_impl,

            # Extension Dyads

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_user_monad,
            },

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): Word.retype_impl
            },

            # Extension Triads

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_user_dyad,
            },
        }

        return obj

class Symbol(Noun, metaclass=MetaSymbol):
    @staticmethod
    def new(x):
        return Word(x, NounType.USER_SYMBOL)
