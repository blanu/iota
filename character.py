import noun
from storage import *
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

# Monads.shape: Word.zero

def size_impl(i):
    return i.erase()

# Monads.transpose: unsupported

# Monads.unique: unsupported

# Dyads

# Dyads.amend: unsupported

# Dyads.cut: unsupported

# Dyads.divide: unsupported

# Dyads.drop unsupported

def equal_character(i, x):
    if i.i == x.i:
        return Word.true()
    else:
        return Word.false()

# Dyads.expand: unsupported

def find_string(i, x):
    return i.erase().find(x.erase())

# form: unimplemented FIXME

# format2: unimplemented FIXME

# index: unsupported

# indexInDepth unimplemented FIXME

# Dyads.integerDivide: unsupported

def join_scalar(i, x):
    return i.enclose().join(x.enclose())

def join_words(i, x):
    return i.enclose().join(MixedArray.from_words(x))

def join_floats(i, x):
    return i.enclose().join(MixedArray.from_floats(x))

def join_mixed(i, x):
    return i.enclose().join(x)

def join_character(i, x):
    return i.enclose().retype(NounType.STRING.symbol()).join(x.enclose().retype(NounType.STRING.symbol()))

def join_string(i, x):
    return i.enclose().retype(NounType.STRING.symbol()).join(x)

def less_character(i, x):
    return Word.erase(i).less(Word.erase(x))

def match_character(i, x):
    return Word.erase(i).match(Word.erase(x))

# Dyads.max: unsupported

# Dyads.min: unsupported

# Dyads.minus: unsupported

def more_character(i, x):
    return Word.erase(i).more(Word.erase(x))

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
    return i.enclose().retype(NounType.STRING.symbol())

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

class MetaCharacter(noun.MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        noun.Noun.dispatch[(NounType.CHARACTER, StorageType.WORD)] = {
            # Monads
            Monads.atom: Word.true,
            # Monads.char: unsupported
            Monads.complementation: Word.false,
            Monads.enclose: Storage.enclose_impl,
            # Monads.enumerate: unsupported
            Monads.first: Storage.identity,
            # Monads.floor: unsupported
            # Monads.format: unimplemented FIXME
            # Monads.gradeDown: unsupported
            # Monads.gradeUp: unsupported
            # Monads.group: unsupported
            # Monads.negate: unsupported
            # Monads.reciprocal: unsupported
            Monads.reverse: Storage.identity,
            Monads.shape: Word.zero,
            Monads.size: size_impl,
            # Monads.transpose: unsupported
            # Monads.unique: unsupported

            # Dyads
            # Dyads.amend: unsupported
            # Dyads.cut: unsupported
            # Dyads.divide: unsupported
            # Dyads.drop unsupported
            Dyads.equal: {
                (NounType.CHARACTER, StorageType.WORD): equal_character,
            },
            # Dyads.expand: unsupported
            Dyads.find: {
                (NounType.STRING, StorageType.WORD_ARRAY): find_string,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # indexInDepth unimplemented FIXME
            # Dyads.integerDivide: unsupported
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): join_scalar,
                (NounType.REAL, StorageType.FLOAT): join_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): join_mixed,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): join_scalar,
                (NounType.CHARACTER, StorageType.WORD): join_character,
                (NounType.STRING, StorageType.WORD_ARRAY): join_string,
            },
            Dyads.less: {
                (NounType.CHARACTER, StorageType.WORD): less_character,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): Word.false,
                (NounType.CHARACTER, StorageType.WORD): match_character,
                (NounType.STRING, StorageType.WORD_ARRAY): Word.false,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            Dyads.more: {
                (NounType.CHARACTER, StorageType.WORD): more_character,
            },
            # Dyads.plus: unsupported
            # Dyads.power: unsupported
            # Dyads.reshape unsupported
            # Dyads.remainder: unsupported
            # Dyads.rotate: unsupported
            # Dyads.split: unsupported
            # Dyads.take unsupported
            # Dyads.times: unsupported

            # Extension Monads

            Monads.erase: Word.erase_impl,
            Monads.truth: Word.false,

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

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: Storage.each_scalar,
            #StorageAdverbs.eachPair: unsupported
            MonadicAdverbs.over: Storage.identity,
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

        return obj

class Character(noun.Noun, metaclass=MetaCharacter):
    @staticmethod
    def new(i):
        return Word(i, NounType.CHARACTER)
