from enum import Enum
import storage

class ErrorTypes(Enum):
    BAD_INDEX_TYPE = 0
    BAD_INITIALIZATION = 1
    BAD_STORAGE = 2
    BAD_OPERATION = 3
    EMPTY = 4
    INVALID_ARGUMENT = 5
    INVALID_ADVERB_ARGUMENT = 6
    OUT_OF_BOUNDS = 7
    SHAPE_MISMATCH = 8
    TEST_ERROR = 9
    UNSUPPORTED_OBJECT = 10
    UNSUPPORTED_SUBJECT = 11
    UNKNOWN_KEY = 12
    UNEQUAL_ARRAY_LENGTHS = 13
    DIVISION_BY_ZERO = 14

class Error:
    @staticmethod
    def bad_index_type():
        return Error.new(ErrorTypes.BAD_INDEX_TYPE.value)

    @staticmethod
    def bad_initialization():
        return Error.new(ErrorTypes.BAD_INITIALIZATION.value)

    @staticmethod
    def bad_storage():
        return Error.new(ErrorTypes.BAD_STORAGE.value)

    @staticmethod
    def bad_operation():
        return Error.new(ErrorTypes.BAD_OPERATION.value)

    @staticmethod
    def empty_argument():
        return Error.new(ErrorTypes.EMPTY.value)

    @staticmethod
    def invalid_argument():
        return Error.new(ErrorTypes.INVALID_ARGUMENT.value)

    @staticmethod
    def invalid_adverb_argument():
        return Error.new(ErrorTypes.INVALID_ADVERB_ARGUMENT.value)

    @staticmethod
    def out_of_bounds():
        return Error.new(ErrorTypes.OUT_OF_BOUNDS.value)

    @staticmethod
    def shape_mismatch():
        return Error.new(ErrorTypes.SHAPE_MISMATCH.value)

    @staticmethod
    def test_error():
        return Error.new(ErrorTypes.TEST_ERROR.value)

    @staticmethod
    def unsupported_object():
        return Error.new(ErrorTypes.UNSUPPORTED_OBJECT.value)

    @staticmethod
    def unsupported_subject():
        return Error.new(ErrorTypes.UNSUPPORTED_SUBJECT.value)

    @staticmethod
    def unknown_key():
        return Error.new(ErrorTypes.UNKNOWN_KEY.value)

    @staticmethod
    def unequal_array_lengths():
        return Error.new(ErrorTypes.UNEQUAL_ARRAY_LENGTHS.value)

    @staticmethod
    def division_by_zero():
        return Error.new(ErrorTypes.DIVISION_BY_ZERO.value)

    @staticmethod
    def new(x):
        return storage.Word(x, o=storage.NounType.ERROR)

    @staticmethod
    def string(i):
        if i.i == ErrorTypes.UNSUPPORTED_SUBJECT.value:
            return "unsupported subject type"
        elif i.i == ErrorTypes.TEST_ERROR.value:
            return "test error"
        elif i.i == ErrorTypes.INVALID_ARGUMENT.value:
            return "invalid argument type"
        elif i.i == ErrorTypes.BAD_INITIALIZATION.value:
            return "bad initialization value"
        elif i.i == ErrorTypes.UNSUPPORTED_OBJECT.value:
            return "operation is not supported by this object type"
        elif i.i == ErrorTypes.BAD_STORAGE.value:
            return "this object type does not support this storage type"
        elif i.i == ErrorTypes.BAD_OPERATION.value:
            return "this operation is not supported by this object type with this storage type"
        elif i.i == ErrorTypes.UNKNOWN_KEY.value:
            return "unknown key"
        elif i.i == ErrorTypes.INVALID_ADVERB_ARGUMENT.value:
            return "invalid adverb argument"
        elif i.i == ErrorTypes.EMPTY.value:
            return "empty"
        elif i.i == ErrorTypes.OUT_OF_BOUNDS.value:
            return "out of bounds"
        elif i.i == ErrorTypes.UNEQUAL_ARRAY_LENGTHS.value:
            return "unequal array lengths"
        elif i.i == ErrorTypes.BAD_INDEX_TYPE.value:
            return "unsupported index type"
        elif i.i == ErrorTypes.SHAPE_MISMATCH.value:
            return "mismatched shapes"
