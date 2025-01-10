from storage import *
from noun import Noun, MetaNoun
from utils import match_dispatch, expand_dispatch


class MetaReal(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.REAL, StorageType.FLOAT)] = {
            # Monads
            Monads.atom: Word.true,
            # Monads.char: unsupported
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Float.enclose_impl,
            # Monads.enumerate: unsupported
            Monads.first: Storage.identity,
            Monads.floor: Float.floor_impl,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: Storage.identity,
            Monads.gradeUp: Storage.identity,
            #StorageMonads.group unsupported
            Monads.negate: Storage.negate_impl,
            Monads.reciprocal: Storage.reciprocal_impl,
            Monads.reverse: Storage.identity,
            Monads.shape: Word.zero,
            Monads.size: Word.zero,
            Monads.transpose: Storage.identity,
            Monads.unique: Storage.identity,

            # Dyads
            # Dyads.amend: {
            #     (NounType.INTEGER, StorageType.WORD): Float.amend_scalar,
            #     (NounType.REAL, StorageType.FLOAT): Float.amend_scalar,
            #     # NounType.LIST unsupported
            # },
            # Dyads.cut unsupported
            Dyads.divide: match_dispatch(Float.divide_word, Float.divide_float, Float.divide_words, Float.divide_floats, Float.divide_mixed),
            # Dyads.drop unsupported
            Dyads.equal: match_dispatch(Float.equal_word, Float.equal_word, Float.equal_words, Float.equal_floats, Float.equal_mixed),
            # Dyads.expand: unsupported
            Dyads.find: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Float.find_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.find_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.find_list,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Float.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.index_mixed,
            },
            # indexInDepth: unimplemented FIXME
            # integerDivide: unsupported
            Dyads.join: match_dispatch(Float.join_word, Float.join_float, Float.join_words, Float.join_floats, Float.join_mixed),
            Dyads.less: match_dispatch(Float.less_word, Float.less_float, Float.less_words, Float.less_floats, Float.less_mixed),
            Dyads.match: match_dispatch(Float.match_word, Float.match_float, Word.false, Word.false, Word.false, dictionary=Word.false),
            Dyads.max: match_dispatch(Float.max_word, Float.max_float, Float.max_words, Float.max_floats, Float.max_mixed),
            Dyads.min: match_dispatch(Float.min_word, Float.min_float, Float.min_words, Float.min_floats, Float.min_mixed),
            Dyads.minus: match_dispatch(Float.minus_word, Float.minus_float, Float.minus_words, Float.minus_floats, Float.minus_mixed),
            Dyads.more: match_dispatch(Float.more_word, Float.more_float, Float.more_words, Float.more_floats, Float.more_mixed),
            Dyads.plus: match_dispatch(Float.plus_word, Float.plus_float, Float.plus_words, Float.plus_floats, Float.plus_mixed),
            Dyads.power: match_dispatch(Float.power_scalar, Float.power_scalar, Float.power_list, Float.power_list, Float.power_mixed),
            # Dyads.reshape unsupported
            # Dyads.remainder unsupported
            # Dyads.rotate unsupported
            Dyads.split: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Float.split_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.split_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.split_list,
            },
            # Dyads.take unsupported
            Dyads.times: match_dispatch(Float.times_word, Float.times_float, Float.times_words, Float.times_floats, Float.times_mixed),

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
            Adverbs.each: Storage.each_scalar,
            #StorageAdverbs.eachPair: unsupported
            Adverbs.over: Storage.identity,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: Float.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: expand_dispatch(Storage.each2_scalar),
            Adverbs.eachLeft: match_dispatch(Storage.eachLeft_scalar, Storage.eachLeft_scalar, Float.eachLeft_words, Float.eachLeft_floats, Float.eachLeft_mixed),
            Adverbs.eachRight: match_dispatch(Storage.eachRight_scalar, Storage.eachRight_scalar, Storage.eachRight_words, Storage.eachRight_floats, Storage.eachRight_mixed),
            Adverbs.overNeutral: expand_dispatch(Float.overNeutral_scalar),
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
            Adverbs.scanOverNeutral: expand_dispatch(Float.scanOverNeutral_scalar),
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        return obj

class Real(Noun, metaclass=MetaReal):
    @staticmethod
    def new(x):
        return Float(x, NounType.REAL)
