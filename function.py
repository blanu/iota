import noun
from storage import NounType, SymbolType, Word, WordArray, MixedArray, Dyads, Triads
from utils import *

# atom: Word.true

# complementation: Word.false

# enclose: Storage.enclose_impl

# Monads.enumerate: unsupported

# Monads.first: Storage.identity

# Monads.floor: unsupported

# Monads.format: unimplemented FIXME

# Monads.gradeDown: unsupported

# Monads.gradeUp: unsupported

# Monads.group: unsupported

# Monads.negate: unsupported

# Monads.reciprocal: unsupported

# Monads.reverse: Storage.identity

# Monads.shape: storage.Word.zero

# Monads.size: unsupported

# Monads.transpose: unsupported

# Monads.unique: unsupported

# Dyads

# Dyads.amend: unsupported

# Dyads.cut: unsupported

# Dyads.divide: unsupported

# Dyads.drop unsupported

# Dyads.equal unsupported

# Dyads.expand: unsupported

# Dyads.find: unsupported

# form: unimplemented FIXME

# format2: unimplemented FIXME

# index: unsupported

# indexInDepth unimplemented FIXME

# Dyads.integerDivide: unsupported

def join_impl(i, x):
    return storage.MixedArray([i, x])

# Dyads.less: unsupported

def match_function(i, x):
    if i.o == x.o:
        ui = WordArray(i.i)
        ux = WordArray(x.i)
        return ui.match(ux)
    else:
        return storage.Word.false()

# Dyads.max: unsupported

# Dyads.min: unsupported

# Dyads.minus: unsupported

# Dyads.more: unsupported

# Dyads.plus: unsupported

# Dyads.power: unsupported

# Dyads.reshape unsupported

# Dyads.remainder: unsupported

# Dyads.rotate: unsupported

# Dyads.split: unsupported

# Dyads.take unsupported

# Dyads.times: unsupported

# Monadic Adverbs

# converge: Storage.converge_impl

# each: Storage.each_scalar

# eachPair: unsupported

# over: Storage.identity

# scanConverging: Storage.scanConverging_impl

def scanOver_impl(i, f):
    return MixedArray([i])

# Dyadic Adverbs

# each2: Storage.each2_scalar

# eachLeft word: Storage.eachLeft_scalar
# eachLeft float: Storage.eachLeft_scalar
# eachLeft words: Storage.eachLeft_words
# eachLeft floats: Storage.eachLeft_floats
# eachLeft mixed: Storage.eachLeft_mixed

# eachRight word: Storage.eachRight_scalar
# eachRight float: Storage.eachRight_scalar
# eachRight words: Storage.eachRight_words
# eachRight floats: Storage.eachRight_floats
# eachRight mixed: Storage.eachRight_mixed

# Storage.overNeutral_impl

# iterate: Storage.iterate_word
# iterate float, words, floats, mixed: unsupported

# scanIterating: Storage.scanIterating_word
# scanIterating: float, words, floats, mixed - unsupported

# scanOverNeutral: Storage.scanOverNeutral_scalar

# scanWhileOne: Storage.scanWhileOne_impl

# whileOne: Storage.whileOne

class MetaExpression(noun.MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        noun.Noun.dispatch[(NounType.EXPRESSION, storage.StorageType.MIXED_ARRAY)] = {
            storage.Monads.evaluate: storage.Storage.evaluate_impl,

            Dyads.apply: {
                (storage.NounType.BUILTIN_MONAD, storage.StorageType.WORD): storage.Storage.apply_monad_expression,
                (storage.NounType.USER_MONAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_monad_expression,
            },

            Triads.apply: {
                (storage.NounType.BUILTIN_DYAD, storage.StorageType.WORD): storage.Storage.apply_dyad_expression,
                (storage.NounType.USER_DYAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_dyad_expression,
            },
        }

        return obj

class Expression(noun.Noun, metaclass=MetaExpression):
    @staticmethod
    def new(i):
        return MixedArray(i, o=NounType.EXPRESSION)

class MetaFunction(noun.MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        dispatch_table = {
            # Monads
            storage.Monads.atom: storage.Word.true,
            # Monads.char: unsupported
            storage.Monads.complementation: storage.Word.false,
            storage.Monads.enclose: storage.Storage.enclose_impl,
            # Monads.enumerate: unsupported
            storage.Monads.first: storage.Storage.identity,
            # Monads.floor: unsupported
            # Monads.format: unimplemented FIXME
            # Monads.gradeDown: unsupported
            # Monads.gradeUp: unsupported
            # Monads.group: unsupported
            # Monads.negate: unsupported
            # Monads.reciprocal: unsupported
            storage.Monads.reverse: storage.Storage.identity,
            storage.Monads.shape: storage.Word.zero,
            # storage.Monads.size: unsupported
            # Monads.transpose: unsupported
            # Monads.unique: unsupported

            # Dyads
            # Dyads.amend: unsupported
            # Dyads.cut: unsupported
            # Dyads.divide: unsupported
            # Dyads.drop unsupported
            # storage.Dyads.equal: unsupported
            # Dyads.expand: unsupported
            # storage.Dyads.find: unsupported
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # indexInDepth unimplemented FIXME
            # Dyads.integerDivide: unsupported
            storage.Dyads.join: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): join_impl,
                (storage.NounType.REAL, storage.StorageType.FLOAT): join_impl,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): join_impl,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): join_impl,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): join_impl,
                (storage.NounType.DICTIONARY, storage.StorageType.WORD_ARRAY): join_impl,
                (storage.NounType.CHARACTER, storage.StorageType.WORD): join_impl,
                (storage.NounType.STRING, storage.StorageType.WORD_ARRAY): join_impl,
            },
            # storage.Dyads.less: unsupported
            storage.Dyads.match: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Word.false,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Word.false,
                (storage.NounType.DICTIONARY, storage.StorageType.WORD_ARRAY): storage.Word.false,
                (storage.NounType.CHARACTER, storage.StorageType.WORD): storage.Word.false,
                (storage.NounType.STRING, storage.StorageType.WORD_ARRAY): storage.Word.false,
                # (storage.NounType.EXPRESSION, storage.StorageType.WORD_ARRAY): match_function,
                (storage.NounType.USER_MONAD, storage.StorageType.WORD_ARRAY): match_function,
                (storage.NounType.USER_DYAD, storage.StorageType.WORD_ARRAY): match_function,
                (storage.NounType.USER_TRIAD, storage.StorageType.WORD_ARRAY): match_function,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            # storage.Dyads.more: unsupported
            # Dyads.plus: unsupported
            # Dyads.power: unsupported
            # Dyads.reshape unsupported
            # Dyads.remainder: unsupported
            # Dyads.rotate: unsupported
            # Dyads.split: unsupported
            # Dyads.take unsupported
            # Dyads.times: unsupported

            # Monadic Adverbs
            storage.Adverbs.converge: storage.Storage.converge_impl,
            storage.Adverbs.each: storage.Storage.each_scalar,
            #StorageAdverbs.eachPair: unsupported
            storage.Adverbs.over: storage.Storage.identity,
            storage.Adverbs.scanConverging: storage.Storage.scanConverging_impl,
            storage.Adverbs.scanOver: scanOver_impl,

            # Dyadic Adverbs
            storage.Adverbs.each2: expand_dispatch(storage.Storage.each2_scalar),
            storage.Adverbs.eachLeft: match_dispatch(storage.Storage.eachLeft_scalar, storage.Storage.eachLeft_scalar, storage.Storage.eachLeft_words, storage.Storage.eachLeft_floats, storage.Storage.eachLeft_mixed),
            storage.Adverbs.eachRight: match_dispatch(storage.Storage.eachRight_scalar, storage.Storage.eachRight_scalar, storage.Storage.eachRight_words, storage.Storage.eachRight_floats, storage.Storage.eachRight_mixed),
            storage.Adverbs.overNeutral: expand_dispatch(storage.Storage.overNeutral_scalar),
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            storage.Adverbs.scanOverNeutral: expand_dispatch(storage.Storage.scanOverNeutral_scalar),
            storage.Adverbs.scanWhileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            },
            storage.Adverbs.whileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            }
        }
        # noun.Noun.dispatch[(storage.NounType.EXPRESSION, storage.StorageType.MIXED_ARRAY)] = dispatch_table
        noun.Noun.dispatch[(storage.NounType.USER_MONAD, storage.StorageType.MIXED_ARRAY)] = dispatch_table
        noun.Noun.dispatch[(storage.NounType.USER_DYAD, storage.StorageType.MIXED_ARRAY)] = dispatch_table
        noun.Noun.dispatch[(storage.NounType.USER_TRIAD, storage.StorageType.MIXED_ARRAY)] = dispatch_table

        return obj

class Function(noun.Noun, metaclass=MetaFunction):
    @staticmethod
    def new(i):
        hasI = False
        hasX = False
        hasY = False
        for y in i:
            if y.o == NounType.BUILTIN_SYMBOL:
                if y.equal(SymbolType.i.symbol()) == Word.true():
                    hasI = True
                if y.equal(SymbolType.x.symbol()) == Word.true():
                    hasX = True
                if y.equal(SymbolType.y.symbol()) == Word.true():
                    hasY = True
        if hasY:
            return storage.MixedArray(i, storage.NounType.USER_TRIAD)
        elif hasX:
            return storage.MixedArray(i, storage.NounType.USER_DYAD)
        elif hasI:
            return storage.MixedArray(i, storage.NounType.USER_MONAD)
        else:
            return storage.MixedArray(i, storage.NounType.EXPRESSION)
