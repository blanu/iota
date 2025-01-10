import error
import iotaSymbol as symbol
from noun import Noun, MetaNoun
from utils import *

# Monads

# atom: Word.true

# char: unsupported

# enclose: Storage.enclose_impl

def first_impl(i):
    untyped = storage.WordArray(i.i)
    untypedResult = untyped.first()
    return Dictionary.new(untypedResult)

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
    return len(i.i)

# transpose: unsupported

# unique: unsupported

# Dyads

# cut: unsupported

# divide: unsupported

def drop_impl(i, x):
    untyped = storage.WordArray(i.i)
    untypedResult = untyped.drop(x)
    return Dictionary.new(untypedResult)


# equal: unsupported

# expand: unsupported

def find_impl(i, x):
    for pair in i.i:
        if pair.t == storage.StorageType.MIXED_ARRAY:
            if len(pair.i) == 2:
                key = pair.i[0]
                if key.match(x) == storage.Word.true():
                    value = pair.i[1]
                    return value
    return symbol.Symbol.undefined.symbol()


# form: unimplemented FIXME

# format2: unimplemented FIXME

# index: unsupported

# indexInDepth: unsupported

# integerDivide: unimplemented FIXME

def join_toList(i, x):
    return storage.MixedArray([i, x])

def join_typed(i, x, c):
    if len(x.i) == 2:
        y = c(x.i[0])

        results = []
        matched = False
        for pair in i.i:
            key = pair.first()
            if key.match(y) == storage.Word.true():
                matched = True
                results.append(x)
            else:
                results.append(pair)
        if not matched:
            results.append(x)
        return storage.MixedArray(results)
    else:
        return join_toList(i, x)

def join_words(i, x):
    join_typed(i, x, storage.Word)

def join_floats(i, x):
    join_typed(i, x, storage.Float)

def join_mixed(i, x):
    join_typed(i, x, identity)

# less: unsupported

def match_dictionary(i, x):
    y = storage.MixedArray(i.i)
    z = storage.MixedArray(x.i)
    return y.match(z)


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
    untyped = storage.WordArray(i.i)
    return untyped.each(f)


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

        Noun.dispatch[(storage.NounType.DICTIONARY, storage.StorageType.MIXED_ARRAY)] = {
            # Monads
            storage.Monads.atom: storage.Word.true,
            # Monads.char: unsupported
            storage.Monads.complementation: storage.Storage.complementation_impl,
            storage.Monads.enclose: storage.Storage.enclose_impl,
            # Monads.enumerate: Word.enumerate_impl,
            storage.Monads.first: first_impl,
            # Monads.floor: unsupported
            # Monads.format: unimplemented FIXME
            # Monads.gradeDown: unsupported
            # Monads.gradeUp: unsupported
            # Monads.group: unsupported
            # Monads.negate: unsupported
            # Monads.reciprocal: unsupported
            storage.Monads.reverse: storage.Storage.identity,
            storage.Monads.shape: storage.Word.zero,
            storage.Monads.size: size_impl,
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
            storage.Dyads.drop: expand_dispatch(drop_impl),
            # Dyads.equal: unsupported
            # Dyads.expand: unsupported
            storage.Dyads.find: expand_dispatch(find_impl),
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # Dyads.indexInDepth: unsupported
            # Dyads.integerDivide: unimplemented FIXME
            storage.Dyads.join: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): join_toList,
                (storage.NounType.REAL, storage.StorageType.FLOAT): join_toList,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): join_words,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): join_floats,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): join_mixed,
                (storage.NounType.DICTIONARY, storage.StorageType.MIXED_ARRAY): join_toList,
            },
            # Dyads.less: unsupported
            storage.Dyads.match: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Word.false,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Word.false,
                (storage.NounType.DICTIONARY, storage.StorageType.MIXED_ARRAY): match_dictionary,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            # Dyads.more: unsupported
            # Dyads.plus: unsupported
            # Dyads.power: unsupported
            # Dyads.reshape unimplemented FIXME
            # Dyads.remainder: unsupported
            storage.Dyads.rotate: expand_dispatch(storage.Storage.identity),
            # Dyads.split: unsupported
            # Dyads.take unsupported
            # Dyads.times: unsupported

            storage.Dyads.apply: {
                (storage.NounType.BUILTIN_MONAD, storage.StorageType.WORD): storage.Storage.apply_builtin_monad,
                (storage.NounType.USER_MONAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_user_monad,
            },

            storage.Triads.apply: {
                (storage.NounType.BUILTIN_DYAD, storage.StorageType.WORD): storage.Storage.apply_builtin_dyad,
                (storage.NounType.USER_DYAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_user_dyad,
            },

            # Monadic Adverbs
            storage.Adverbs.converge: storage.Storage.converge_impl,
            storage.Adverbs.each: each_impl,
            storage.Adverbs.eachPair: storage.Storage.identity,
            storage.Adverbs.over: storage.Storage.identity,
            storage.Adverbs.scanConverging: storage.Storage.scanConverging_impl,
            storage.Adverbs.scanOver: storage.Storage.identity,

            # Dyadic Adverbs
            # Adverbs.each2: unsupported
            # Adverbs.eachLeft: unsupported
            # Adverbs.eachRight: unsupported
            # Adverbs.overNeutral: unsupported
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            # Adverbs.scanOverNeutral: unsupported
            storage.Adverbs.scanWhileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            },
            storage.Adverbs.whileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            }
        }

        return obj

class Dictionary(Noun, metaclass=MetaDictionary):
    @staticmethod
    def empty():
        return storage.MixedArray([], storage.NounType.DICTIONARY)

    @staticmethod
    def new(x):
        if x.t == storage.StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return error.Error.empty_argument()

            return storage.MixedArray(x.i, storage.NounType.DICTIONARY)
        else:
            return error.Error.bad_initialization()
