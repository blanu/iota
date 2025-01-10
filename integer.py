from storage import *
from noun import Noun, MetaNoun
from utils import *

class MetaInteger(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.INTEGER, StorageType.WORD)] = {
            # Monads
            Monads.atom: Word.true,
            # Monads.char: hotpatched by character.py to avoid circular imports
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Word.enclose_impl,
            Monads.enumerate: Word.enumerate_impl,
            Monads.first: Storage.identity,
            Monads.floor: Storage.identity,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: Storage.identity,
            Monads.gradeUp: Storage.identity,
            #Monads.group: unsupported
            Monads.negate: Storage.negate_impl,
            Monads.reciprocal: Storage.reciprocal_impl,
            Monads.reverse: Storage.identity,
            Monads.shape: Word.zero,
            Monads.size: Word.zero,
            Monads.transpose: Storage.identity,
            Monads.unique: Storage.identity,

            # Dyads
            # Dyads.amend: {
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): Word.amend_impl,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): Word.amend_impl,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): Word.amend_impl,
            # },
            Dyads.cut: expand_dispatch(Word.cut_impl),
            Dyads.divide: match_dispatch(Word.divide_word, Word.divide_float, Word.divide_words, Word.divide_floats, Word.divide_mixed),
            # Dyads.drop unsupported
            Dyads.equal: match_dispatch(Word.equal_word, Word.equal_float, Word.equal_words, Word.equal_floats, Word.equal_mixed),
            # Dyads.expand: unsupported
            Dyads.find: {
                # (NounType.INTEGER, StorageType.WORD): unsupported
                # (NounType.REAL, StorageType.FLOAT): unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.find_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.find_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.find_list,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.index_mixed,
            },
            # indexInDepth unimplemented FIXME
            Dyads.integerDivide: {
                (NounType.INTEGER, StorageType.WORD): Word.integerDivide_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.integerDivide_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.integerDivide_mixed,
            },
            Dyads.join: match_dispatch(Word.join_word, Word.join_float, Word.join_words, Word.join_floats, Word.join_mixed),
            Dyads.less: match_dispatch(Word.less_word, Word.less_float, Word.less_words, Word.less_floats, Word.less_mixed),
            Dyads.match: match_dispatch(Word.match_word, Word.match_float, Word.false, Word.false, Word.false, dictionary=Word.false),
            Dyads.max: match_dispatch(Word.max_word, Word.max_float, Word.max_words, Word.max_floats, Word.max_mixed),
            Dyads.min: match_dispatch(Word.min_word, Word.min_float, Word.min_words, Word.min_floats, Word.min_mixed),
            Dyads.minus: match_dispatch(Word.minus_word, Word.minus_float, Word.minus_words, Word.minus_floats, Word.minus_mixed),
            Dyads.more: match_dispatch(Word.more_word, Word.more_float, Word.more_words, Word.more_floats, Word.more_mixed),
            Dyads.plus: match_dispatch(Word.plus_word, Word.plus_float, Word.plus_words, Word.plus_floats, Word.plus_mixed),
            Dyads.power: match_dispatch(Word.power_scalar, Word.power_scalar, Word.power_list, Word.power_list, Word.power_mixed),
            # Dyads.reshape unsupported
            Dyads.remainder: {
                (NounType.INTEGER, StorageType.WORD): Word.remainder_word,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.remainder_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY) unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.remainder_mixed,
            },
            Dyads.rotate: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.rotate_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.rotate_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.rotate_impl,
            },
            Dyads.split: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.split_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.split_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.split_impl,
            },
            # Dyads.take unsupported
            Dyads.times: match_dispatch(Word.times_word, Word.times_float, Word.times_words, Word.times_floats, Word.times_mixed),

            storage.Dyads.apply: {
                (storage.NounType.BUILTIN_MONAD, storage.StorageType.WORD): storage.Storage.apply_builtin_monad,
                (storage.NounType.USER_MONAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_user_monad,
            },

            storage.Triads.apply: {
                (storage.NounType.BUILTIN_DYAD, storage.StorageType.WORD): storage.Storage.apply_builtin_dyad,
                (storage.NounType.USER_DYAD, storage.StorageType.MIXED_ARRAY): storage.Storage.apply_user_dyad,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: Storage.each_scalar,
            #StorageAdverbs.eachPair: unsupported
            Adverbs.over: Storage.identity,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: Word.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: expand_dispatch(Storage.each2_scalar),
            Adverbs.eachLeft: match_dispatch(Storage.eachLeft_scalar, Storage.eachLeft_scalar, Storage.eachLeft_words, Storage.eachLeft_floats, Storage.eachLeft_mixed),
            Adverbs.eachRight: match_dispatch(Storage.eachRight_scalar, Storage.eachRight_scalar, Storage.eachRight_words, Storage.eachRight_floats, Storage.eachRight_mixed),
            Adverbs.overNeutral: expand_dispatch(Storage.overNeutral_scalar),
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            Adverbs.scanOverNeutral: expand_dispatch(Storage.scanOverNeutral_scalar),
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        return obj

class Integer(Noun, metaclass=MetaInteger):
    @staticmethod
    def true():
        return Integer.new(1)

    @staticmethod
    def false():
        return Integer.new(0)

    @staticmethod
    def new(x):
        return Word(x, NounType.INTEGER)
