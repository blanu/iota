from storage import *
from noun import Noun, MetaNoun
import character

# atom: Storage.atom_list

# char: unsupported

# complementation: unsupported

# enclose: Storage.enclose_impl

# enumerate: unsupported

# expand: unimplemented FIXME

def first_impl(i):
    untyped = WordArray(i.i)
    untypedResult = untyped.first()
    if untypedResult.o == NounType.ERROR:
        return untypedResult

    return character.Character.new(untypedResult.i)

# floor: Storage.identity,

# format: unimplemented FIXME

# gradeDown: WordArray.gradeDown_impl

# gradeUp: WordArray.gradeUp_impl

# group WordArray.group_impl unimplemented FIXME

# negate: unsupported

# reciprocal: unsupported

def reverse_impl(i):
    untyped = WordArray(i.i)
    untypedResult = untyped.reverse()
    return String.new(untypedResult)

# shape: WordArray.shape_impl

# size: WordArray.size_impl

# transpose: Storage.identity

def unique_impl(i):
    untyped = WordArray(i.i)
    untypedResult = untyped.unique()
    return String.new(untypedResult)

# Dyads

# amend: unimplemented FIXME

def cut_impl(i, x):
    untyped = WordArray(i.i)
    untypedResult = untyped.cut(x)
    if untypedResult.o == NounType.ERROR:
        return untypedResult
    else:
        return MixedArray([String.new(y) for y in untypedResult.i])

# divide: unsupported

def drop_word(i, x):
    untyped = WordArray(i.i)
    untypedResult = untyped.drop(x)
    if untypedResult.o == NounType.ERROR:
        return untypedResult
    else:
        return String.new(untypedResult.i)
# drop float, words, floats, mixed: unsupported

# equal word, float, words, floats, mixed: Word.false
def equal_string(i, x):
    ui = WordArray(i.i)
    ux = WordArray(x.i)
    return ui.equal(ux)

def find_character(i, x):
    ui = WordArray(i.i)
    ux = Word(x.i)
    return ui.find(ux)

# unimplemented FIXME
def find_string(i, x):
    pass

# form: unimplemented FIXME

# format2: unimplemented FIXME

def index_impl(i, x):
    untyped = WordArray(i.i)
    untypedResult = untyped.index(x)
    if untypedResult.o == NounType.ERROR:
        return untypedResult
    else:
        return String.new(untypedResult.i)

# indexInDepth: unimplemented FIXME

# integerDivide: unsupported

def join_toList(i, x):
    return MixedArray([i, x])

def join_character(i, x):
    return String.new(i.i + [x.i])

def join_string(i, x):
    return String.new(i.i + x.i)

# FIXME
def join_dictionary(i, x):
    pass

def less_string(i, x):
    ui = WordArray(i.i)
    ux = WordArray(x.i)
    return ui.less(ux)

# FIXME
def match_mixed(i, x):
    pass

def match_string(i, x):
    ui = WordArray(i.i)
    ux = WordArray(x.i)
    return ui.match(ux)

# Dyads.max: unsupported

# Dyads.min: unsupported

# Dyads.minus: unsupported

def more_string(i, x):
    ui = WordArray(i.i)
    ux = WordArray(x.i)
    return ui.more(ux)

# FIXME Dyads.reshape unimplemented

# Dyads.remainder: unsupported

def rotate_word(i, x):
    ui = WordArray(i.i)
    ux = Word(x.i)
    ur = ui.rotate(ux)
    return String.new(ur.i)

def split_impl(i, x):
    ui = WordArray(i.i)
    ur = ui.split(x)
    return MixedArray([String.new(y) for y in ur.i])

def take_impl(i, x):
    ui = WordArray(i.i)
    ur = ui.take(x)
    return String.new(ur.i)

# times: unsupported

# Monadic adverbs

# Adverbs.converge: Storage.converge_impl,

def each_impl(i, f):
    return MixedArray([Noun.dispatchMonad(character.Character.new(y), f) for y in i.i])

def eachPair_impl(i, f):
    results = []
    for index, y in enumerate(i.i):
        if index != len(i.i) - 1:
            z = i.i[index + 1]
            results.append(Noun.dispatchDyad(character.Character.new(y), f, Word(z)))
    return MixedArray(results)


def over_impl(i, f):
    if len(i.i) == 0:
        return i
    elif len(i.i) == 1:
        return i
    else:
        accumulator = 0
        for index, y in enumerate(i.i):
            if index == 0:
                accumulator = character.Character.new(y)
            else:
                accumulator = Noun.dispatchDyad(accumulator, f, character.Character.new(y))
        return accumulator


# Adverbs.scanConverging: Storage.scanConverging_impl,

def scanOver_impl(i, f):
    if len(i.i) == 0:
        return String.new([])
    else:
        current = character.Character.new(i.i[0])
        rest = i.i[1:]
        results = [current]
        for y in rest:
            current = Noun.dispatchDyad(current, f, character.Character.new(y))
            results.append(current)
        return MixedArray(results)

# Dyadic adverbs

def each2_scalar(i, f, x):
    return MixedArray([Noun.dispatchDyad(character.Character.new(y), f, x) for y in i.i])

def each2_words(i, f, x):
    results = []
    #FIXME - make this work for arrays on unequal lengths
    for y, z in zip([character.Character.new(y) for y in i.i], [Word(z) for z in x.i]):
        results.append(Noun.dispatchDyad(y, f, z))
    return MixedArray(results)

def each2_floats(i, f, x):
    results = []
    #FIXME - make this work for arrays on unequal lengths
    for y, z in zip([character.Character.new(y) for y in i.i], [Float(z) for z in x.i]):
        results.append(Noun.dispatchDyad(y, f, z))
    return MixedArray(results)

def each2_mixed(i, f, x):
    results = []
    #FIXME - make this work for arrays on unequal lengths
    for y, z in zip([character.Character.new(y) for y in i.i], [z for z in x.i]):
        results.append(Noun.dispatchDyad(y, f, z))
    return MixedArray(results)

def each2_string(i, f, x):
    results = []
    #FIXME - make this work for arrays on unequal lengths
    for y, z in zip([character.Character.new(y) for y in i.i], [character.Character.new(z) for z in x.i]):
        results.append(Noun.dispatchDyad(y, f, z))
    return MixedArray(results)

# eachLeft word: Storage.eachLeft_scalar
# eachLeft float: Storage.eachLeft_scalar
# eachLeft words: Storage.eachLeft_words
# eachLeft floats: Storage.eachLeft_floats
# eachLeft mixed: Storage.eachLeft_mixed
def eachLeft_string(i, f, x):
    return MixedArray([Noun.dispatchDyad(i, f, character.Character.new(y)) for y in x.i])

# eachRight word: Storage.eachRight_scalar
# eachRight float: Storage.eachRight_scalar
# eachRight words: Storage.eachRight_words
# eachRight floats: Storage.eachRight_floats
# eachRight mixed: Storage.eachRight_mixed
def eachRight_string(i, f, x):
    return MixedArray([Noun.dispatchDyad(character.Character.new(y), f, i) for y in x.i])

def overNeutral_impl(i, f, x):
    if len(i.i) == 0:
        return error.Error.empty_argument()
    else:
        accumulator = x
        for index, y in enumerate(i.i):
            accumulator = Noun.dispatchDyad(accumulator, f, character.Character.new(y))
        return accumulator

# iterate: Storage.iterate_word

# scanIterating: Storage.scanIterating_word

def scanOverNeutral_impl(i, f, x):
    current = x
    results = [current]
    for y in i.i:
        current = Noun.dispatchDyad(current, f, character.Character.new(y))
        results.append(current)
    return MixedArray(results)

# scanWhileOne: Storage.scanWhileOne_impl

# whileOne: Storage.whileOne_impl

class MetaString(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.STRING, StorageType.WORD_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            # Monads.char: unsupported
            # Monads.complementation: unsupported
            Monads.enclose: Storage.enclose_impl,
            # Monads.enumerate: unsupported
            # Monads.expand: unimplemented FIXME
            Monads.first: first_impl,
            Monads.floor: Storage.identity,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: WordArray.gradeDown_impl,
            Monads.gradeUp: WordArray.gradeUp_impl,
            # Monads.group: WordArray.group_impl unimplemented FIXME
            # Monads.negate: unsupported
            # Monads.reciprocal: unsupported
            Monads.reverse: WordArray.reverse_impl,
            Monads.shape: WordArray.shape_impl,
            Monads.size: WordArray.size_impl,
            Monads.transpose: Storage.identity,
            Monads.unique: unique_impl,

            # Dyads
            #
            # Dyads.amend: { FIXME
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): WordArray.amend_words,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.amend_floats,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.amend_mixed,
            # },
            Dyads.cut: {
                (NounType.INTEGER, StorageType.WORD): cut_impl,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): cut_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): cut_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): cut_impl,
            },
            # Dyads.divide: unsupported
            Dyads.drop: {
                (NounType.INTEGER, StorageType.WORD): drop_word,
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): Word.false,
                (NounType.CHARACTER, StorageType.WORD): Word.false,
                (NounType.STRING, StorageType.WORD_ARRAY): equal_string,
            },
            Dyads.find: {
                (NounType.CHARACTER, StorageType.WORD): find_character,
                (NounType.STRING, StorageType.WORD_ARRAY): find_string,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                (NounType.INTEGER, StorageType.WORD): index_impl,
                (NounType.REAL, StorageType.FLOAT): index_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): index_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): index_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): index_impl,
            },
            # indexInDepth: unimplemented FIXME
            # Dyads.integerDivide: unsupported
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): join_toList,
                (NounType.REAL, StorageType.FLOAT): join_toList,
                (NounType.LIST, StorageType.WORD_ARRAY): join_toList,
                (NounType.LIST, StorageType.FLOAT_ARRAY): join_toList,
                (NounType.LIST, StorageType.MIXED_ARRAY): join_toList,
                (NounType.CHARACTER, StorageType.WORD): join_character,
                (NounType.STRING, StorageType.WORD_ARRAY): join_string,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): WordArray.join_dictionary,
            },
            Dyads.less: {
                (NounType.STRING, StorageType.WORD_ARRAY): less_string,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): match_mixed,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): Word.false,
                (NounType.STRING, StorageType.WORD_ARRAY): match_string,
            },
            # Dyads.max: unsupported
            # Dyads.min: unsupported
            # Dyads.minus: unsupported
            Dyads.more: {
                (NounType.STRING, StorageType.WORD_ARRAY): more_string,
            },
            # Dyads.plus: unsupported
            # Dyads.power: unsupported
            # FIXME Dyads.reshape unimplemented
            # Dyads.remainder: unsupported
            Dyads.rotate: {
                (NounType.INTEGER, StorageType.WORD): WordArray.rotate_word
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.split: {
                (NounType.INTEGER, StorageType.WORD): split_impl,
                (NounType.REAL, StorageType.FLOAT): split_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): split_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): split_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): split_impl,
            },
            Dyads.take: {
                (NounType.INTEGER, StorageType.WORD): take_impl,
                (NounType.REAL, StorageType.FLOAT): take_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): take_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): take_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): take_impl,
            },
            # Dyads.times: unsupported

            Dyads.apply: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.apply_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.apply_user_monad,
            },

            Triads.apply: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.apply_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.apply_user_dyad,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: each_impl,
            Adverbs.eachPair: eachPair_impl,
            Adverbs.over: over_impl,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): each2_scalar,
                (NounType.REAL, StorageType.FLOAT): each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): each2_mixed,
                (NounType.CHARACTER, StorageType.WORD): each2_scalar,
                (NounType.STRING, StorageType.WORD_ARRAY): each2_string,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
                (NounType.CHARACTER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.STRING, StorageType.WORD_ARRAY): eachLeft_string,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
                (NounType.CHARACTER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.STRING, StorageType.WORD_ARRAY): eachRight_string,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): overNeutral_impl,
                (NounType.CHARACTER, StorageType.WORD): overNeutral_impl,
                (NounType.STRING, StorageType.WORD_ARRAY): overNeutral_impl,
            },
            Adverbs.iterate: {
                (NounType.INTEGER, StorageType.WORD): Storage.iterate_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            Adverbs.scanIterating: {
                (NounType.INTEGER, StorageType.WORD): Storage.scanIterating_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            Adverbs.scanOverNeutral: {
                (NounType.INTEGER, StorageType.WORD): scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): scanOverNeutral_impl,
                (NounType.CHARACTER, StorageType.WORD): scanOverNeutral_impl,
                (NounType.STRING, StorageType.WORD_ARRAY): scanOverNeutral_impl,
            },
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        return obj

class String(Noun, metaclass=MetaString):
    @staticmethod
    def empty():
        return String.new([])

    @staticmethod
    def new(i: [int]):
        for y in i:
            if not type(y) is int:
                return error.Error.unsupported_object()
        return WordArray(i, NounType.STRING)
