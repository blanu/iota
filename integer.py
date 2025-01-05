from storage import *
from noun import Noun, MetaNoun

class MetaInteger(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.INTEGER, StorageType.WORD)] = {
            # Monads
            Monads.atom: Word.true,
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Word.enclose_impl,
            Monads.enumerate: Word.enumerate_impl,
            Monads.first: Storage.identity,
            Monads.floor: Storage.identity,
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
            Dyads.cut: {
                (NounType.INTEGER, StorageType.WORD): Word.cut_impl,
                (NounType.REAL, StorageType.FLOAT): Word.cut_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.cut_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.cut_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.cut_impl,
            },
            Dyads.divide: {
                (NounType.INTEGER, StorageType.WORD): Word.divide_word,
                (NounType.REAL, StorageType.FLOAT): Word.divide_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.divide_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.divide_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.divide_mixed,
            },
            # Dyads.drop unsupported
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): Word.equal_word,
                (NounType.REAL, StorageType.FLOAT): Word.equal_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.equal_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.equal_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.equal_mixed,
            },
            Dyads.find: {
                # (NounType.INTEGER, StorageType.WORD): unsupported
                # (NounType.REAL, StorageType.FLOAT): unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.find_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.find_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.find_list,
            },
            Dyads.index: {
                # NounType.INTEGER unsupported
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): Word.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.index_mixed,
            },
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): Word.join_word,
                (NounType.REAL, StorageType.FLOAT): Word.join_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.join_mixed,
            },
            Dyads.less: {
                (NounType.INTEGER, StorageType.WORD): Word.less_word,
                (NounType.REAL, StorageType.FLOAT): Word.less_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.less_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.less_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.less_mixed,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.match_word,
                (NounType.REAL, StorageType.FLOAT): Word.match_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.false,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.false,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.false,
            },
            Dyads.max: {
                (NounType.INTEGER, StorageType.WORD): Word.max_word,
                (NounType.REAL, StorageType.FLOAT): Word.max_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.max_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.max_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.max_mixed,
            },
            Dyads.min: {
                (NounType.INTEGER, StorageType.WORD): Word.min_word,
                (NounType.REAL, StorageType.FLOAT): Word.min_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.min_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.min_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.min_mixed,
            },
            Dyads.minus: {
                (NounType.INTEGER, StorageType.WORD): Word.minus_word,
                (NounType.REAL, StorageType.FLOAT): Word.minus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.minus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.minus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.minus_mixed,
            },
            Dyads.more: {
                (NounType.INTEGER, StorageType.WORD): Word.more_word,
                (NounType.REAL, StorageType.FLOAT): Word.more_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.more_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.more_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.more_mixed,
            },
            Dyads.plus: {
                (NounType.INTEGER, StorageType.WORD): Word.plus_word,
                (NounType.REAL, StorageType.FLOAT): Word.plus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.plus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.plus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.plus_mixed,
            },
            Dyads.power: {
                (NounType.INTEGER, StorageType.WORD): Word.power_scalar,
                (NounType.REAL, StorageType.FLOAT): Word.power_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.power_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.power_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.power_mixed,
            },
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
            Dyads.times: {
                (NounType.INTEGER, StorageType.WORD): Word.times_word,
                (NounType.REAL, StorageType.FLOAT): Word.times_float,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.times_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.times_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.times_mixed,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: Word.each_impl,
            #StorageAdverbs.eachPair: unsupported
            Adverbs.over: Storage.identity,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: Word.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): Word.each2_impl,
                (NounType.REAL, StorageType.FLOAT): Word.each2_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.each2_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.each2_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.each2_impl,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Word.eachLeft_impl,
                (NounType.REAL, StorageType.FLOAT): Word.eachLeft_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.eachLeft_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.eachLeft_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.eachLeft_impl,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Word.eachRight_impl,
                (NounType.REAL, StorageType.FLOAT): Word.eachRight_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.eachRight_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.eachRight_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.eachRight_impl,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): Word.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): Word.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.overNeutral_impl,
            },
            # Adverbs.iterate: unsupported
            # Adverbs.scanIterating: unsupported
            Adverbs.scanOverNeutral: {
                (NounType.INTEGER, StorageType.WORD): Word.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): Word.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): Word.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Word.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): Word.scanOverNeutral_impl,
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
