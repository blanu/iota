from storage import *
from noun import Noun, MetaNoun

class MetaReal(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.REAL, StorageType.FLOAT)] = {
            # Monads
            Monads.atom: Word.true,
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Float.enclose_impl,
            # Monads.enumerate unsupported
            Monads.first: Storage.identity,
            Monads.floor: Float.floor_impl,
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
            Dyads.divide: {
                (NounType.INTEGER, StorageType.WORD): Float.divide_word,
                (NounType.REAL, StorageType.FLOAT): Float.divide_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.divide_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.divide_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.divide_mixed,
            },
            # Dyads.drop unsupported
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): Float.equal_word,
                (NounType.REAL, StorageType.FLOAT): Float.equal_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.equal_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.equal_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.equal_mixed,
            },
            Dyads.find: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Float.find_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.find_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.find_list,
            },
            Dyads.index: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Float.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.index_mixed,
            },
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): Float.join_word,
                (NounType.REAL, StorageType.FLOAT): Float.join_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.join_mixed,
            },
            Dyads.less: {
                (NounType.INTEGER, StorageType.WORD): Float.less_word,
                (NounType.REAL, StorageType.FLOAT): Float.less_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.less_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.less_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.less_mixed,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Float.match_word,
                (NounType.REAL, StorageType.FLOAT): Float.match_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
            },
            Dyads.max: {
                (NounType.INTEGER, StorageType.WORD): Float.max_word,
                (NounType.REAL, StorageType.FLOAT): Float.max_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.max_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.max_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.max_mixed,
            },
            Dyads.min: {
                (NounType.INTEGER, StorageType.WORD): Float.min_word,
                (NounType.REAL, StorageType.FLOAT): Float.min_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.min_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.min_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.min_mixed,
            },
            Dyads.minus: {
                (NounType.INTEGER, StorageType.WORD): Float.minus_word,
                (NounType.REAL, StorageType.FLOAT): Float.minus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.minus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.minus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.minus_mixed,
            },
            Dyads.more: {
                (NounType.INTEGER, StorageType.WORD): Float.more_word,
                (NounType.REAL, StorageType.FLOAT): Float.more_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.more_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.more_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.more_mixed,
            },
            Dyads.plus: {
                (NounType.INTEGER, StorageType.WORD): Float.plus_word,
                (NounType.REAL, StorageType.FLOAT): Float.plus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.plus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.plus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.plus_mixed,
            },
            Dyads.power: {
                (NounType.INTEGER, StorageType.WORD): Float.power_scalar,
                (NounType.REAL, StorageType.FLOAT): Float.power_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.power_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.power_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.power_mixed,
            },
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
            Dyads.times: {
                (NounType.INTEGER, StorageType.WORD): Float.times_word,
                (NounType.REAL, StorageType.FLOAT): Float.times_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.times_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.times_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.times_mixed,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: Float.each_impl,
            #StorageAdverbs.eachPair: unsupported
            Adverbs.over: Storage.identity,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: Float.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): Float.each2_impl,
                (NounType.REAL, StorageType.FLOAT): Float.each2_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.each2_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.each2_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.each2_impl,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Float.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Float.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.eachLeft_mixed,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Float.eachRight_impl,
                (NounType.REAL, StorageType.FLOAT): Float.eachRight_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.eachRight_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.eachRight_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.eachRight_impl,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): Float.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): Float.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.overNeutral_impl,
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
                (NounType.INTEGER, StorageType.WORD): Float.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): Float.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Float.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Float.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Float.scanOverNeutral_impl,
            },
            Adverbs.scanWhileOne: {
                (NounType.INTEGER, StorageType.WORD): Storage.scanWhileOne_impl,
                (NounType.REAL, StorageType.FLOAT): Storage.scanWhileOne_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.scanWhileOne_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.scanWhileOne_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.scanWhileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.INTEGER, StorageType.WORD): Storage.whileOne_impl,
                (NounType.REAL, StorageType.FLOAT): Storage.whileOne_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.whileOne_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.whileOne_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.whileOne_impl,
            }
        }

        return obj

class Real(Noun, metaclass=MetaReal):
    @staticmethod
    def new(x):
        return Float(x, NounType.REAL)
