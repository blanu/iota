from storage import *
from error import *
from nouns import *

def F(*i):
    return Object.from_python_to_expression(list(i))

def C(i):
    if len(i) == 1:
        utf32 = i.encode("utf-32be")
        x = int.from_bytes(utf32, 'big')
        return Word(x, o=NounType.CHARACTER)
    else:
        raise Exception('invalid character')

def eval(*e):
    se = Object.from_python_to_expression(list(e))
    result = se.evaluate()
    return Object.to_python(result)

class Object:
    @staticmethod
    def from_python(i):
        if type(i) == int:
            return Word(i, o=NounType.INTEGER)
        elif type(i) == float:
            return Float(i, o=NounType.REAL)
        elif type(i) == list:
            if all([type(y) == int for y in i]):
                return WordArray(i, o=NounType.LIST)
            elif all([type(y) == float for y in i]):
                return FloatArray(i, o=NounType.LIST)
            else:
                return MixedArray([Object.from_python(y) for y in i], o=NounType.LIST)
        elif type(i) == tuple:
            return Function.new([Object.from_python(y) for y in list(i)])
        elif type(i) == str:
            utf32 = i.encode("utf-32be")
            ints = [int.from_bytes(utf32[y:y+4], 'big') for y in range(0, len(utf32), 4)]
            return WordArray(ints, o=NounType.STRING)
        elif type(i) == dict:
            keys = i.keys()
            values = i.values()
            zipped = zip(keys, values)
            return MixedArray(zipped, o=NounType.DICTIONARY)
        elif isinstance(i, Storage):
            return i

    @staticmethod
    def from_python_to_expression(i):
        parts = [Object.from_python(y) for y in i]
        return Function.new(parts)

    @staticmethod
    def from_bytes(d):
        return Storage.from_bytes(d)

    @staticmethod
    def to_python(i):
        if i.o == NounType.INTEGER:
            return i.i
        elif i.o == NounType.REAL:
            return i.i
        elif i.o == NounType.LIST:
            if i.t == StorageType.WORD_ARRAY:
                return i.i
            elif i.t == StorageType.FLOAT_ARRAY:
                return i.i
            elif i.t == StorageType.MIXED_ARRAY:
                return [Object.to_python(y) for y in i.i]
        elif i.o == NounType.CHARACTER:
            b = int.to_bytes(i.i, 4, 'big')
            return b.decode("utf-32be")
        elif i.o == NounType.STRING:
            b = b''.join([int.to_bytes(y, 4, 'big') for y in i.i])
            return b.decode("utf-32be")
        elif i.o == NounType.DICTIONARY:
            results = {}
            for pair in i.i:
                key = pair.i[0]
                value = pair.i[1]
                results[key] = value
            return results
        elif i.o == NounType.USER_SYMBOL:
            return None # FIXME
        elif i.o == NounType.USER_MONAD:
            return None # FIXME
        elif i.o == NounType.USER_DYAD:
            return None # FIXME
        elif i.o == NounType.USER_TRIAD:
            return None # FIXME
        elif i.o == NounType.EXPRESSION:
            return tuple([Object.to_python(y) for y in i.i])
        elif i.o == NounType.ERROR:
            s = error_to_string(i.i)
            raise Exception(s)

class Function(Object):
    @staticmethod
    def checkSymbols(i):
        hasI = False
        hasX = False
        hasY = False
        for y in i:
            if y.o == NounType.INTEGER:
                continue
            elif y.o == NounType.REAL:
                continue
            elif y.o == NounType.LIST:
                if y.t == StorageType.WORD_ARRAY:
                    continue
                elif y.t == StorageType.FLOAT_ARRAY:
                    continue
                elif y.t == StorageType.MIXED_ARRAY:
                    (subHasI, subHasX, subHasY) = Function.checkSymbols(y.i)
                    hasI = hasI or subHasI
                    hasX = hasX or subHasX
                    hasY = hasY or subHasY
            elif y.o == NounType.EXPRESSION:
                (subHasI, subHasX, subHasY) = Function.checkSymbols(y.i)
                hasI = hasI or subHasI
                hasX = hasX or subHasX
                hasY = hasY or subHasY
            else:
                if y.o == NounType.BUILTIN_SYMBOL:
                    if y.equal(SymbolType.i.symbol()) == Word.true():
                        hasI = True
                    if y.equal(SymbolType.x.symbol()) == Word.true():
                        hasX = True
                    if y.equal(SymbolType.y.symbol()) == Word.true():
                        hasY = True
        return hasI, hasX, hasY

    @staticmethod
    def new(i):
        (hasI, hasX, hasY) = Function.checkSymbols(i)
        if hasY:
            return MixedArray(i, o=NounType.USER_TRIAD)
        elif hasX:
            return MixedArray(i, o=NounType.USER_DYAD)
        elif hasI:
            return MixedArray(i, o=NounType.USER_MONAD)
        else:
            return MixedArray(i, o=NounType.EXPRESSION)

def test_error():
    return Word(ErrorTypes.TEST_ERROR.value, o=NounType.ERROR)

def error_to_string(self):
    if self.i.i == ErrorTypes.UNSUPPORTED_SUBJECT.value:
        return "unsupported subject type"
    elif self.i.i == ErrorTypes.TEST_ERROR.value:
        return "test error"
    elif self.i.i == ErrorTypes.INVALID_ARGUMENT.value:
        return "invalid argument type"
    elif self.i.i == ErrorTypes.BAD_INITIALIZATION.value:
        return "bad initialization value"
    elif self.i.i == ErrorTypes.UNSUPPORTED_OBJECT.value:
        return "operation is not supported by this object type"
    elif self.i.i == ErrorTypes.BAD_STORAGE.value:
        return "this object type does not support this storage type"
    elif self.i.i == ErrorTypes.BAD_OPERATION.value:
        return "this operation is not supported by this object type with this storage type"
    elif self.i.i == ErrorTypes.UNKNOWN_KEY.value:
        return "unknown key"
    elif self.i.i == ErrorTypes.INVALID_ADVERB_ARGUMENT.value:
        return "invalid adverb argument"
    elif self.i.i == ErrorTypes.EMPTY.value:
        return "empty"
    elif self.i.i == ErrorTypes.OUT_OF_BOUNDS.value:
        return "out of bounds"
    elif self.i.i == ErrorTypes.UNEQUAL_ARRAY_LENGTHS.value:
        return "unequal array lengths"
    elif self.i.i == ErrorTypes.BAD_INDEX_TYPE.value:
        return "unsupported index type"
    elif self.i.i == ErrorTypes.SHAPE_MISMATCH.value:
        return "mismatched shapes"
