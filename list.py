from storage import *
from noun import Noun, MetaNoun
import error
from utils import *

class MetaList(MetaNoun, type):
    def __new__(cls, name, bases, dct):
        obj = super().__new__(cls, name, bases, dct)

        Noun.dispatch[(NounType.LIST, StorageType.WORD_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            Monads.char: WordArray.char_impl,
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
            Dyads.divide: match_dispatch(WordArray.divide_word, WordArray.divide_float, WordArray.divide_words, WordArray.divide_floats, WordArray.divide_mixed),
            Dyads.drop: {
                (NounType.INTEGER, StorageType.WORD): WordArray.drop_word,
                # NounType.REAL unsupported
                # NounType.LIST unsupported
            },
            Dyads.equal: match_dispatch(WordArray.equal_scalar, WordArray.equal_scalar, WordArray.equal_words, WordArray.equal_floats, WordArray.equal_mixed),
            Dyads.find: match_dispatch(WordArray.find_word, WordArray.find_float, WordArray.find_words, WordArray.find_floats, WordArray.find_mixed),
            # form: unimplemented FIXME
            # format2: unimplemented FIXME
            Dyads.index: match_dispatch(WordArray.index_word, WordArray.index_float, WordArray.index_words, WordArray.index_floats, WordArray.index_mixed),
            # indexInDepth: unimplemented FIXME
            Dyads.integerDivide: {
                (NounType.INTEGER, StorageType.WORD): WordArray.integerDivide_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                (NounType.LIST, StorageType.WORD_ARRAY): WordArray.integerDivide_words,
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                (NounType.LIST, StorageType.MIXED_ARRAY): WordArray.integerDivide_mixed,
            },
            Dyads.join: match_dispatch(WordArray.join_word, WordArray.join_float, WordArray.join_words, WordArray.join_floats, WordArray.join_mixed),
            Dyads.less: match_dispatch(WordArray.less_scalar, WordArray.less_scalar, WordArray.less_words, WordArray.less_floats, WordArray.less_mixed),
            Dyads.match: match_dispatch(Word.false, Word.false, WordArray.match_words, WordArray.match_floats, WordArray.match_mixed, dictionary=Word.false),
            Dyads.max: match_dispatch(WordArray.max_word, WordArray.max_float, WordArray.max_words, WordArray.max_floats, WordArray.max_mixed),
            Dyads.min: match_dispatch(WordArray.min_word, WordArray.min_float, WordArray.min_words, WordArray.min_floats, WordArray.min_mixed),
            Dyads.minus: match_dispatch(WordArray.minus_word, WordArray.minus_float, WordArray.minus_words, WordArray.minus_floats, WordArray.minus_mixed),
            Dyads.more: match_dispatch(WordArray.more_scalar, WordArray.more_scalar, WordArray.more_words, WordArray.more_floats, WordArray.more_mixed),
            Dyads.plus: match_dispatch(WordArray.plus_word, WordArray.plus_float, WordArray.plus_words, WordArray.plus_floats, WordArray.plus_mixed),
            Dyads.power: match_dispatch(WordArray.power_scalar, WordArray.power_scalar, WordArray.power_list, WordArray.power_list, WordArray.power_list),
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
            Dyads.split: match_dispatch(WordArray.split_word, WordArray.split_float, WordArray.split_words, WordArray.split_floats, WordArray.split_mixed),
            Dyads.take: match_dispatch(WordArray.take_word, WordArray.take_float, WordArray.take_words, WordArray.take_floats, WordArray.take_mixed),
            Dyads.times: match_dispatch(WordArray.times_word, WordArray.times_float, WordArray.times_words, WordArray.times_floats, WordArray.times_mixed),

            # Extension Monads

            Monads.erase: WordArray.erase_impl,
            Monads.truth: Storage.truth_list,

            # Extension Dyads

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_user_monad,
            },

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): WordArray.retype_impl
            },

            # Extension Triads

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_user_dyad,
            },

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: WordArray.each_impl,
            MonadicAdverbs.eachPair: WordArray.eachPair_impl,
            MonadicAdverbs.over: WordArray.over_impl,
            MonadicAdverbs.scanConverging: Storage.scanConverging_impl,
            MonadicAdverbs.scanOver: WordArray.scanOver_impl,

            # Dyadic Adverbs
            DyadicAdverbs.each2: match_dispatch(WordArray.each2_scalar, WordArray.each2_scalar, WordArray.each2_words, WordArray.each2_floats, WordArray.each2_mixed),
            DyadicAdverbs.eachLeft: match_dispatch(WordArray.eachLeft_scalar, WordArray.eachLeft_scalar, WordArray.eachLeft_words, WordArray.eachLeft_floats, WordArray.eachLeft_mixed),
            DyadicAdverbs.eachRight: match_dispatch(Storage.eachRight_scalar, Storage.eachRight_scalar, Storage.eachRight_words, Storage.eachRight_floats, Storage.eachRight_mixed),
            DyadicAdverbs.overNeutral: expand_dispatch(WordArray.overNeutral_impl),
            DyadicAdverbs.iterate: {
                (NounType.INTEGER, StorageType.WORD): Storage.iterate_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanIterating: {
                (NounType.INTEGER, StorageType.WORD): Storage.scanIterating_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanOverNeutral: expand_dispatch(WordArray.scanOverNeutral_impl),
            DyadicAdverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            DyadicAdverbs.whileOne: {
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

            # Extension Monads

            Monads.erase: FloatArray.erase_impl,
            Monads.truth: Storage.truth_list,

            # Extension Dyads

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_user_monad,
            },

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): FloatArray.retype_impl
            },

            # Extension Triads

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_user_dyad,
            },

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: FloatArray.each_impl,
            MonadicAdverbs.eachPair: FloatArray.eachPair_impl,
            MonadicAdverbs.over: FloatArray.over_impl,
            MonadicAdverbs.scanConverging: Storage.scanConverging_impl,
            MonadicAdverbs.scanOver: FloatArray.scanOver_impl,

            # Dyadic Adverbs
            DyadicAdverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.each2_scalar,
                (NounType.REAL, StorageType.FLOAT): FloatArray.each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.each2_mixed,
            },
            DyadicAdverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
            },
            DyadicAdverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
            },
            DyadicAdverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.overNeutral_impl,
            },
            DyadicAdverbs.iterate: {
                (NounType.INTEGER, StorageType.WORD): Storage.iterate_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanIterating: {
                (NounType.INTEGER, StorageType.WORD): Storage.scanIterating_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanOverNeutral: {
                (NounType.INTEGER, StorageType.WORD): FloatArray.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): FloatArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): FloatArray.scanOverNeutral_impl,
            },
            DyadicAdverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            DyadicAdverbs.whileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            }
        }

        Noun.dispatch[(NounType.LIST, StorageType.MIXED_ARRAY)] = {
            # Monads
            Monads.atom: Storage.atom_list,
            Monads.char: MixedArray.char_impl,
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

            # Extension Monads

            Monads.erase: MixedArray.erase_impl,
            Monads.truth: Storage.truth_list,

            # Extension Dyads

            Dyads.applyMonad: {
                (NounType.BUILTIN_MONAD, StorageType.WORD): Storage.applyMonad_builtin_monad,
                (NounType.USER_MONAD, StorageType.MIXED_ARRAY): Storage.applyMonad_user_monad,
            },

            Dyads.retype: {
                (NounType.TYPE, StorageType.WORD): MixedArray.retype_impl
            },

            # Extension Triads

            Triads.applyDyad: {
                (NounType.BUILTIN_DYAD, StorageType.WORD): Storage.applyDyad_builtin_dyad,
                (NounType.USER_DYAD, StorageType.MIXED_ARRAY): Storage.applyDyad_user_dyad,
            },

            # Monadic Adverbs
            MonadicAdverbs.converge: Storage.converge_impl,
            MonadicAdverbs.each: MixedArray.each_impl,
            MonadicAdverbs.eachPair: MixedArray.eachPair_impl,
            MonadicAdverbs.over: MixedArray.over_impl,
            MonadicAdverbs.scanConverging: Storage.scanConverging_impl,
            MonadicAdverbs.scanOver: MixedArray.scanOver_impl,

            # Dyadic Adverbs
            DyadicAdverbs.each2: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.each2_scalar,
                (NounType.REAL, StorageType.FLOAT): MixedArray.each2_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.each2_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.each2_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.each2_mixed,
            },
            DyadicAdverbs.eachLeft: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachLeft_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachLeft_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachLeft_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachLeft_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachLeft_mixed,
            },
            DyadicAdverbs.eachRight: {
                (NounType.INTEGER, StorageType.WORD): Storage.eachRight_scalar,
                (NounType.REAL, StorageType.FLOAT): Storage.eachRight_scalar,
                (NounType.LIST, StorageType.WORD_ARRAY): Storage.eachRight_words,
                (NounType.LIST, StorageType.FLOAT_ARRAY): Storage.eachRight_floats,
                (NounType.LIST, StorageType.MIXED_ARRAY): Storage.eachRight_mixed,
            },
            DyadicAdverbs.overNeutral: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.overNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.overNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.overNeutral_impl,
            },
            DyadicAdverbs.iterate: {
                (NounType.INTEGER, StorageType.WORD): Storage.iterate_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanIterating: {
                (NounType.INTEGER, StorageType.WORD): Storage.scanIterating_word,
                # (NounType.REAL, StorageType.FLOAT): unsupported
                # (NounType.LIST, StorageType.WORD_ARRAY): unsupported
                # (NounType.LIST, StorageType.FLOAT_ARRAY): unsupported
                # (NounType.LIST, StorageType.MIXED_ARRAY): unsupported
            },
            DyadicAdverbs.scanOverNeutral: {
                (NounType.INTEGER, StorageType.WORD): MixedArray.scanOverNeutral_impl,
                (NounType.REAL, StorageType.FLOAT): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.WORD_ARRAY): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.FLOAT_ARRAY): MixedArray.scanOverNeutral_impl,
                (NounType.LIST, StorageType.MIXED_ARRAY): MixedArray.scanOverNeutral_impl,
            },
            DyadicAdverbs.scanWhileOne: {
                (NounType.BUILTIN_SYMBOL, StorageType.WORD): Storage.whileOne_impl,
            },
            DyadicAdverbs.whileOne: {
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
                return Word(error.ErrorTypes.BAD_INITIALIZATION, o=NounType.ERROR)

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
                        results.append(Word(y, o=NounType.INTEGER))
                    elif type(y) == float:
                        results.append(Float(y, o=NounType.REAL))
                    elif type(y) == list:
                        result = List.new(y)
                        if isinstance(result, error.Error):
                            return result
                        else:
                            results.append(result)
                    else:
                        return Word(error.ErrorTypes.BAD_INITIALIZATION, o=NounType.ERROR)
                return MixedArray(results, o=NounType.LIST)
        else:
            return Word(error.ErrorTypes.BAD_INITIALIZATION, o=NounType.ERROR)
