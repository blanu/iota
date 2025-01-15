from storage import *
from noun import Noun, MetaNoun
from utils import *
import error

# Monads

# atom: Word.true

# char: unsupported

# enclose: Storage.enclose_impl

def first_impl(i):
    return i.erase().first().retype(NounType.DICTIONARY.symbol())

# floor: unsupported

# format: unimplemented FIXME

# enumerate: unsupported

# gradeDown: unsupported

# gradeUp: unsupported

# group: unsupported

# negate: unsupported

# reciprocal: unsupported

# reverse: Storage.identity

# shape: Word.zero

def size_impl(i):
    return i.erase().size()

# transpose: unsupported

# unique: unsupported

# Dyads

# cut: unsupported

# divide: unsupported

def drop_impl(i, x):
    return i.erase().drop(x).retype(NounType.DICTIONARY.symbol())

# equal: unsupported

# expand: unsupported

def find_impl(i, x):
    for pair in i.i:
        if pair.t == StorageType.MIXED_ARRAY:
            if len(pair.i) == 2:
                key = pair.i[0]
                if key.match(x) == Word.true():
                    value = pair.i[1]
                    return value
    return Word(SymbolType.undefined, o=NounType.BUILTIN_SYMBOL)

# form: unimplemented FIXME

# format2: unimplemented FIXME

# index: unsupported

# indexInDepth: unsupported

# integerDivide: unimplemented FIXME

def join_toList(i, x):
    return i.enclose().join(x.enclose())

def join_typed(i, x, c):
    if len(x.i) == 2:
        y = c(x.i[0])

        results = []
        matched = False
        for pair in i.i:
            key = pair.first()
            if key.match(y) == Word.true():
                matched = True
                results.append(x)
            else:
                results.append(pair)
        if not matched:
            results.append(x)
        return MixedArray(results)
    else:
        return join_toList(i, x)

def join_words(i, x):
    join_typed(i, x, Word)

def join_floats(i, x):
    join_typed(i, x, Float)

def join_mixed(i, x):
    join_typed(i, x, identity)

# less: unsupported

def match_dictionary(i, x):
    return i.erase().match(x.erase())

# max: unsupported

# min: unsupported

# minus: unsupported

# more: unsupported

# plus: unsupported

# power: unsupported

# reshape unimplemented FIXME

# remainder unsupported

# split unsupported

# take unsupported

# times unsupported

# Monadic Adverbs

# converge: Storage.converge_impl

def each_impl(i, f):
    return i.erase().each(f)

# eachPair: Storage.identity

# over: Storage.identity

# scanConverging: Storage.scanConverging_impl,

# scanOver: Storage.identity

# Dyadic Adverbs

# each2: unsupported

# eachLeft: unsupported

# eachRight: unsupported

# overNeutral: unsupported

# scanOverNeutral: unsupported

# scanWhileOne: Storage.scanWhileOne_impl

# whileOne: Storage.whileOne_impl

class MetaDictionary(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.DICTIONARY, StorageType.MIXED_ARRAY)] = {
            # Monads
            Monads.atom: Word.true,
            # Monads.char: unsupported
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Storage.enclose_impl,
            # Monads.enumerate: Word.enumerate_impl,
            Monads.first: first_impl,
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
            # Dyads.amend: {
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): Word.amend_impl,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): Word.amend_impl,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): Word.amend_impl,
            # },
            # Dyads.cut: unsupported
            # Dyads.divide: unsupported
            Dyads.drop: expand_dispatch(drop_impl),
            # Dyads.equal: unsupported
            # Dyads.expand: unsupported
            Dyads.find: expand_dispatch(find_impl),
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # Dyads.indexInDepth: unsupported
            # Dyads.integerDivide: unimplemented FIXME
            Dyads.join: match_dispatch(join_toList, join_toList, join_words, join_floats, join_mixed, dictionary=join_toList),
            # Dyads.less: unsupported
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): match_dictionary,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            # Dyads.more: unsupported
            # Dyads.plus: unsupported
            # Dyads.power: unsupported
            # Dyads.reshape unimplemented FIXME
            # Dyads.remainder: unsupported
            Dyads.rotate: expand_dispatch(Storage.identity),
            # Dyads.split: unsupported
            # Dyads.take unsupported
            # Dyads.times: unsupported

            # Extension Monads

            Monads.erase: MixedArray.erase_impl,
            Monads.truth: Word.false,

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_user_monad,
            },

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): MixedArray.retype_impl
            },

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_user_dyad,
            },

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: each_impl,
            MonadicAdverbs.eachPair: Storage.identity,
            MonadicAdverbs.over: Storage.identity,
            MonadicAdverbs.scanConverging: Storage.scanConverging_impl,
            MonadicAdverbs.scanOver: Storage.identity,

            # Dyadic Adverbs
            # Adverbs.each2: unsupported
            # Adverbs.eachLeft: unsupported
            # Adverbs.eachRight: unsupported
            # Adverbs.overNeutral: unsupported
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            # Adverbs.scanOverNeutral: unsupported
            DyadicAdverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            DyadicAdverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        return obj

class Dictionary(Noun, metaclass=MetaDictionary):
    @staticmethod
    def empty():
        return MixedArray([], NounType.DICTIONARY)

    @staticmethod
    def new(x):
        if x.t == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return error.Error.empty_argument()

            return MixedArray(x.i, NounType.DICTIONARY)
        else:
            return Word(error.ErrorTypes.BAD_INITIALIZATION, o=NounType.ERROR)
