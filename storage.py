from abc import abstractmethod
from enum import Enum
import math

class StorageType(Enum):
    INTEGER = 0,
    FLOAT = 1,
    INTEGER_ARRAY = 2, # all integers
    FLOAT_ARRAY = 3, # all floats
    MIXED_ARRAY = 4, # array of storage types
    ERROR = 5

class Storage:
    @staticmethod
    def addStatic(x, y):
        return x.add(y)

    @staticmethod
    def subtractStatic(x, y):
        return x.subtract(y)

    @staticmethod
    def multiplyStatic(x, y):
        return x.multiply(y)

    @staticmethod
    def divideStatic(x, y):
        return x.divide(y)

    @staticmethod
    def _add(x, y):
        return x + y

    @staticmethod
    def _subtract(x, y):
        return x - y

    @staticmethod
    def _multiply(x, y):
        return x * y

    @staticmethod
    def _divide(x, y):
        return x / y

    def __init__(self, x, t):
        self.i = x
        self.type = t

    def __str__(self):
        return str(self.i)

    def __eq__(self, other):
        return self.i == other.i and self.type == other.type

    def __hash__(self):
        return hash(self.i)

    def add(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            return self.dyad(x, self.addStatic, self._add)

    def subtract(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            return self.dyad(x, self.subtractStatic, self._subtract)

    def multiply(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            return self.dyad(x, self.multiplyStatic, self._multiply)

    def divide(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            try:
                return self.dyad(x, self.divideStatic, self._divide)
            except ZeroDivisionError as error:
                return Error(error)

    def negate(self):
        return Integer(0).subtract(self)

    def reciprocal(self):
        return Float(1).divide(self)

    def complementation(self):
        return Integer(1).subtract(self)

    @abstractmethod
    def monad(self, rop, op):
        pass

    @abstractmethod
    def dyad(self, x, rop, op):
        pass

class Integer(Storage):
    def __init__(self, x):
        super().__init__(int(x), StorageType.INTEGER)

    def __lt__(self, x):
        if x.type == StorageType.INTEGER:
            return self.less(x) == Integer(1)
        elif x.type == StorageType.FLOAT:
            return self.less(x) == Integer(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def monad(self, rop, op):
        return Integer(op(self.i))

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return Integer(op(self.i, x.i))
        elif x.type == StorageType.FLOAT:
            return Float(op(float(self.i), x.i))
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray(list(map(lambda y: op(self.i, y), x.i))) # flipped map
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray(list(map(lambda y: op(float(self.i), y), x.i))) # flipped map
        elif x.type == StorageType.MIXED_ARRAY:
            return x.apply(self, rop)

    def join(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray([self.i, x.i])
        elif x.type == StorageType.FLOAT:
            return MixedArray([Integer(self.i), Float(x.i)])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([self.i] + x.i)
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray([float(self.i)] + x.i)
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([Integer(self.i)] + x.i)

    def rotate(self, x):
        if x.type == StorageType.INTEGER_ARRAY:
            return x.rotate(self)
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.rotate(self)
        elif x.type == StorageType.MIXED_ARRAY:
            return x.rotate(self)
        else:
            return Error('unsupported argument type')

    def split(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            return x.split(self)
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.split(self)
        elif x.type == StorageType.MIXED_ARRAY:
            return x.split(self)

    def power(self, x):
        if x.type == StorageType.INTEGER:
            return Float(math.pow(self.i, x.i))
        elif x.type == StorageType.FLOAT:
            return Float(math.pow(self.i, x.i))
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: self.power(y), x.i)))

    def remainder(self, x):
        if x.type == StorageType.INTEGER:
            return Integer(self.i % x.i)
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray(list(map(lambda y: self.i % y, x.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: self.remainder(y), x.i)))
        else:
            return Error('unsupported argument type')

    def match(self, x):
        if x.type == StorageType.INTEGER:
            if self.i == x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            return Float(self.i).match(x)
        else:
            return Integer(0)

    def find(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
        if x.type == StorageType.INTEGER_ARRAY:
            return x.find(IntegerArray([self.i]))
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.find(IntegerArray([self.i]))
        elif x.type == StorageType.MIXED_ARRAY:
            return x.find(IntegerArray([self.i]))

    def max(self, x):
        if x.type == StorageType.INTEGER:
            if self.i >= x.i:
                return self
            else:
                return x
        elif x.type == StorageType.FLOAT:
            if float(self.i) > x.i:
                return Float(self.i)
            elif float(self.i) < x.i:
                return x
            else: #self.i == x.i
                return Float(self.i)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in x.i:
                if self.i > y:
                    results.append(self.i)
                else:
                    results.append(y)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in x.i:
                if float(self.i) > y:
                    results.append(self.i)
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(self.max(y))
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            if self.i <= x.i:
                return self
            else:
                return x
        elif x.type == StorageType.FLOAT:
            if float(self.i) < x.i:
                return Float(self.i)
            elif float(self.i) > x.i:
                return x
            else: #self.i == x.i
                return Float(self.i)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in x.i:
                if self.i < y:
                    results.append(self.i)
                else:
                    results.append(y)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in x.i:
                if float(self.i) < y:
                    results.append(self.i)
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(self.min(y))
            return MixedArray(results)

    def less(self, x):
        if x.type == StorageType.INTEGER:
            if self.i < x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if float(self.i) < x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self.i >= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if float(self.i) >= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.less(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def more(self, x):
        if x.type == StorageType.INTEGER:
            if self.i > x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if float(self.i) > x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self.i <= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if float(self.i) <= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.more(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def equal(self, x):
        if x.type == StorageType.INTEGER:
            if self.i == x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if Float(self.i) == x:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self.i != y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if Float(self.i) != Float(y):
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.equal(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def index(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported arugment type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            if self.i < 1 or self.i > len(x.i):
                return Error('out of bounds')
            else:
                return Integer(x.i[self.i - 1])
        elif x.type == StorageType.FLOAT_ARRAY:
            if self.i < 1 or self.i > len(x.i):
                return Error('out of bounds')
            else:
                return Float(x.i[self.i - 1])
        elif x.type == StorageType.MIXED_ARRAY:
            if self.i < 1 or self.i > len(x.i):
                return Error('out of bounds')
            else:
                return x.i[self.i - 1]

    def cut(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported arugment type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            return x.drop(self)
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.drop(self)
        elif x.type == StorageType.MIXED_ARRAY:
            return x.drop(self)

    def amend(self, x):
        if x.type == StorageType.INTEGER:
            return self.enclose().amend(x.enclose())
        elif x.type == StorageType.FLOAT:
            return self.enclose().amend(x.enclose())
        else:
            return Error('unsupported arugment type')

    def enumerate(self):
        return IntegerArray(list(range(1, self.i+1)))

    def floor(self):
        return self

    def count(self):
        return Integer(1)

    def shape(self):
        return IntegerArray([])

    def enclose(self):
        return IntegerArray([self.i])

class Float(Storage):
    @staticmethod
    def tolerance():
        return 1e-14

    def __init__(self, x):
        super().__init__(float(x), StorageType.FLOAT)

    def __eq__(self, other):
        diff = self.i - other.i
        return abs(diff) < Float.tolerance()

    def __lt__(self, x):
        if x.type == StorageType.INTEGER:
            return self.less(x) == Integer(1)
        elif x.type == StorageType.FLOAT:
            return self.less(x) == Integer(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def monad(self, rop, op):
        return Float(op(self.i))

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return Float(op(self.i, float(x.i)))
        elif x.type == StorageType.FLOAT:
            return Float(op(self.i, x.i))
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray(list(map(lambda y: op(self.i, float(y)), x.i))) # flipped map
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray(list(map(lambda y: op(self.i, y), x.i))) # flipped map
        elif x.type == StorageType.MIXED_ARRAY:
            return x.apply(self, rop)

    def join(self, x):
        if x.type == StorageType.INTEGER:
            return MixedArray([Float(self.i), Integer(x.i)])
        elif x.type == StorageType.FLOAT:
            return FloatArray([self.i, x.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray([self.i] + [float(y) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray([self.i] + x.i)
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([Float(self.i)] + x.i)

    def split(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            return x.split(self)
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.split(self)
        elif x.type == StorageType.MIXED_ARRAY:
            return x.split(self)

    def power(self, x):
        if x.type == StorageType.INTEGER:
            return Float(math.pow(self.i, x.i))
        elif x.type == StorageType.FLOAT:
            return Float(math.pow(self.i, x.i))
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: self.power(y), x.i)))

    def match(self, x):
        if x.type == StorageType.INTEGER:
            return self.match(Float(x.i))
        elif x.type == StorageType.FLOAT:
            if self.i == x.i:
                return Integer(1)
            else:
                return Integer(0)
        else:
            return Integer(0)

    def find(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            return x.find(FloatArray([self.i]))
        elif x.type == StorageType.FLOAT_ARRAY:
            return x.find(FloatArray([self.i]))
        elif x.type == StorageType.MIXED_ARRAY:
            return x.find(FloatArray([self.i]))

    def max(self, x):
        if x.type == StorageType.INTEGER:
            if self.i >= float(x.i):
                return self
            else:
                return Float(x.i)
        elif x.type == StorageType.FLOAT:
            if self.i > x.i:
                return self
            elif self.i < x.i:
                return x
            else: #self.i == x.i
                return self
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in x.i:
                if self.i > float(y):
                    results.append(self.i)
                else:
                    results.append(float(y))
            return FloatArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in x.i:
                if self.i > y:
                    results.append(self.i)
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(self.max(y))
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            if self.i <= float(x.i):
                return self
            else:
                return Float(x.i)
        elif x.type == StorageType.FLOAT:
            if self.i < x.i:
                return self
            elif self.i > x.i:
                return x
            else: #self.i == x.i
                return self
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in x.i:
                if self.i < float(y):
                    results.append(self.i)
                else:
                    results.append(float(y))
            return FloatArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in x.i:
                if self.i < y:
                    results.append(self.i)
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(self.min(y))
            return MixedArray(results)

    def less(self, x):
        if x.type == StorageType.INTEGER:
            if self.i < float(x.i):
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if self.i < x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self.i >= float(y):
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if self.i >= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.less(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def more(self, x):
        if x.type == StorageType.INTEGER:
            if self.i > float(x.i):
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if self.i > x.i:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self.i <= float(y):
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if self.i <= y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.more(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def equal(self, x):
        if x.type == StorageType.INTEGER:
            if self == Float(x.i):
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.FLOAT:
            if self == x:
                return Integer(1)
            else:
                return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            for y in x.i:
                if self != Float(y):
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            for y in x.i:
                if self.i != y:
                    return Integer(0)
            return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            for y in x.i:
                if self.equal(y) != Integer(1):
                    return Integer(0)
            return Integer(1)

    def index(self, x):
        if x.type == StorageType.INTEGER:
            return Error('unsupported arugment type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            count = len(x.i)
            extent = self.i * float(count)
            offset = int(extent)
            return Integer(offset).index(x)
        elif x.type == StorageType.FLOAT_ARRAY:
            count = len(x.i)
            extent = self.i * float(count)
            offset = int(extent)
            return Integer(offset).index(x)
        elif x.type == StorageType.MIXED_ARRAY:
            count = len(x.i)
            extent = self.i * float(count)
            offset = int(extent)
            return Integer(offset).index(x)

    def amend(self, x):
        if x.type == StorageType.INTEGER:
            return self.enclose().amend(x.enclose())
        elif x.type == StorageType.FLOAT:
            return self.enclose().amend(x.enclose())
        else:
            return Error('unsupported arugment type')

    def floor(self):
        return Integer(math.floor(self.i))

    def count(self):
        return Integer(1)

    def shape(self):
        return IntegerArray([])

    def enclose(self):
        return FloatArray([self.i])

class IntegerArray(Storage):
    def __init__(self, x):
        super().__init__(list(map(lambda y: int(y), x)), StorageType.INTEGER_ARRAY)

    def __hash__(self):
        return hash(self.i)

    def monad(self, rop, op):
        return IntegerArray([op(x) for x in self.i])

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return IntegerArray(list(map(lambda y: op(y, x.i), self.i)))
        elif x.type == StorageType.FLOAT:
            return FloatArray(list(map(lambda y: op(float(y), x.i), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: IntegerArray(list(map(lambda z: op(y, z), x.i))), self.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(list(map(lambda y: FloatArray(list(map(lambda z: op(float(y), z), x.i))), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([Integer(y) for y in self.i]).dyad(x, rop, op)

    def take(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return Error('out of bounds')
            elif x.i == 0:
                return IntegerArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return IntegerArray(self.i[:x.i])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return IntegerArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return IntegerArray(results)
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif x.i == 1.9:
                return self
            elif len(self.i) == 0:
                return self
            elif x.i > 0:
                if x.i < 1.0:
                    count = len(self.i)
                    extent = float(count) * x.i
                    lowIndex = int(extent)
                    return self.take(Integer(lowIndex))
                else: # x.i > 1.0
                    replication = int(x.i)
                    remainder = x.i - float(replication)
                    replicated = self.take(Integer(replication))
                    remaindered = self.take(Float(remainder))
                    return replicated.join(remaindered)
            else: # x.i < 0
                return self.reverse().take(x).reverse()
        else:
            return Error('unsupported index type')

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return IntegerArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return IntegerArray(self.i[x.i:])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return IntegerArray(self.i[:x.i])
            else:
                return Error('out of bounds')
        else:
            return Error('unsupported index type')

    def join(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray(self.i + [x.i])
        elif x.type == StorageType.FLOAT:
            return FloatArray([float(y) for y in self.i] + [x.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray(self.i + x.i)
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray([float(y) for y in self.i] + x.i)
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([Integer(y) for y in self.i] + x.i)

    def rotate(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= 1 and x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return self.reverse().rotate(x.negate()).reverse()
            elif x.i > len(self.i):
                return self.rotate(Integer(x.i % len(self.i)))
            elif x.i < 0 and abs(x.i) > len(self.i):
                return self.rotate(Integer(-(abs(x.i) % len(self.i))))
        else:
            return Error('unsupported argument type')

    def split(self, x):
        if len(self.i) == 0:
            return Error('out of bounds')
        elif x.type == StorageType.INTEGER:
            if x.i > 0 and x.i <= len(self.i):
                return MixedArray([IntegerArray(self.i[:x.i]), IntegerArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif x.i > 0.0 and x.i <= 1.0:
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.split(Integer(lowIndex))
            else:
                return Error('out of bounds')
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = x.i[index]
                split  = working.split(Integer(offset))
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = Float(x.i[index])
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = x.i[index]
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def power(self, x):
        if x.type == StorageType.INTEGER:
            return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))
        elif x.type == StorageType.FLOAT:
            return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: Integer(y).power(x), self.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(list(map(lambda y: Integer(y).power(x), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: Integer(y).power(x), self.i)))

    def remainder(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray(list(map(lambda y: y % x.i, self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: Integer(y).remainder(x), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: Integer(y).remainder(x), self.i)))
        else:
            return Error('unsupported argument type')

    def match(self, x):
        if x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        if y != z:
                            return Integer(0)
                    return Integer(1)
                else:
                    return Integer(0)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        if Float(y) != Float(z):
                            return Integer(0)
                    return Integer(1)
                else:
                    return Integer(0)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        if Float(y) != z:
                            return Integer(0)
                    return Integer(1)
                else:
                    return Integer(0)
        else:
            return Integer(0)

    def find(self, x):
        if len(self.i) == 0:
            return IntegerArray([])
        elif x.type == StorageType.INTEGER:
            return self.find(IntegerArray([x.i]))
        elif x.type == StorageType.FLOAT:
            return self.find(FloatArray([x.i]))
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        if self.i[offset:offset+len(x.i)] == x.i:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if Integer(y).match(Float(z)) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if Integer(y).match(z) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)

    def max(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                if y > x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                if float(y) > x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return FloatArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                result = Integer(y)
                for z in x.i:
                    result = result.max(Integer(z))
                results.append(result.i)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.max(Float(z))
                results.append(result.i)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.max(z)
                results.append(result)
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                if y < x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                if float(y) < x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return FloatArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                result = Integer(y)
                for z in x.i:
                    result = result.min(Integer(z))
                results.append(result.i)
            return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.min(Float(z))
                results.append(result.i)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.min(z)
                results.append(result)
            return MixedArray(results)

    def less(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray([Integer(y).less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([Integer(y).less(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([Integer(y).less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([Integer(y).less(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return IntegerArray([Integer(y).less(x).i for y in self.i])

    def more(self, x):
        return IntegerArray([Integer(y).more(x).i for y in self.i])

    def equal(self, x):
        return IntegerArray([Integer(y).equal(x).i for y in self.i])

    def index(self, x):
        if x.type == StorageType.INTEGER:
            if x.i < 1 or x.i > len(self.i):
                return Error('out of bounds')
            else:
                return Integer(self.i[x.i - 1])
        elif x.type == StorageType.FLOAT:
            count = len(self.i)
            extent = x.i * float(count)
            offset = int(extent)
            return self.index(Integer(offset))
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([self.i[y - 1] for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([self.index(Float(y)).i for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return IntegerArray([self.index(y).i for y in x.i])

    def cut(self, x):
        if x.type == StorageType.INTEGER:
            return self.drop(x)
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            first = x.i[0] - 1
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y - 1
                if first <= last:
                    results.append(IntegerArray(self.i[first:last]))
                    first = last
                else:
                    return Error('invalid argument value')
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            length = len(self.i)
            first = x.i[0]
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y.i[0]
                if first <= last:
                    results.append(FloatArray([self.i[first:last]]))
                else:
                    return Error('invalid argument value')
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            first = x.i[0]
            if first.type != StorageType.INTEGER:
                return Error('invalid argument type')
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y
                if last.type != StorageType.INTEGER:
                    return Error('invalid argument type')
                if first.i <= last.i:
                    results.append(IntegerArray(self.i[first.i:last.i]))
                else:
                    return Error('invalid argument value')
            return MixedArray(results)

    def replicate(self, x):
        if x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    results = results + ([y]*z)
                return IntegerArray(results)
            else:
                return Error('invalid argument value')
        else:
            return Error('unsupported argument type')

    def amend(self, x):
        if x.type == StorageType.INTEGER:
            return Error('invalid argument type')
        elif x.type == StorageType.FLOAT:
            return Error('invalid argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')

    def floor(self):
        return self

    def count(self):
        return Integer(len(self.i))

    def reverse(self):
        return IntegerArray(list(reversed(self.i)))

    def first(self):
        if len(self.i) == 0:
            return Error('empty')
        else:
            return Integer(self.i[0])

    def shape(self):
        return IntegerArray([len(self.i)])

    def enclose(self):
        return MixedArray([self])

    def unique(self):
        return IntegerArray(list(dict.fromkeys(self.i)))

    def gradeUp(self):
        return IntegerArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    def gradeDown(self):
        return self.gradeUp().reverse()

    def group(self):
        keys = self.unique()
        values = []
        for key in keys.i:
            indexes = []
            for index in range(len(self.i)):
                if self.i[index] == key:
                    indexes.append(index + 1)
            values.append(IntegerArray(indexes))
        return Dictionary(keys, MixedArray(values))

class FloatArray(Storage):
    def __init__(self, x):
        super().__init__(list(map(lambda y: float(y), x)), StorageType.FLOAT_ARRAY)

    def __hash__(self):
        return hash(self.i)

    def monad(self, rop, op):
        return FloatArray([op(x) for x in self.i])

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return FloatArray(list(map(lambda y: op(y, float(x.i)), self.i)))
        elif x.type == StorageType.FLOAT:
            return FloatArray(list(map(lambda y: op(y, x.i), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: FloatArray(list(map(lambda z: op(y, z), x.i))), self.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(list(map(lambda y: FloatArray(list(map(lambda z: op(float(y), z), x.i))), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: MixedArray(list(map(lambda z: rop(Float(y), z)), x.i)), self.i)))

    def take(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return Error('out of bounds')
            elif x.i == 0:
                return FloatArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return FloatArray(self.i[:x.i])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return FloatArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return FloatArray(results)
            else:
                return Error('out of bounds')
        else:
            return Error('unsupported index type')

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return FloatArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return FloatArray(self.i[x.i:])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return FloatArray(self.i[:-x.i])
            else:
                return Error('out of bounds')
        else:
            return Error('unsupported index type')

    def join(self, x):
        if x.type == StorageType.INTEGER:
            return FloatArray(self.i + [float(x.i)])
        elif x.type == StorageType.FLOAT:
            return FloatArray(self.i + [x.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray(self.i + [float(y) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray(self.i + x.i)
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([Float(self.i)] + x.i)

    def rotate(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= 1 and x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return self.reverse().rotate(x.negate()).reverse()
            elif x.i > len(self.i):
                return self.rotate(Integer(x.i % len(self.i)))
            elif x.i < 0 and abs(x.i) > len(self.i):
                return self.rotate(Integer(-(abs(x.i) % len(self.i))))
        else:
            return Error('unsupported argument type')

    def power(self, x):
        if x.type == StorageType.INTEGER:
            return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))
        elif x.type == StorageType.FLOAT:
            return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: Float(y).power(x), self.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(list(map(lambda y: Float(y).power(x), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: Float(y).power(x), self.i)))

    def split(self, x):
        if len(self.i) == 0:
            return Error('out of bounds')
        elif x.type == StorageType.INTEGER:
            if x.i > 0 and x.i <= len(self.i):
                return MixedArray([FloatArray(self.i[:x.i]), FloatArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif x.i > 0.0 and x.i <= 1.0:
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.split(Integer(lowIndex))
            else:
                return Error('out of bounds')
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            working = self
            for index in range(x.i):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = x.i[index]
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split[0])
                working = split[1]
            results.append(working)
            return results
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            working = self
            for index in range(x.i):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = x.i[index]
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split[0])
                working = split[1]
            results.append(working)
            return results

    def match(self, x):
        if x.type == StorageType.INTEGER:
            return Integer(0)
        elif x.type == StorageType.FLOAT:
            return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if Float(y).match(Integer(z)) != Integer(1):
                        return Integer(0)
                return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            return self.i == x.i
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if Float(y).match(z) != Integer(1):
                        return Integer(0)
                return Integer(1)

    def find(self, x):
        if len(self.i) == 0:
            return IntegerArray([])
        elif x.type == StorageType.INTEGER:
            return self.find(IntegerArray([x.i]))
        elif x.type == StorageType.FLOAT:
            return self.find(FloatArray([x.i]))
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if Float(y).match(Integer(z)) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        if self.i[offset:offset+len(x.i)] == x.i:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if Float(y).match(z) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)

    def max(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                if y > float(x.i):
                    results.append(y)
                else:
                    results.append(float(x.i))
            return FloatArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                if y > x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return FloatArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                results.append(Float(y).max(x).i)
            return FloatArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                results.append(Float(y).max(x).i)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(y.max(x))
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                if y < float(x.i):
                    results.append(y)
                else:
                    results.append(float(x.i))
            return FloatArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                if y < x.i:
                    results.append(y)
                else:
                    results.append(x.i)
            return FloatArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                results.append(Float(y).min(x).i)
            return FloatArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                results.append(Float(y).min(x).i)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in x.i:
                results.append(y.min(x))
            return MixedArray(results)

    def less(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray([Float(y).less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([Float(y).less(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([Float(y).less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([Float(y).less(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return IntegerArray([Float(y).less(x).i for y in self.i])

    def more(self, x):
        return IntegerArray([Float(y).more(x).i for y in self.i])

    def equal(self, x):
        return IntegerArray([Float(y).more(x).i for y in self.i])

    def index(self, x):
        if x.type == StorageType.INTEGER:
            if x.i < 1 or x.i > len(self.i):
                return Error('out of bounds')
            else:
                return Float(self.i[x.i - 1])
        elif x.type == StorageType.FLOAT:
            count = len(self.i)
            extent = x.i * float(count)
            offset = int(extent)
            return self.index(Integer(offset))
        elif x.type == StorageType.INTEGER_ARRAY:
            return FloatArray([self.i[y] for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray([self.index(Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return FloatArray([self.index(y).i for y in x.i])

    def cut(self, x):
        if x.type == StorageType.INTEGER:
            return self.drop(x)
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            first = x.i[0] - 1
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y - 1
                if first <= last:
                    results.append(FloatArray(self.i[first:last]))
                    first = last
                else:
                    return Error('invalid argument value')
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            return Error('invalid argument type')
        elif x.type == StorageType.MIXED_ARRAY:
            first = x.i[0]
            if first.type != StorageType.INTEGER:
                return Error('invalid argument type')
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y
                if last.type != StorageType.INTEGER:
                    return Error('invalid argument type')
                if first.i <= last.i:
                    results.append(FloatArray(self.i[first.i:last.i]))
                else:
                    return Error('invalid argument value')
            return MixedArray(results)

    def replicate(self, x):
        if x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    results = results + ([y]*z)
                return FloatArray(results)
            else:
                return Error('invalid argument value')
        else:
            return Error('unsupported argument type')

    def amend(self, x):
        if x.type == StorageType.INTEGER:
            return Error('invalid argument type')
        elif x.type == StorageType.FLOAT:
            return Error('invalid argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')

    def floor(self):
        return IntegerArray([math.floor(x) for x in self.i])

    def count(self):
        return Integer(len(self.i))

    def reverse(self):
        return FloatArray(list(reversed(self.i)))

    def first(self):
        if len(self.i) == 0:
            return Error('empty')
        else:
            return Float(self.i[0])

    def shape(self):
        return IntegerArray([len(self.i)])

    def enclose(self):
        return MixedArray([self])

    def unique(self):
        return FloatArray(list(dict.fromkeys(self.i)))

    def gradeUp(self):
        return IntegerArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    def gradeDown(self):
        return self.gradeUp().reverse()

    def group(self):
        keys = self.unique()
        values = []
        for key in keys.i:
            indexes = []
            for index in range(len(self.i)):
                if self.i[index] == key:
                    indexes.append(index + 1)
            values.append(IntegerArray(indexes))
        return Dictionary(keys, MixedArray(values))

class MixedArray(Storage):
    def __init__(self, x):
        super().__init__(x, StorageType.MIXED_ARRAY)

    def __str__(self):
        return "[%s]" % ", ".join(list(map(lambda x: str(x), self.i)))

    def __eq__(self, other):
        if self.type != other.type:
            return False

        for x, y in zip(self.i, other.i):
            if x != y:
                return False

        return True

    def __hash__(self):
        return hash(self.i)

    def monad(self, rop, op):
        return MixedArray([rop(x) for x in self.i])

    def dyad(self, x, rop, op):
        results = []
        for y in self.i:
            result = rop(y, x)
            if result.type == StorageType.ERROR:
                return result
            else:
                results.append(result)

        return MixedArray(results)

    def apply(self, x, rop):
        results = []
        for y in self.i:
            result = rop(x, y)
            if result.type == StorageType.ERROR:
                return result
            else:
                results.append(result)

        return MixedArray(results)

    def take(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return Error('out of bounds')
            elif x.i == 0:
                return MixedArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return MixedArray(self.i[:x.i])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return MixedArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return MixedArray(results)
            else:
                return Error('out of bounds')
        else:
            return Error('unsupported index type')

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return MixedArray([])
            elif x.i >= 1 and x.i <= len(self.i):
               return MixedArray(self.i[x.i:])
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return MixedArray(self.i[:-x.i])
            else:
                return Error('out of bounds')
        else:
            return Error('unsupported index type')

    def join(self, x):
        if x.type == StorageType.INTEGER:
            return MixedArray(self.i + [x])
        elif x.type == StorageType.FLOAT:
            return MixedArray(self.i + [x])
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(self.i + [Integer(y) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(self.i + [Float(y) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(self.i + x.i)

    def rotate(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= 1 and x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and abs(x.i) >= 1 and abs(x.i) <= len(self.i):
                return self.reverse().rotate(x.negate()).reverse()
            elif x.i > len(self.i):
                return self.rotate(Integer(x.i % len(self.i)))
            elif x.i < 0 and abs(x.i) > len(self.i):
                return self.rotate(Integer(-(abs(x.i) % len(self.i))))
        else:
            return Error('unsupported argument type')

    def power(self, x):
        if x.type == StorageType.INTEGER:
            return MixedArray(list(map(lambda y: y.power(x), self.i)))
        elif x.type == StorageType.FLOAT:
            return MixedArray(list(map(lambda y: y.power(x), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: y.power(x), self.i)))
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray(list(map(lambda y: y.power(x), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: y.power(x), self.i)))

    def remainder(self, x):
        if x.type == StorageType.INTEGER:
            return MixedArray(list(map(lambda y: y.remainder(x), self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray(list(map(lambda y: y.remainder(x), self.i)))
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray(list(map(lambda y: y.remainder(x), self.i)))
        else:
            return Error('unsupported argument type')

    def split(self, x):
        if len(self.i) == 0:
            return Error('out of bounds')
        elif x.type == StorageType.INTEGER:
            if x.i > 0 and x.i <= len(self.i):
                return MixedArray([MixedArray(self.i[:x.i]), MixedArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif x.i > 0.0 and x.i <= 1.0:
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.split(Integer(lowIndex))
            else:
                return Error('out of bounds')
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = Integer(x.i[index])
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = Float(x.i[index])
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return Error('out of bounds')
                offset = x.i[index]
                split  = working.split(offset)
                if len(split.i) != 2:
                    return Error('out of bounds')
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def match(self, x):
        if x.type == StorageType.INTEGER:
            return Integer(0)
        elif x.type == StorageType.FLOAT:
            return Integer(0)
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(Integer(z)) != Integer(1):
                        return Integer(0)
                return Integer(1)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(Float(z)) != Integer(1):
                        return Integer(0)
                return Integer(1)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer(1)
                else:
                    return Integer(0)
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(z) != Integer(1):
                        return Integer(0)
                return Integer(1)

    def find(self, x):
        if len(self.i) == 0:
            return IntegerArray([])
        elif x.type == StorageType.INTEGER:
            return IntegerArray(list(map(lambda y: y.match(x).i, self.i)))
        elif x.type == StorageType.FLOAT:
            return IntegerArray(list(map(lambda y: y.match(x).i, self.i)))
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if y.match(Integer(z)) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if y.match(Float(z)) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        slice = self.i[offset:offset+len(x.i)]
                        zipped = zip(slice, x.i)
                        matched = True
                        for y, z in zipped:
                            if y.match(z) != Integer(1):
                                matched = False
                                break
                        if matched:
                            results.append(1)
                        else:
                            results.append(0)
                    else:
                        results.append(0)
                return IntegerArray(results)

    def max(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                results.append(y.max(x))
            return MixedArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                results.append(y.max(x))
            return MixedArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.max(Integer(z))
                results.append(result)
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.max(Float(z))
                results.append(result)
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.max(z)
                results.append(result)
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                results.append(y.min(x))
            return MixedArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                results.append(y.min(x))
            return MixedArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(Integer(z))
                results.append(result)
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(Float(z))
                results.append(result)
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(z)
                results.append(result)
            return MixedArray(results)

    def less(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray([y.less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([y.less(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([y.less(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([y.less(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return IntegerArray([y.less(x).i for y in self.i])

    def more(self, x):
        return IntegerArray([y.more(x).i for y in self.i])

    def equal(self, x):
        return IntegerArray([y.equal(x).i for y in self.i])

    def index(self, x):
        if x.type == StorageType.INTEGER:
            if x.i < 1 or x.i > len(self.i):
                return Error('out of bounds')
            else:
                return self.i[x.i - 1]
        elif x.type == StorageType.FLOAT:
            count = len(self.i)
            extent = x.i * float(count)
            offset = int(extent)
            return self.index(Integer(offset))
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.i[y - 1] for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.index(Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.index(y) for y in x.i])

    def cut(self, x):
        if x.type == StorageType.INTEGER:
            return self.drop(x)
        elif x.type == StorageType.FLOAT:
            return Error('unsupported arugment type')
        elif x.type == StorageType.INTEGER_ARRAY:
            first = x.i[0]
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y - 1
                if first <= last:
                    results.append(MixedArray(self.i[first:last]))
                    first = last
                else:
                    return Error('invalid argument value')
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            return Error('invalid argument type')
        elif x.type == StorageType.MIXED_ARRAY:
            first = x.i[0]
            if first.type != StorageType.INTEGER:
                return Error('invalid argument type')
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y
                if last.type != StorageType.INTEGER:
                    return Error('invalid argument type')
                if first.i <= last.i:
                    results.append(MixedArray(self.i[first.i:last.i]))
                else:
                    return Error('invalid argument value')
            return MixedArray(results)

    def replicate(self, x):
        if x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    results = results + ([y]*z)
                return MixedArray(results)
            else:
                return Error('invalid argument value')
        else:
            return Error('unsupported argument type')

    def transpose(self):
        if len(self.i) == 0:
            return self
        elif all(map(lambda y: y.type == StorageType.INTEGER_ARRAY, self.i)):
            zipped = list(zip(*[y.i for y in self.i]))
            arrays = [IntegerArray(list(y)) for y in zipped]
            return MixedArray(arrays)
        elif all(map(lambda y: y.type == StorageType.FLOAT_ARRAY, self.i)):
            zipped = list(zip(*[y.i for y in self.i]))
            arrays = [FloatArray(list(y)) for y in zipped]
            return MixedArray(arrays)
        else:
            return Error('unsupported argument type')

    def amend(self, x):
        if x.type == StorageType.INTEGER:
            return Error('invalid argument type')
        elif x.type == StorageType.FLOAT:
            return Error('invalid argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == len(x.i):
                return Dictionary(self, x)
            else:
                return Error('invalid argument value')

    def floor(self):
        return MixedArray([x.floor() for x in self.i])

    def count(self):
        return Integer(len(self.i))

    def reverse(self):
        return MixedArray(list(reversed(self.i)))

    def first(self):
        if len(self.i) == 0:
            return Error('empty')
        else:
            return self.i[0]

    def shape(self):
        return MixedArray([x.shape() for x in self.i])

    def enclose(self):
        return MixedArray([self])

    def unique(self):
        return MixedArray(list(dict.fromkeys(self.i)))

    def gradeUp(self):
        return IntegerArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    def gradeDown(self):
        return self.gradeUp().reverse()

    def group(self):
        keys = self.unique()
        values = []
        for key in keys.i:
            indexes = []
            for index in range(len(self.i)):
                if self.i[index] == key:
                    indexes.append(index + 1)
            values.append(IntegerArray(indexes))
        return Dictionary(keys, MixedArray(values))

class Error(Storage):
    def __init__(self, x):
        super().__init__(x, StorageType.ERROR)

    def dyad(self, x, rop, op):
        return self

class Dictionary:
    def __init__(self, keys, values):
        self.map = {}
        if keys.type == StorageType.INTEGER_ARRAY:
            for index, key in enumerate(keys.i):
                value = values.index(Integer(index + 1))
                self.map[Integer(key)] = value
        elif keys.type == StorageType.FLOAT_ARRAY:
            for index, key in enumerate(keys.i):
                value = values.index(Integer(index + 1))
                self.map[Integer(key)] = value
        if keys.type == StorageType.MIXED_ARRAY:
            for index, key in enumerate(keys.i):
                value = values.index(Integer(index + 1))
                self.map[key] = value

    def __eq__(self, x):
        if not isinstance(x, Dictionary):
            return False
        return self.map == x.map

    def __str__(self):
        result = "{"
        for key, value in self.map.items():
            result += str(key) + ":" + str(value) + ", "
        result += "}"
        return result

    def get(self, key):
        if key in self.map:
            return self.map[key]
        else:
            return Error('unknown key')

    def put(self, key, value):
        newMap = self.map.copy()
        newMap[key] = value
        keys = []
        values = []
        for key, value in newMap.items():
            keys.append(key)
            values.append(value)
        if all(map(lambda y: y.type == StorageType.INTEGER, keys)):
            if all(map(lambda y: y.type == StorageType.INTEGER, values)):
                return Dictionary(IntegerArray([y.i for y in keys]), IntegerArray([y.i for y in values]))
            elif all(map(lambda y: y.type == StorageType.FLOAT, values)):
                return Dictionary(IntegerArray([y.i for y in keys]), FloatArray([y.i for y in values]))
            else:
                return Dictionary(IntegerArray(keys), MixedArray(values))
        elif all(map(lambda y: y.type == StorageType.FLOAT, keys)):
            if all(map(lambda y: y.type == StorageType.INTEGER, values)):
                return Dictionary(FloatArray([y.i for y in keys]), IntegerArray([y.i for y in values]))
            elif all(map(lambda y: y.type == StorageType.FLOAT, values)):
                return Dictionary(FloatArray([y.i for y in keys]), FloatArray([y.i for y in values]))
            else:
                return Dictionary(FloatArray([y.i for y in keys]), MixedArray(values))
        else:
            if all(map(lambda y: y.type == StorageType.INTEGER, values)):
                return Dictionary(MixedArray(keys), IntegerArray([y.i for y in values]))
            elif all(map(lambda y: y.type == StorageType.FLOAT, values)):
                return Dictionary(MixedArray(keys), FloatArray([y.i for y in values]))
            else:
                return Dictionary(MixedArray(keys), MixedArray(values))

    def contains(self, key):
        if key in self.map:
            return Integer(1)
        else:
            return Integer(0)

    def remove(self, key):
        pairs = self.items()
        transposed = pairs.transpose()
        keys = transposed.index(Integer(1))
        values = transposed.index(Integer(2))
        if keys.type == StorageType.INTEGER_ARRAY:
            index = keys.i.index(key.i)
            if index == -1:
                return Error('unknown key')
            del keys.i[index]
            del values.i[index]
            return Dictionary(keys, values)
        elif keys.type == StorageType.FLOAT_ARRAY:
            index = keys.i.index(key.i)
            if index == -1:
                return Error('unknown key')
            del keys.i[index]
            del values.i[index]
            return Dictionary(keys, values)
        elif keys.type == StorageType.MIXED_ARRAY:
            index = keys.i.index(key)
            if index == -1:
                return Error('unknown key')
            del keys.i[index]
            del values.i[index]
            return Dictionary(keys, values)
        else:
            return Error('unsupported type')

        del keys.i[index]
        del values.i[index]
        return Dictionary(keys, values)

    def keys(self):
        result = self.map.keys()
        if all(map(lambda y: y.type == StorageType.INTEGER, result)):
            return IntegerArray([y.i for y in result])
        elif all(map(lambda y: y.type == StorageType.FLOAT, result)):
            return FloatArray([y.i for y in result])
        else:
            return MixedArray(result)

    def values(self):
        result = self.map.values()
        if all(map(lambda y: y.type == StorageType.INTEGER, result)):
            return IntegerArray([y.i for y in result])
        elif all(map(lambda y: y.type == StorageType.FLOAT, result)):
            return FloatArray([y.i for y in result])
        else:
            return MixedArray(result)

    def items(self):
        results = []
        for key, value in self.map.items():
            if key.type == StorageType.INTEGER and value.type == StorageType.INTEGER:
                results.append(IntegerArray([key.i, value.i]))
            elif key.type == StorageType.FLOAT and value.type == StorageType.FLOAT:
                results.append(FloatArray([key.i, value.i]))
            else:
                results.append(MixedArray([key, value]))
        return MixedArray(results)
