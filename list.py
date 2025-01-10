from storage import *
from noun import Noun, MetaNoun
from integer import Integer
from real import Real
import error

class MetaList(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.LIST, StorageType.WORD_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            # Monads.char: hotpatched by character.py to avoid circular imports
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Storage.enclose_impl,
            # Monads.enumerate: unsupported
            # Monads.expand: unimplemented FIXME
            Monads.first: WordArray.first_impl,
            Monads.floor: Storage.identity,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: WordArray.gradeDown_impl,
            Monads.gradeUp: WordArray.gradeUp_impl,
            # Monads.group: WordArray.group_impl,
            Monads.negate: Storage.negate_impl,
            Monads.reciprocal: Storage.reciprocal_impl,
            Monads.reverse: WordArray.reverse_impl,
            Monads.shape: WordArray.shape_impl,
            Monads.size: WordArray.size_impl,
            Monads.transpose: Storage.identity,
            Monads.unique: WordArray.unique_impl,

            # Dyads
            #
            # Dyads.amend: {
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): WordArray.amend_words,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.amend_floats,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.amend_mixed,
            # },
            Dyads.cut: {
                (NounType.INTEGER, StorageType.WORD): WordArray.cut_word,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.cut_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.cut_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.cut_mixed,
            },
            Dyads.divide: {
                (NounType.INTEGER, StorageType.WORD): WordArray.divide_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.divide_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.divide_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.divide_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.divide_mixed,
            },
            Dyads.drop: {
                (NounType.INTEGER, StorageType.WORD): WordArray.drop_word,
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): WordArray.equal_scalar,
                (NounType.REAL, StorageType.FLOAT): WordArray.equal_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.equal_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.equal_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.equal_mixed,
            },
            Dyads.find: {
                (NounType.INTEGER, StorageType.WORD): WordArray.find_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.find_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.find_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.find_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.find_mixed,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                (NounType.INTEGER, StorageType.WORD): WordArray.index_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.index_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.index_mixed,
            },
            # indexInDepth: unimplemented FIXME
            Dyads.integerDivide: {
                (NounType.INTEGER, StorageType.WORD): WordArray.integerDivide_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.integerDivide_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.integerDivide_mixed,
            },
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): WordArray.join_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.join_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.join_mixed,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): WordArray.join_dictionary,
            },
            Dyads.less: {
                (NounType.INTEGER, StorageType.WORD): WordArray.less_scalar,
                (NounType.REAL, StorageType.FLOAT): WordArray.less_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.less_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.less_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.less_mixed,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.match_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.match_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.match_mixed,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): Word.false,
            },
            Dyads.max: {
                (NounType.INTEGER, StorageType.WORD): WordArray.max_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.max_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.max_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.max_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.max_mixed,
            },
            Dyads.min: {
                (NounType.INTEGER, StorageType.WORD): WordArray.min_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.min_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.min_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.min_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.min_mixed,
            },
            Dyads.minus: {
                (NounType.INTEGER, StorageType.WORD): WordArray.minus_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.minus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.minus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.minus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.minus_mixed,
            },
            Dyads.more: {
                (NounType.INTEGER, StorageType.WORD): WordArray.more_scalar,
                (NounType.REAL, StorageType.FLOAT): WordArray.more_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.more_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.more_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.more_mixed,
            },
            Dyads.plus: {
                (NounType.INTEGER, StorageType.WORD): WordArray.plus_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.plus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.plus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.plus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.plus_mixed,
            },
            Dyads.power: {
                (NounType.INTEGER, StorageType.WORD): WordArray.power_scalar,
                (NounType.REAL, StorageType.FLOAT): WordArray.power_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.power_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.power_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.power_list,
            },
            # FIXME Dyads.reshape unimplemented
            Dyads.remainder: {
                (NounType.INTEGER, StorageType.WORD): WordArray.remainder_word,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.remainder_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY) unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.remainder_mixed,
            },
            Dyads.rotate: {
                (NounType.INTEGER, StorageType.WORD): WordArray.rotate_word
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.split: {
                (NounType.INTEGER, StorageType.WORD): WordArray.split_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.split_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.split_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.split_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.split_mixed,
            },
            Dyads.take: {
                (NounType.INTEGER, StorageType.WORD): WordArray.take_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.take_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.take_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.take_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.take_mixed,
            },
            Dyads.times: {
                (NounType.INTEGER, StorageType.WORD): WordArray.times_word,
                (NounType.REAL, StorageType.FLOAT): WordArray.times_float,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.times_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.times_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.times_mixed,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: WordArray.each_impl,
            Adverbs.eachPair: WordArray.eachPair_impl,
            Adverbs.over: WordArray.over_impl,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: WordArray.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): WordArray.each2_scalar,
                (NounType.REAL, StorageType.FLOAT): WordArray.each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.each2_mixed,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): WordArray.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): WordArray.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.overNeutral_impl,
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
                (NounType.INTEGER, StorageType.WORD): WordArray.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): WordArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): WordArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.scanOverNeutral_impl,
            },
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        Noun.dispatch[(NounType.LIST, StorageType.FLOAT_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            # Monads.char: unsupported
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Storage.enclose_impl,
            #Monads.enumerate: unsupported
            Monads.first: FloatArray.first_impl,
            Monads.floor: FloatArray.floor_impl,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: FloatArray.gradeDown_impl,
            Monads.gradeUp: FloatArray.gradeUp_impl,
            # Monads.group: FloatArray.group_impl,
            Monads.negate: Storage.negate_impl,
            Monads.reciprocal: Storage.reciprocal_impl,
            Monads.reverse: FloatArray.reverse_impl,
            Monads.shape: FloatArray.shape_impl,
            Monads.size: FloatArray.size_impl,
            Monads.transpose: Storage.identity,
            Monads.unique: FloatArray.unique_impl,

            # Dyads
            # Dyads.amend: {
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.amend_words,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.amend_floats,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.amend_mixed,
            # },
            Dyads.cut: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.cut_word,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.cut_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.cut_mixed,
            },
            Dyads.divide: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.divide_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.divide_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.divide_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.divide_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.divide_mixed,
            },
            Dyads.drop: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.drop_word,
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.equal_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.equal_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.equal_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.equal_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.equal_mixed,
            },
            Dyads.find: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.find_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.find_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.find_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.find_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.find_mixed,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.index_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.index_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.index_mixed,
            },
            # indexInDepth: unimplemented FIXME
            # integerDivide: unimplemented FIXME
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.join_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.join_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.join_mixed,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): FloatArray.join_dictionary,
            },
            Dyads.less: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.less_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.less_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.less_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.less_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.less_mixed,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.match_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.match_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.match_mixed,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): Word.false,
            },
            Dyads.max: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.max_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.max_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.max_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.max_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.max_mixed,
            },
            Dyads.min: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.min_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.min_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.min_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.min_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.min_mixed,
            },
            Dyads.minus: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.minus_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.minus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.minus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.minus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.minus_mixed,
            },
            Dyads.more: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.more_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.more_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.more_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.more_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.more_mixed,
            },
            Dyads.plus: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.plus_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.plus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.plus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.plus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.plus_mixed,
            },
            Dyads.power: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.power_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.power_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.power_list,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.power_list,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.power_list,
            },
            # FIXME Dyads.reshape unimplemented
            # Dyads.remainder: unsupported
            Dyads.rotate: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.rotate_word
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.split: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.split_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.split_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.split_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.split_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.split_mixed,
            },
            Dyads.take: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.take_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.take_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.take_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.take_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.take_mixed,
            },
            Dyads.times: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.times_word,
                (NounType.REAL, StorageType.FLOAT): FloatArray.times_float,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.times_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.times_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.times_mixed,
            },

            # Monadic Adverbs
            Adverbs.converge: Storage.converge_impl,
            Adverbs.each: FloatArray.each_impl,
            Adverbs.eachPair: FloatArray.eachPair_impl,
            Adverbs.over: FloatArray.over_impl,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: FloatArray.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.each2_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.each2_mixed,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.overNeutral_impl,
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
                (NounType.INTEGER, StorageType.WORD): FloatArray.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.scanOverNeutral_impl,
            },
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        Noun.dispatch[(NounType.LIST, StorageType.MIXED_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            # char: hotpatched by character.py to avoid circular imports
            Monads.complementation: Storage.complementation_impl,
            Monads.enclose: Storage.enclose_impl,
            #Monads.enumerate: unsupported
            Monads.first: MixedArray.first_impl,
            Monads.floor: MixedArray.floor_impl,
            # Monads.format: unimplemented FIXME
            Monads.gradeDown: MixedArray.gradeDown_impl,
            Monads.gradeUp: MixedArray.gradeUp_impl,
            # Monads.group: MixedArray.group_impl,
            Monads.negate: Storage.negate_impl,
            Monads.reciprocal: Storage.reciprocal_impl,
            Monads.reverse: MixedArray.reverse_impl,
            Monads.shape: MixedArray.shape_impl,
            Monads.size: MixedArray.size_impl,
            Monads.transpose: MixedArray.transpose_impl,
            Monads.unique: MixedArray.unique_impl,

            # Dyads
            # Dyads.amend: {
            #     # NounType.INTEGER unsupported
            #     # NounType.REAL unsupported
            #     (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.amend_words,
            #     (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.amend_floats,
            #     (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.amend_mixed,
            # },
            Dyads.cut: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.cut_word,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.cut_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.cut_mixed,
            },
            Dyads.divide: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.divide_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.divide_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.divide_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.divide_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.divide_mixed,
            },
            Dyads.drop: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.drop_word,
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.equal: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.equal_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.equal_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.equal_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.equal_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.equal_impl,
            },
            Dyads.find: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.find_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.find_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.find_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.find_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.find_mixed,
            },
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.index_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.index_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.index_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.index_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.index_mixed,
            },
            # indexInDepth: unimplemented FIXME
            Dyads.integerDivide: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.integerDivide_word,
                # (NounType.REAL, StorageType.FLOAT): MixedArray.join_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.integerDivide_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.integerDivide_mixed,
            },
            Dyads.join: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.join_scalar,
                (NounType.REAL, StorageType.FLOAT): MixedArray.join_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.join_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.join_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.join_mixed,
                (NounType.DICTIONARY, StorageType.WORD_ARRAY): MixedArray.join_dictionary,
            },
            Dyads.less: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.less_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.less_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.less_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.less_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.less_impl,
            },
            Dyads.match: {
                (NounType.INTEGER, StorageType.WORD): Word.false,
                (NounType.REAL, StorageType.FLOAT): Word.false,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.match_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.match_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.match_mixed,
                (NounType.DICTIONARY, StorageType.MIXED_ARRAY): Word.false,
            },
            Dyads.max: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.max_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.max_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.max_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.max_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.max_mixed,
            },
            Dyads.min: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.min_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.min_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.min_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.min_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.min_mixed,
            },
            Dyads.minus: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.minus_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.minus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.minus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.minus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.minus_mixed,
            },
            Dyads.more: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.more_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.more_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.more_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.more_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.more_impl,
            },
            Dyads.plus: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.plus_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.plus_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.plus_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.plus_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.plus_mixed,
            },
            Dyads.power: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.power_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.power_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.power_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.power_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.power_impl,
            },
            # FIXME Dyads.reshape unimplemented
            Dyads.remainder: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.remainder_impl,
                # NounType.REAL unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.remainder_impl,
                # (NounType.LIST, StorageType.FLOAT_ARRAY) unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.remainder_impl,
            },
            Dyads.rotate: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.rotate_word
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.split: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.split_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.split_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.split_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.split_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.split_mixed,
            },
            Dyads.take: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.take_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.take_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.take_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.take_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.take_mixed,
            },
            Dyads.times: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.times_word,
                (NounType.REAL, StorageType.FLOAT): MixedArray.times_float,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.times_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.times_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.times_mixed,
            },

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
            Adverbs.each: MixedArray.each_impl,
            Adverbs.eachPair: MixedArray.eachPair_impl,
            Adverbs.over: MixedArray.over_impl,
            Adverbs.scanConverging: Storage.scanConverging_impl,
            Adverbs.scanOver: MixedArray.scanOver_impl,

            # Dyadic Adverbs
            Adverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.each2_scalar,
                (NounType.REAL, StorageType.FLOAT): MixedArray.each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.each2_mixed,
            },
            Adverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
            },
            Adverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
            },
            Adverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.overNeutral_impl,
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
                (NounType.INTEGER, StorageType.WORD): MixedArray.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.scanOverNeutral_impl,
            },
            Adverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            Adverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        return obj

class List(Noun, metaclass=MetaList):
    @staticmethod
    def empty(typeHint=StorageType.MIXED_ARRAY):
        return List.new([], typeHint=typeHint)

    @staticmethod
    def new(x, typeHint=StorageType.MIXED_ARRAY):
        if len(x) == 0:
            if typeHint == StorageType.WORD_ARRAY:
                return WordArray(x, NounType.LIST)
            elif typeHint == StorageType.FLOAT_ARRAY:
                return FloatArray(x, NounType.LIST)
            elif typeHint == StorageType.MIXED_ARRAY:
                return MixedArray(x, NounType.LIST)
            else:
                return error.Error.bad_initialization()

        if type(x) == list:
            if all(map(lambda y: type(y) == int, x)):
                 return WordArray(x, NounType.LIST)
            elif all(map(lambda y: type(y) == float, x)):
                return FloatArray(x, NounType.LIST)
            elif all(map(lambda y: type(y) == int or type(y) == float, x)):
                return FloatArray([float(y) for y in x], NounType.LIST)
            else:
                results = []
                for y in x:
                    if type(y) == int:
                        results.append(Integer.new(y))
                    elif type(y) == float:
                        results.append(Real.new(y))
                    elif type(y) == list:
                        result = List.new(y)
                        if isinstance(result, error.Error):
                            return result
                        else:
                            results.append(result)
                    else:
                        return error.Error.bad_initialization()
                return MixedArray(results, o=NounType.LIST)
        else:
            return error.Error.bad_initialization()
