from storage import *
from noun import Noun, MetaNoun
from utils import *

def truth_impl(i):
    return i.evaluate().truth()

# atom: Word.true

# complementation: Word.false

# enclose: enclose_impl

# Monads.enumerate: unsupported

# Monads.first: identity

# Monads.floor: unsupported

# Monads.format: unimplemented FIXME

# Monads.gradeDown: unsupported

# Monads.gradeUp: unsupported

# Monads.group: unsupported

# Monads.negate: unsupported

# Monads.reciprocal: unsupported

# Monads.reverse: identity

# Monads.shape: Word.zero

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
    return i.enclose().join(x.enclose())

# Dyads.less: unsupported

def match_function(i, x):
    if i.o == x.o:
        return i.erase().match(x.erase())
    else:
        return Word.false()

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

# converge: converge_impl

# each: each_scalar

# eachPair: unsupported

# over: identity

# scanConverging: scanConverging_impl

def scanOver_impl(i, f):
    return i.enclose()

# Dyadic Adverbs

# each2: each2_scalar

# eachLeft word: eachLeft_scalar
# eachLeft float: eachLeft_scalar
# eachLeft words: eachLeft_words
# eachLeft floats: eachLeft_floats
# eachLeft mixed: eachLeft_mixed

# eachRight word: eachRight_scalar
# eachRight float: eachRight_scalar
# eachRight words: eachRight_words
# eachRight floats: eachRight_floats
# eachRight mixed: eachRight_mixed

# overNeutral_impl

# iterate: iterate_word
# iterate float, words, floats, mixed: unsupported

# scanIterating: scanIterating_word
# scanIterating: float, words, floats, mixed - unsupported

# scanOverNeutral: scanOverNeutral_scalar

# scanWhileOne: scanWhileOne_impl

# whileOne: whileOne

class MetaExpression(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.EXPRESSION, StorageType.MIXED_ARRAY)] = {
            Monads.evaluate: Storage.evaluate_impl,
            Monads.truth: truth_impl,

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_expression,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_expression,
            },

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_expression,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_expression,
            },
        }

        return obj

class Expression(Noun, metaclass=MetaExpression):
    @staticmethod
    def new(i):
        return MixedArray(i, o=NounType.EXPRESSION)

class MetaFunction(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        dispatch_table = {
            # Monads
            Monads.atom: Word.true,
            # Monads.char: unsupported
            Monads.complementation: Word.false,
            Monads.enclose: Storage.enclose_impl,
            # Monads.enumerate: unsupported
            Monads.first: identity,
            # Monads.floor: unsupported
            # Monads.format: unimplemented FIXME
            # Monads.gradeDown: unsupported
            # Monads.gradeUp: unsupported
            # Monads.group: unsupported
            # Monads.negate: unsupported
            # Monads.reciprocal: unsupported
            Monads.reverse: identity,
            Monads.shape: Word.zero,
            # Monads.size: unsupported
            # Monads.transpose: unsupported
            # Monads.unique: unsupported

            # Dyads
            # Dyads.amend: unsupported
            # Dyads.cut: unsupported
            # Dyads.divide: unsupported
            # Dyads.drop unsupported
            # Dyads.equal: unsupported
            # Dyads.expand: unsupported
            # Dyads.find: unsupported
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # indexInDepth unimplemented FIXME
            # Dyads.integerDivide: unsupported
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): join_impl,
                (NounType.REAL, StorageType.FLOAT): join_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): join_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): join_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): join_impl,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): join_impl,
                (NounType.CHARACTER, StorageType.WORD): join_impl,
                (NounType.STRING, StorageType.WORD_ARRAY): join_impl,
            },
            # Dyads.less: unsupported
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): Word.false,
                (NounType.CHARACTER, StorageType.WORD): Word.false,
                (NounType.STRING, StorageType.WORD_ARRAY): Word.false,
                # (NounType.EXPRESSION, StorageType.WORD_ARRAY): match_function,
                (NounType.USER_MONAD, StorageType.WORD_ARRAY): match_function,
                (NounType.USER_DYAD, StorageType.WORD_ARRAY): match_function,
                (NounType.USER_TRIAD, StorageType.WORD_ARRAY): match_function,
            },
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

            # Extension Monads

            Monads.erase: MixedArray.erase_impl,
            Monads.truth: Word.false,

            # Extension Dyads

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): MixedArray.retype_impl
            },

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: Storage.each_scalar,
            #StorageAdverbs.eachPair: unsupported
            MonadicAdverbs.over: identity,
            MonadicAdverbs.scanConverging: Storage.scanConverging_impl,
            MonadicAdverbs.scanOver: scanOver_impl,

            # Dyadic Adverbs
            DyadicAdverbs.each2: expand_dispatch(Storage.each2_scalar),
            DyadicAdverbs.eachLeft: match_dispatch(Storage.eachLeft_scalar, Storage.eachLeft_scalar, Storage.eachLeft_words, Storage.eachLeft_floats, Storage.eachLeft_mixed),
            DyadicAdverbs.eachRight: match_dispatch(Storage.eachRight_scalar, Storage.eachRight_scalar, Storage.eachRight_words, Storage.eachRight_floats, Storage.eachRight_mixed),
            DyadicAdverbs.overNeutral: expand_dispatch(Storage.overNeutral_scalar),
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            DyadicAdverbs.scanOverNeutral: expand_dispatch(Storage.scanOverNeutral_scalar),
            DyadicAdverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            DyadicAdverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }
        # dispatch[(NounType.EXPRESSION, StorageType.MIXED_ARRAY)] = dispatch_table
        Noun.dispatch[(NounType.USER_MONAD, StorageType.MIXED_ARRAY)] = dispatch_table
        Noun.dispatch[(NounType.USER_DYAD, StorageType.MIXED_ARRAY)] = dispatch_table
        Noun.dispatch[(NounType.USER_TRIAD, StorageType.MIXED_ARRAY)] = dispatch_table

        return obj

class Function(Noun, metaclass=MetaFunction):
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
            return MixedArray(i, NounType.USER_TRIAD)
        elif hasX:
            return MixedArray(i, NounType.USER_DYAD)
        elif hasI:
            return MixedArray(i, NounType.USER_MONAD)
        else:
            return MixedArray(i, NounType.EXPRESSION)
