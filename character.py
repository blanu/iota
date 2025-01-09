import error
import integer
import iotaString as string
import noun
import storage

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

def size_impl(i):
    return storage.Word(i.i, o=storage.NounType.INTEGER)

# Monads.transpose: unsupported

# Monads.unique: unsupported

# Dyads

# Dyads.amend: unsupported

# Dyads.cut: unsupported

# Dyads.divide: unsupported

# Dyads.drop unsupported

def equal_character(i, x):
    if i.i == x.i:
        return storage.Word.true()
    else:
        return storage.Word.false()

# Dyads.expand: unsupported

def find_string(i, x):
    return storage.Word(i.i).find(storage.WordArray(x.i))

# form: unimplemented FIXME

# format2: unimplemented FIXME

# index: unsupported

# indexInDepth unimplemented FIXME

# Dyads.integerDivide: unsupported

def join_scalar(i, x):
    return storage.MixedArray([i, x])

def join_words(i, x):
    return storage.MixedArray([i] + [storage.Word(y) for y in x.i])

def join_floats(i, x):
    return storage.MixedArray([i] + [storage.Float(y) for y in x.i])

def join_mixed(i, x):
    return storage.MixedArray([i] + x.i)

def join_character(i, x):
    return string.String.new([i.i, x.i])

def join_string(i, x):
    return string.String.new([i.i] + x.i)

def less_character(i, x):
    return storage.Word(i.i).less(storage.Word(x.i))

def match_character(i, x):
    return storage.Word(i.i).match(storage.Word(x.i))

# Dyads.max: unsupported

# Dyads.min: unsupported

# Dyads.minus: unsupported

def more_character(i, x):
    return storage.Word(i.i).more(storage.Word(x.i))

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
    return string.String.new([i])

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

# Hot patches

def integer_word_char_impl(i):
    return Character.new(i.i)

def list_words_char_impl(i):
    return storage.MixedArray([Character.new(y) for y in i.i])

# char floats: unsupported

def list_mixed_char_impl(i):
    results = []
    for y in i.i:
        if y.t == storage.StorageType.WORD:
            result = y.char()
            if result.o == storage.NounType.ERROR:
                return result
            else:
                results.append(result)
        elif y.t == storage.StorageType.WORD_ARRAY:
            result = y.char()
            if result.o == storage.NounType.ERROR:
                return result
            else:
                results.append(result)
        elif y.t == storage.StorageType.MIXED_ARRAY:
            result = y.char()
            if result.o == storage.NounType.ERROR:
                return result
            else:
                results.append(result)
        else:
            return error.Error.unsupported_object()
    return storage.MixedArray(results)

class MetaCharacter(integer.MetaInteger, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        noun.Noun.dispatch[(storage.NounType.CHARACTER, storage.StorageType.WORD)] = {
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
            storage.Monads.size: size_impl,
            # Monads.transpose: unsupported
            # Monads.unique: unsupported

            # Dyads
            # Dyads.amend: unsupported
            # Dyads.cut: unsupported
            # Dyads.divide: unsupported
            # Dyads.drop unsupported
            storage.Dyads.equal: {
                (storage.NounType.CHARACTER, storage.StorageType.WORD): equal_character,
            },
            # Dyads.expand: unsupported
            storage.Dyads.find: {
                (storage.NounType.STRING, storage.StorageType.WORD_ARRAY): find_string,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            # Dyads.index: unsupported
            # indexInDepth unimplemented FIXME
            # Dyads.integerDivide: unsupported
            storage.Dyads.join: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): join_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): join_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): join_words,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): join_floats,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): join_mixed,
                (storage.NounType.DICTIONARY, storage.StorageType.WORD_ARRAY): join_scalar,
                (storage.NounType.CHARACTER, storage.StorageType.WORD): join_character,
                (storage.NounType.STRING, storage.StorageType.WORD_ARRAY): join_string,
            },
            storage.Dyads.less: {
                (storage.NounType.CHARACTER, storage.StorageType.WORD): less_character,
            },
            storage.Dyads.match: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Word.false,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Word.false,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Word.false,
                (storage.NounType.DICTIONARY, storage.StorageType.WORD_ARRAY): storage.Word.false,
                (storage.NounType.CHARACTER, storage.StorageType.WORD): match_character,
                (storage.NounType.STRING, storage.StorageType.WORD_ARRAY): storage.Word.false,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            storage.Dyads.more: {
                (storage.NounType.CHARACTER, storage.StorageType.WORD): more_character,
            },
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
            storage.Adverbs.each2: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Storage.each2_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Storage.each2_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Storage.each2_scalar,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Storage.each2_scalar,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Storage.each2_scalar,
            },
            storage.Adverbs.eachLeft: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Storage.eachLeft_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Storage.eachLeft_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Storage.eachLeft_words,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Storage.eachLeft_floats,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Storage.eachLeft_mixed,
            },
            storage.Adverbs.eachRight: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Storage.eachRight_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Storage.eachRight_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Storage.eachRight_words,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Storage.eachRight_floats,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Storage.eachRight_mixed,
            },
            storage.Adverbs.overNeutral: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Storage.overNeutral_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Storage.overNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Storage.overNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Storage.overNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Storage.overNeutral_scalar,
            },
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            storage.Adverbs.scanOverNeutral: {
                (storage.NounType.INTEGER, storage.StorageType.WORD): storage.Storage.scanOverNeutral_scalar,
                (storage.NounType.REAL, storage.StorageType.FLOAT): storage.Storage.scanOverNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): storage.Storage.scanOverNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): storage.Storage.scanOverNeutral_scalar,
                (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): storage.Storage.scanOverNeutral_scalar,
            },
            storage.Adverbs.scanWhileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            },
            storage.Adverbs.whileOne: {
                (storage.NounType.BUILTIN_SYMBOL, storage.StorageType.WORD): storage.Storage.whileOne_impl,
            }
        }

        return obj

class Character(integer.Integer, metaclass=MetaCharacter):
    @staticmethod
    def new(i):
        return storage.Word(i, storage.NounType.CHARACTER)
