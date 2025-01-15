import error
from storage import *
from noun import Noun, MetaNoun
from utils import *

def evaluate_impl(e):
    if len(e.i) != 3:
        return Word(error.ErrorTypes.SHAPE_MISMATCH, o=NounType.ERROR)

    a = e.i[0]
    b = e.i[1]
    c = e.i[2]

    if a.truth() == Word.true():
        return b.evaluate()
    else:
        return c.evaluate()

def truth_impl(i):
    return i.evaluate().truth()

class MetaConditional(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.CONDITIONAL, StorageType.MIXED_ARRAY)] = {
            Monads.evaluate: evaluate_impl,
            Monads.truth: truth_impl,

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_expression,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_expression,
            },

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_expression,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_expression,
            },

            # Extension Monads

            Monads.erase: MixedArray.erase_impl,

            # Extension Dyads

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): MixedArray.retype_impl
            },
        }

        return obj

class Conditional(Noun, metaclass=MetaConditional):
    @staticmethod
    def new(i):
        return MixedArray(i, o=NounType.EXPRESSION)
