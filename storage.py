import struct
from abc import abstractmethod
from enum import Enum
import math

from traitlets import Int

from squeeze import squeeze, expand

class StorageMonads(Enum):
    atom = 0
    complementation = 1
    enclose = 2
    enumerate = 3
    first = 4
    floor = 5
    gradeDown = 6
    gradeUp = 7
    group = 8
    negate = 9
    reciprocal = 11
    reverse = 12
    shape = 13
    size = 14
    transpose = 15
    unique = 16
    count = 17

class StorageDyads(Enum):
    amend = 117
    cut = 118
    divide = 119
    drop = 120
    equal = 121
    expand = 122
    find = 123
    index = 124
    join = 125
    less = 126
    match = 127
    max = 128
    min = 129
    minus = 130
    more = 131
    plus = 132
    power = 133
    remainder = 135
    reshape = 136
    rotate = 137
    split = 138
    take = 139
    times = 140

class StorageAdverbs(Enum):
    each = 41
    each2 = 42
    eachLeft = 43
    eachRight = 44
    eachPair = 45
    over = 46
    overNeutral = 47
    converge = 48
    whileOne = 49
    iterate = 50
    scanOver = 51
    scanOverNeutral = 52
    scanConverging = 53
    scanWhileOne = 54
    scanIterating = 55

class IStorageRegisterNetwork:
    @staticmethod
    def allocate(i):
        return IStorageRegisterNetwork(StorageRegister.allocate(i))

    @staticmethod
    def allocateZero():
        return IStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))

    def __init__(self, ir):
        self.ir = ir

    def dispatchMonad(self, f):
        return self.ir.dispatchMonad(f)

    def dispatchDyad(self, f, x):
        return self.ir.dispatchDyad(f, x)

class FStorageRegisterNetwork:
    @staticmethod
    def allocate(f):
        return FStorageRegisterNetwork(StorageRegister.allocate(f))

    def __init__(self, fr):
        self.fr = fr

    def dispatchMonad(self, i):
        f = self.fr.i
        return i.dispatchMonad(f)

    def dispatchDyad(self, i, x):
        f = self.fr.i
        return i.dispatchDyad(f, x)

class XStorageRegisterNetwork:
    @staticmethod
    def allocate(x):
        return XStorageRegisterNetwork(StorageRegister.allocate(x))

    @staticmethod
    def allocateZero():
        return XStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))

    def __init__(self, xr):
        self.xr = xr

    def dispatchDyad(self, i, f):
        x = self.xr.i
        return i.dispatchDyad(f, x)

class RStorageRegisterNetwork:
    @staticmethod
    def allocate(r):
        return RStorageRegisterNetwork(StorageRegister.allocate(r))

    @staticmethod
    def allocateZero():
        return RStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))

    def __init__(self, r):
        self.r = r

    def dispatchMonad(self, i, f):
        self.r.i = i.dispatchMonad(f)

    def dispatchDyad(self, i, f, x):
        self.r.i = i.dispatchDyad(f, x)

class IFStorageRegisterNetwork:
    @staticmethod
    def allocate(i, f):
        return IFStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f))

    @staticmethod
    def allocateZero(f):
        return IFStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(f))

    def __init__(self, ir, fr):
        self.ir = ir
        self.fr = fr

    def dispatchMonad(self):
        i = self.ir.i
        f = self.fr.i
        return i.dispatchMonad(f)

    def dispatchDyad(self, x):
        i = self.ir.i
        f = self.fr.i
        return i.dispatchDyad(f, x)

class IXStorageRegisterNetwork:
    @staticmethod
    def allocate(i, x):
        return IXStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(x))

    @staticmethod
    def allocateZeros():
        return IXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, xr):
        self.ir = ir
        self.xr = xr

    def dispatchMonad(self, f):
        i = self.ir.i
        return i.dispatchMonad(f)

    def dispatchDyad(self, f):
        i = self.ir.i
        x = self.xr.i
        return i.dispatchDyad(f, x)

class IRStorageRegisterNetwork:
    @staticmethod
    def allocate(i, r):
        return IRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return IRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, rr):
        self.ir = ir
        self.rr = rr

    def dispatchMonad(self, f):
        i = self.ir.i
        self.ir.i = i.dispatchMonad(f)

    def dispatchDyad(self, f, x):
        i = self.ir.i
        self.ir.i = i.dispatchDyad(f, x)

class FXStorageRegisterNetwork:
    @staticmethod
    def allocate(f, x):
        return FXStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(x))

    @staticmethod
    def allocateZeros():
        return FXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, fr, xr):
        self.fr = fr
        self.xr = xr

    def dispatchMonad(self, i):
        f = self.fr.i
        return i.dispatchDyad(f)

    def dispatchDyad(self, i, x):
        f = self.fr.i
        return i.dispatchDyad(f, x)

class FRStorageRegisterNetwork:
    @staticmethod
    def allocate(f, r):
        return FRStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return FRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, fr, rr):
        self.fr = fr
        self.rr = rr

    def dispatchMonad(self, i):
        f = self.fr.i
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self, i, x):
        f = self.fr.i
        self.rr.i = i.dispatchDyad(f, x)

class XRStorageRegisterNetwork:
    @staticmethod
    def allocate(x, r):
        return XRStorageRegisterNetwork(StorageRegister.allocate(x), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return XRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, xr, rr):
        self.xr = xr
        self.rr = rr

    def dispatchMonad(self, i, f):
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self, i, f):
        x = self.xr.i
        self.rr.i = i.dispatchDyad(f, x)

class IFXStorageRegisterNetwork:
    @staticmethod
    def allocate(i, f, x):
        return IFXStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(x))

    @staticmethod
    def allocateZeros():
        return IFXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, fr, xr):
        self.ir = ir
        self.fr = fr
        self.xr = xr

    def dispatchMonad(self):
        i = self.ir.i
        f = self.fr.i
        return i.dispatchMonad(f)

    def dispatchDyad(self):
        i = self.ir.i
        f = self.fr.i
        x = self.xr.i
        return i.dispatchDyad(f, x)

class IFRStorageRegisterNetwork:
    @staticmethod
    def allocate(i, f, r):
        return IFRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return IFRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, fr, rr):
        self.ir = ir
        self.fr = fr
        self.rr = rr

    def dispatchMonad(self):
        i = self.ir.i
        f = self.fr.i
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self, x):
        i = self.ir.i
        f = self.fr.i
        self.rr.i = i.dispatchDyad(f, x)

class IXRStorageRegisterNetwork:
    @staticmethod
    def allocate(i, x, r):
        return IXRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(x), StorageRegister.allocate(r))

    @staticmethod
    def allocateZero():
        return IXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, xr, rr):
        self.ir = ir
        self.xr = xr
        self.rr = rr

    def dispatchMonad(self, f):
        i = self.ir.i
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self, f):
        i = self.ir.i
        x = self.xr.i
        self.rr.i = i.dispatchDyad(f, x)

class FXRStorageRegisterNetwork:
    @staticmethod
    def allocate(f, x, r):
        return FXRStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(x), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return FXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, fr, xr, rr):
        self.fr = fr
        self.xr = xr
        self.rr = rr

    def dispatchMonad(self, i):
        f = self.fr.i
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self, i):
        f = self.fr.i
        x = self.xr.i
        self.rr.i = i.dispatchDyad(f, x)

class IFXRStorageRegisterNetwork:
    @staticmethod
    def allocate(i, f, x, r):
        return IFXRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(x), StorageRegister.allocate(r))

    @staticmethod
    def allocateZeros():
        return IFXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))

    def __init__(self, ir, fr, xr, rr):
        self.ir = ir
        self.fr = fr
        self.xr = xr
        self.rr = rr

    def dispatchMonad(self):
        i = self.ir.i
        f = self.fr.i
        self.rr.i = i.dispatchMonad(f)

    def dispatchDyad(self):
        i = self.ir.i
        f = self.fr.i
        x = self.xr.i
        self.rr.i = i.dispatchDyad(f, x)

class StorageRegister:
    @staticmethod
    def allocate(i):
        return StorageRegister(i)

    @staticmethod
    def allocateDispatchDyad(i, f, x):
        StorageRegister.allocate(i).dispatchDyad(f, x)

    def __init__(self, i):
        self.i = i

    def store(self, i):
        self.i = i

    def fetch(self):
        return self.i

    def dispatchMonad(self, f):
        return self.i.dispatchMonad(f)

    def dispatchDyad(self, f, x):
        return self.i.dispatchDyad(f, x)

class StorageType(Enum):
    INTEGER = 0
    FLOAT = 1
    INTEGER_ARRAY = 2 # all integers
    FLOAT_ARRAY = 3 # all floats
    MIXED_ARRAY = 4 # array of storage types
    ERROR = 5

class Storage:
    @staticmethod
    def addStatic(x, y):
        return x.plus(y)

    @staticmethod
    def subtractStatic(x, y):
        return x.minus(y)

    @staticmethod
    def multiplyStatic(x, y):
        return x.times(y)

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

    @staticmethod
    def from_bytes(data):
        length, typedRest = expand(data)
        typedData = typedRest[:length]
        typedRest = typedRest[length:]

        typeBytes = typedData[0:1]
        untypedData = typedData[1:]

        typeInt = struct.unpack("B", typeBytes)[0]
        storageType = StorageType(typeInt)

        if storageType == StorageType.INTEGER:
            result, integerRest = Integer.from_bytes(untypedData)
            return result, integerRest + typedRest
        elif storageType == StorageType.FLOAT:
            return Float.from_bytes(untypedData), typedRest
        elif storageType == StorageType.INTEGER_ARRAY:
            result, integerArrayRest = IntegerArray.from_bytes(untypedData)
            return result, integerArrayRest + typedRest
        elif storageType == StorageType.FLOAT_ARRAY:
            return FloatArray.from_bytes(untypedData), typedRest
        elif storageType == StorageType.MIXED_ARRAY:
            result, mixedArrayRest = MixedArray.from_bytes(untypedData)
            return result, mixedArrayRest + typedRest

    def __init__(self, x, t):
        self.i = x
        self.type = t

    def __eq__(self, x):
        if self.type != x.type:
            return False

        return self.i == x.i

    def __hash__(self):
        return hash(self.i)

    def dispatchMonad(self, f):
        # Determine if we have a verb or an adverb-verb pair
        if f.type == StorageType.INTEGER:
            if f.i == StorageMonads.atom.value:
                return self.atom()
            elif f.i == StorageMonads.complementation.value:
                return self.complementation()
            elif f.i == StorageMonads.enclose.value:
                return self.enclose()
            elif f.i == StorageMonads.enumerate.value:
                return self.enumerate()
            elif f.i == StorageMonads.first.value:
                return self.first()
            elif f.i == StorageMonads.floor.value:
                return self.floor()
            elif f.i == StorageMonads.gradeDown.value:
                return self.gradeDown()
            elif f.i == StorageMonads.gradeUp.value:
                return self.gradeUp()
            elif f.i == StorageMonads.group.value:
                return self.group()
            elif f.i == StorageMonads.negate.value:
                return self.negate()
            elif f.i == StorageMonads.reciprocal.value:
                return self.reciprocal()
            elif f.i == StorageMonads.reverse.value:
                return self.reverse()
            elif f.i == StorageMonads.shape.value:
                return self.shape()
            elif f.i == StorageMonads.size.value:
                return self.size()
            elif f.i == StorageMonads.transpose.value:
                return self.transpose()
            elif f.i == StorageMonads.unique.value:
                return self.unique()
            elif f.i == StorageMonads.count.value:
                return self.count()
            else:
                return Error("unknown monad %d" % f.i)
        elif f.type == StorageType.INTEGER_ARRAY:
            adverb = f.index(Integer(1))
            f = f.index(Integer(2))

            if adverb.i == StorageAdverbs.each.value:
                return self.each(f)
            elif adverb.i == StorageAdverbs.eachPair.value:
                return self.eachPair(f)
            elif adverb.i == StorageAdverbs.over.value:
                return self.over(f)
            elif adverb.i == StorageAdverbs.converge.value:
                return self.converge(f)
            elif adverb.i == StorageAdverbs.scanOver.value:
                return self.scanOver(f)
            elif adverb.i == StorageAdverbs.scanConverging.value:
                return self.scanConverging(f)
            elif adverb.i == StorageAdverbs.scanWhileOne.value:
                return self.scanConverging(f)
            else:
                return Error('unknown adverb')
        else:
            return Error('invalid function storage type')

    def dispatchDyad(self, f, x):
        # Determine if we have a verb or an adverb-verb pair
        if f.type == StorageType.INTEGER:
            if f.i == StorageDyads.amend.value:
                return self.amend(x)
            elif f.i == StorageDyads.cut.value:
                return self.cut(x)
            elif f.i == StorageDyads.divide.value:
                return self.divide(x)
            elif f.i == StorageDyads.drop.value:
                return self.drop(x)
            elif f.i == StorageDyads.equal.value:
                return self.equal(x)
            elif f.i == StorageDyads.expand.value:
                return self.expand(x)
            elif f.i == StorageDyads.find.value:
                return self.find(x)
            elif f.i == StorageDyads.index.value:
                return self.index(x)
            elif f.i == StorageDyads.join.value:
                return self.join(x)
            elif f.i == StorageDyads.less.value:
                return self.less(x)
            elif f.i == StorageDyads.match.value:
                return self.match(x)
            elif f.i == StorageDyads.max.value:
                return self.max(x)
            elif f.i == StorageDyads.min.value:
                return self.min(x)
            elif f.i == StorageDyads.minus.value:
                return self.minus(x)
            elif f.i == StorageDyads.more.value:
                return self.more(x)
            elif f.i == StorageDyads.plus.value:
                return self.plus(x)
            elif f.i == StorageDyads.power.value:
                return self.power(x)
            elif f.i == StorageDyads.remainder.value:
                return self.remainder(x)
            elif f.i == StorageDyads.reshape.value:
                return self.reshape(x)
            elif f.i == StorageDyads.rotate.value:
                return self.rotate(x)
            elif f.i == StorageDyads.split.value:
                return self.split(x)
            elif f.i == StorageDyads.take.value:
                return self.take(x)
            elif f.i == StorageDyads.times.value:
                return self.times(x)
            else:
                return Error("unknown dyad")
        elif f.type == StorageType.INTEGER_ARRAY:
            adverb = f.index(Integer(1))
            f = f.index(Integer(2))

            if adverb.i == StorageAdverbs.each2.value:
                return self.each2(f, x)
            elif adverb.i == StorageAdverbs.eachLeft.value:
                return self.eachLeft(f, x)
            elif adverb.i == StorageAdverbs.eachRight.value:
                return self.eachRight(f, x)
            elif adverb.i == StorageAdverbs.overNeutral.value:
                return self.overNeutral(f, x)
            elif adverb.i == StorageAdverbs.whileOne.value:
                return self.whileOne(f, x)
            elif adverb.i == StorageAdverbs.iterate.value:
                return self.iterate(f, x)
            elif adverb.i == StorageAdverbs.scanOverNeutral.value:
                return self.scanOverNeutral(f, x)
            elif adverb.i == StorageAdverbs.scanIterating.value:
                return self.scanIterating(f, x)
            else:
                return Error('unknown adverb')
        else:
            return Error('invalid function storage type')

    def converge(self, f):
        current = self
        nextValue = current.dispatchMonad(f)
        while nextValue.match(current) != Integer.true():
            current = nextValue
            nextValue = current.dispatchMonad(f)
        return current

    def whileOne(self, f, x):
        current = self
        truth = current.dispatchMonad(f)
        while truth == Integer(1):
            current = current.dispatchMonad(x)
            truth = current.dispatchMonad(f)
        return current

    def scanConverging(self, f):
        current = self
        results = [current]
        nextValue = current.dispatchMonad(f)
        while nextValue.match(current) != Integer.true():
            current = nextValue
            results.append(current)
            nextValue = current.dispatchMonad(f)
        return MixedArray(results)

    def scanWhileOne(self, f, x):
        current = self
        results = [current]
        truth = current.dispatchMonad(f)
        while truth == Integer(1):
            current = current.dispatchMonad(x)
            truth = current.dispatchMonad(f)
            results.append(current)
        return MixedArray(results)

    def scanIterating(self, f, x):
        if x.type == StorageType.INTEGER:
            if x.i >= 0:
                current = self
                truth = x
                results = [current]
                while truth != Integer(0):
                    current = current.dispatchMonad(f)
                    truth = truth.minus(Integer(1))
                    results.append(current)
                return MixedArray(results)
            else:
                return Error('invalid adverb argument')
        else:
            return Error('invalid adverb argument')

    def plus(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            return self.dyad(x, self.addStatic, self._add)

    def minus(self, x):
        if x.type == StorageType.ERROR:
            return x
        else:
            return self.dyad(x, self.subtractStatic, self._subtract)

    def times(self, x):
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
        return Integer(0).minus(self)

    def reciprocal(self):
        return Float(1).divide(self)

    def complementation(self):
        return Integer(1).minus(self)

    # Monads
    @abstractmethod
    def monad(self, rop, op):
        pass

    @abstractmethod
    def dyad(self, x, rop, op):
        pass

    @abstractmethod
    def atom(self):
        pass

    @abstractmethod
    def enclose(self):
        pass

    @abstractmethod
    def enumerate(self):
        pass

    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def floor(self):
        pass

    @abstractmethod
    def gradeDown(self):
        pass

    @abstractmethod
    def gradeUp(self):
        pass

    @abstractmethod
    def group(self):
        pass

    @abstractmethod
    def reverse(self):
        pass

    @abstractmethod
    def shape(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def transpose(self):
        pass

    @abstractmethod
    def count(self):
        pass

    @abstractmethod
    def unique(self):
        pass

    # Dyads
    @abstractmethod
    def amend(self, x):
        pass

    @abstractmethod
    def cut(self, x):
        pass

    @abstractmethod
    def drop(self, x):
        pass

    @abstractmethod
    def equal(self, x):
        pass

    @abstractmethod
    def expand(self, x):
        pass

    @abstractmethod
    def find(self, x):
        pass

    @abstractmethod
    def index(self, x):
        pass

    @abstractmethod
    def join(self, x):
        pass

    @abstractmethod
    def less(self, x):
        pass

    @abstractmethod
    def match(self, x):
        pass

    @abstractmethod
    def max(self, x):
        pass

    @abstractmethod
    def min(self, x):
        pass

    @abstractmethod
    def more(self, x):
        pass

    @abstractmethod
    def power(self, x):
        pass

    @abstractmethod
    def remainder(self, x):
        pass

    @abstractmethod
    def reshape(self, x):
        pass

    @abstractmethod
    def rotate(self, x):
        pass

    @abstractmethod
    def split(self, x):
        pass

    @abstractmethod
    def take(self, x):
        pass

    # Adverbs
    @abstractmethod
    def each(self, f):
        pass

    @abstractmethod
    def each2(self, f, x):
        pass

    @abstractmethod
    def eachLeft(self, f, x):
        pass

    @abstractmethod
    def eachRight(self, f, x):
        pass

    @abstractmethod
    def eachPair(self, f):
        pass

    @abstractmethod
    def over(self, f):
        pass

    @abstractmethod
    def overNeutral(self, f, x):
        pass

    @abstractmethod
    def scanOver(self, f):
        pass

    @abstractmethod
    def iterate(self, f, x):
        pass

    @abstractmethod
    def scanOverNeutral(self, f, x):
        pass

class Integer(Storage):
    @staticmethod
    def true():
        return Integer(1)

    @staticmethod
    def false():
        return Integer(0)

    @staticmethod
    def from_bytes(data):
        i, rest = expand(data)
        return Integer(i), rest

    def __init__(self, x):
        super().__init__(int(x), StorageType.INTEGER)

    def __str__(self):
        return "I%s" % str(self.i)

    def __lt__(self, x):
        if x.type == StorageType.INTEGER:
            return self.less(x) == Integer(1)
        elif x.type == StorageType.FLOAT:
            return self.less(x) == Integer(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.type.value)
        intBytes = squeeze(self.i)
        data = typeBytes + intBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    def monad(self, rop, op):
        return Integer(op(self.i))

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return Integer(op(self.i, x.i))
        elif x.type == StorageType.FLOAT:
            return Float(op(float(self.i), x.i))
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([op(self.i, y) for y in x.i]) # flipped map
        elif x.type == StorageType.FLOAT_ARRAY:
            return FloatArray([op(float(self.i), y) for y in x.i]) # flipped map
        elif x.type == StorageType.MIXED_ARRAY:
            return x.apply(self, rop)

    def each(self, f):
        return self.dispatchMonad(f)

    def each2(self, f, x):
        return self.dispatchDyad(f, x)

    def eachLeft(self, f, x):
        return self.dispatchDyad(f, x)

    def eachRight(self, f, x):
        return self.dispatchDyad(f, x)

    def over(self, f):
        return self

    def overNeutral(self, f, x):
        return self.dispatchDyad(f, x)

    def iterate(self, f, x):
        if x.i >= 0:
            current = self
            truth = x
            while truth != Integer(0):
                current = current.dispatchMonad(f)
                truth = truth.minus(Integer(1))
            return current
        else:
            return Error('invalid adverb argument')

    def scanOver(self, f):
        return IntegerArray([self.i])

    def scanOverNeutral(self, f, x):
        return MixedArray([x] + [self.dispatchDyad(f, x)])

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
                return Integer.true()
            else:
                return Integer.false()
        elif x.type == StorageType.FLOAT:
            diff = abs(float(self.i) - x.i)
            if diff < Float.tolerance():
                return Integer.true()
            else:
                return Integer.false()
        else:
            return Integer.false()

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
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
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
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
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
            return Error('unsupported argument type')

    def enumerate(self):
        return IntegerArray(list(range(1, self.i+1)))

    def floor(self):
        return self

    def count(self):
        return Integer(abs(self.i))

    def shape(self):
        return Integer(0)

    def enclose(self):
        return IntegerArray([self.i])

    def atom(self):
        return Integer.true()

    # Unsupported
    def first(self):
        return Error('unsupported subject type')

    def gradeDown(self):
        return Error('unsupported subject type')

    def gradeUp(self):
        return Error('unsupported subject type')

    def group(self):
        return Error('unsupported subject type')

    def reverse(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def transpose(self):
        return Error('unsupported subject type')

    def unique(self):
        return Error('unsupported subject type')

    def drop(self, x):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def take(self, x):
        return Error('unsupported subject type')

    def eachPair(self, f):
        return Error('unsupported subject type')

class Float(Storage):
    @staticmethod
    def tolerance():
        return 1e-14

    @staticmethod
    def from_bytes(data):
        i = struct.unpack('f', data)
        return Float(i[0])

    def __init__(self, x):
        super().__init__(float(x), StorageType.FLOAT)

    def __str__(self):
        return "F%s" % str(self.i)

    def __lt__(self, x):
        if x.type == StorageType.INTEGER:
            return self.less(x) == Integer(1)
        elif x.type == StorageType.FLOAT:
            return self.less(x) == Integer(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.type.value)
        floatBytes = struct.pack("f", self.i)
        data = typeBytes + floatBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

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

    def each(self, f):
        return self.dispatchMonad(f)

    def each2(self, f, x):
        return self.dispatchDyad(f, x)

    def eachLeft(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachRight(self, f, x):
        return self.dispatchDyad(f, x)

    def over(self, f):
        return self

    def overNeutral(self, f, x):
        return self.dispatchDyad(f, x)

    def scanOver(self, f):
        return FloatArray([self.i])

    def scanOverNeutral(self, f, x):
        return MixedArray([x] + [self.dispatchDyad(f, x)])

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
            diff = abs(self.i - float(x.i))
            if diff < Float.tolerance():
                return Integer.true()
            else:
                return Integer.false()
        elif x.type == StorageType.FLOAT:
            diff = abs(self.i - x.i)
            if diff < Float.tolerance():
                return Integer.true()
            else:
                return Integer.false()
        else:
            return Integer.false()

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
            return Error('unsupported argument type')
        elif x.type == StorageType.FLOAT:
            return Error('unsupported argument type')
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
            return Error('unsupported argument type')

    def floor(self):
        return Integer(math.floor(self.i))

    def count(self):
        return Float(abs(self.i))

    def shape(self):
        return Integer(0)

    def enclose(self):
        return FloatArray([self.i])

    def atom(self):
        return Integer.true()

    # Unsupported
    def enumerate(self):
        return Error('unsupported subject type')

    def first(self):
        return Error('unsupported subject type')

    def gradeDown(self):
        return Error('unsupported subject type')

    def gradeUp(self):
        return Error('unsupported subject type')

    def group(self):
        return Error('unsupported subject type')

    def reverse(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def transpose(self):
        return Error('unsupported subject type')

    def unique(self):
        return Error('unsupported subject type')

    def cut(self, x):
        return Error('unsupported subject type')

    def drop(self, x):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def remainder(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def rotate(self, x):
        return Error('unsupported subject type')

    def take(self, x):
        return Error('unsupported subject type')

    def eachPair(self, f):
        return Error('unsupported subject type')

    def iterate(self, f, x):
        return Error('unsupported subject type')


class IntegerArray(Storage):
    @staticmethod
    def from_bytes(data):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = expand(rest)
            results.append(result)
        return IntegerArray(results), rest

    def __init__(self, x):
        super().__init__([int(y) for y in x], StorageType.INTEGER_ARRAY)

    def __str__(self):
        return "I%s" % str(self.i)

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.type.value)

        intArrayBytes = b''
        for y in self.i:
            intArrayBytes += squeeze(y)

        data = typeBytes + intArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

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

    def each(self, f):
        return MixedArray([Integer(y).dispatchMonad(f) for y in self.i])

    def each2(self, f, x):
        if x.type == StorageType.INTEGER:
            return MixedArray([Integer(y).dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.FLOAT:
            return MixedArray([Integer(y).dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            #FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [Integer(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            #FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [Float(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            #FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [z for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)

    def eachLeft(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachPair(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append(Integer(y).dispatchDyad(f, Integer(z)))
        return MixedArray(results)

    def eachRight(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def over(self, f):
        if len(self.i) == 0:
            return self
        elif len(self.i) == 1:
            return self
        else:
            accumulator = 0
            for index, y in enumerate(self.i):
                if index == 0:
                    accumulator = Integer(y)
                else:
                    accumulator = accumulator.dispatchDyad(f, Integer(y))
            return accumulator

    def overNeutral(self, f, x):
        if len(self.i) == 0:
            return Error('empty array')
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = accumulator.dispatchDyad(f, Integer(y))
            return accumulator

    def scanOver(self, f):
        if len(self.i) == 0:
            return IntegerArray([])
        else:
            current = Integer(self.i[0])
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = current.dispatchDyad(f, Integer(y))
                results.append(current)
            return MixedArray(results)

    def scanOverNeutral(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = current.dispatchDyad(f, Integer(y))
            results.append(current)
        return MixedArray(results)

    def take(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return Error('out of bounds')
            elif x.i == 0:
                return IntegerArray([])
            elif 1 <= x.i <= len(self.i):
               return IntegerArray(self.i[:x.i])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
                return IntegerArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return IntegerArray(results)
            else: # x.i < 0 and abs(x.i) > len(self.i)
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.FLOAT:
            if x.match(Float(0.0)) == Integer.true():
                return IntegerArray([])
            elif x.match(Float(1.0)) == Integer.true():
                return self
            elif len(self.i) == 0:
                return self
            elif x.more(Float(0)) == Integer.true():
                if x.less(Float(1.0)) == Integer.true():
                    count = len(self.i)
                    extent = float(count) * x.i
                    lowIndex = int(extent)
                    return self.take(Integer(lowIndex))
                else: # x > 1.0
                    replication = int(x.i)
                    remainder = x.i - float(replication)
                    replicated = self.take(Integer(replication * len(self.i)))
                    remaindered = self.take(Float(remainder))
                    return replicated.join(remaindered)
            else: # x < 0
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.INTEGER_ARRAY:
                if len(x.i) == 0:
                    return IntegerArray([])
                else:
                    results = []
                    for y in x.i:
                        result = self.take(Integer(y))
                        if isinstance(result, Error):
                            return result
                        else:
                            results.append(result)
                    return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([])
            else:
                results = []
                for y in x.i:
                    results.append(self.take(Float(y)))
                return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([])
            else:
                results = []
                for y in x.i:
                    result = self.take(y)
                    if isinstance(result, Error):
                        return result
                    else:
                        results.append(result)
                return MixedArray(results)

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return IntegerArray([])
            elif 1 <= x.i <= len(self.i):
               return IntegerArray(self.i[x.i:])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            elif 1 <= x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            if 0 < x.i <= len(self.i):
                return MixedArray([IntegerArray(self.i[:x.i]), IntegerArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif 0.0 < x.i <= 1.0:
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
        if x.type == StorageType.INTEGER:
            return Integer.false()
        elif x.type == StorageType.FLOAT:
            return Integer.false()
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        if y != z:
                            return Integer.false()
                    return Integer.true()
                else:
                    return Integer.false()
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        diff = abs(float(y) - z)
                        if diff > Float.tolerance():
                            return Integer.false()
                    return Integer.true()
                else:
                    return Integer.false()
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            else:
                if len(self.i) == len(x.i):
                    zipped = zip(self.i, x.i)
                    for y, z in zipped:
                        if Float(y).match(z) != Integer.true():
                            return Integer.false()
                    return Integer.true()
                else:
                    return Integer.false()

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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = Integer(y)
                    for z in x.i:
                        result = result.min(Integer(z))
                    results.append(result.i)
                return IntegerArray(results)
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = Float(y)
                    for z in x.i:
                        result = result.min(Float(z))
                    results.append(result.i)
                return FloatArray(results)
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = Float(y)
                    for z in x.i:
                        result = result.min(z)
                    results.append(result)
                return MixedArray(results)
            else:
                return Error('unequal array lengths')

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
        if x.type == StorageType.INTEGER:
            return IntegerArray([Integer(y).more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([Integer(y).more(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([Integer(y).more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([Integer(y).more(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return IntegerArray([Integer(y).more(x).i for y in self.i])

    def equal(self, x):
        if x.type == StorageType.INTEGER:
            return IntegerArray([Integer(y).equal(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([Integer(y).equal(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                for y, z in zip(self.i, x.i):
                    if y == z:
                        results.append(1)
                    else:
                        results.append(0)
                return IntegerArray(results)
            else:
                return Error('mismatched shapes')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                for y, z in zip(self.i, x.i):
                    if Integer(y).equal(Float(z)) == Integer(1):
                        results.append(1)
                    else:
                        results.append(0)
                return IntegerArray(results)
            else:
                return Error('mismatched shapes')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == len(x.i):
                results = []
                for y, z in zip(self.i, x.i):
                    if Integer(y).equal(z) == Integer(1):
                        results.append(1)
                    else:
                        results.append(0)
                return IntegerArray(results)
            else:
                return Error('mismatched shapes')

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
            return Error('unsupported argument type')
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
        if len(self.i) == 0:
            return Integer(0)
        else:
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

    def atom(self):
        return Integer.false()

    # Unsupported
    def enumerate(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def transpose(self):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def iterate(self, f, x):
        if x.type == StorageType.INTEGER:
            if x.i >= 0:
                current = self
                truth = x
                while truth != Integer(0):
                    current = current.dispatchMonad(f)
                    truth = truth.minus(Integer(1))
                return current
            else:
                return Error('invalid adverb argument')
        else:
            return Error('unsupported argument type')

class FloatArray(Storage):
    @staticmethod
    def from_bytes(data):
        rest = data
        results = []
        while len(rest) > 0:
            data = rest[:4]
            rest = rest[4:]

            result = struct.unpack('f', data)[0]
            results.append(result)
        return FloatArray(results)

    def __init__(self, x):
        super().__init__(list(map(lambda y: float(y), x)), StorageType.FLOAT_ARRAY)

    def __str__(self):
        return "F%s" % str(self.i)

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.type.value)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += struct.pack("f", y)

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    def monad(self, rop, op):
        return FloatArray([op(x) for x in self.i])

    def dyad(self, x, rop, op):
        if x.type == StorageType.INTEGER:
            return FloatArray([op(y, float(x.i)) for y in self.i])
        elif x.type == StorageType.FLOAT:
            return FloatArray([op(y, x.i) for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([FloatArray([op(y, z) for z in x.i]) for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([FloatArray([op(float(y), z) for z in x.i]) for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([MixedArray([rop(Float(y), z) for z in x.i]) for y in self.i])

    def each(self, f):
        return MixedArray([Float(y).dispatchMonad(f) for y in self.i])

    def each2(self, f, x):
        if x.type == StorageType.INTEGER:
            return MixedArray([Float(y).dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.FLOAT:
            return MixedArray([Float(y).dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [Integer(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [Float(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip([Integer(y) for y in self.i], [z for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)

    def eachLeft(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachRight(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachPair(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append((Float(y).dispatchDyad(f, Float(z))))
        return MixedArray(results)

    def over(self, f):
        if len(self.i) == 0:
            return self
        elif len(self.i) == 1:
            return self
        else:
            accumulator = 0
            for index, y in enumerate(self.i):
                if index == 0:
                    accumulator = Float(y)
                else:
                    accumulator = accumulator.dispatchDyad(f, Float(y))
            return accumulator

    def overNeutral(self, f, x):
        if len(self.i) == 0:
            return Error('empty array')
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = accumulator.dispatchDyad(f, Float(y))
            return accumulator

    def scanOver(self, f):
        if len(self.i) == 0:
            return FloatArray([])
        else:
            current = Float(self.i[0])
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = current.dispatchDyad(f, Float(y))
                results.append(current)
            return MixedArray(results)

    def scanOverNeutral(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = current.dispatchDyad(f, Float(y))
            results.append(current)
        return MixedArray(results)

    def take(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return Error('out of bounds')
            elif x.i == 0:
                return FloatArray([])
            elif 1 <= x.i <= len(self.i):
               return FloatArray(self.i[:x.i])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
                return FloatArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return FloatArray(results)
            else:  # x.i < 0 and abs(x.i) > len(self.i)
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.FLOAT:
            if x.match(Float(0.0)) == Integer.true():
                return FloatArray([])
            elif x.match(Float(1.0)) == Integer.true():
                return self
            elif len(self.i) == 0:
                return self
            elif x.more(Float(0)) == Integer.true():
                if x.less(Float(1.0)) == Integer.true():
                    count = len(self.i)
                    extent = float(count) * x.i
                    lowIndex = int(extent)
                    return self.take(Integer(lowIndex))
                else: # x > 1.0
                    replication = int(x.i)
                    remainder = x.i - float(replication)
                    replicated = self.take(Integer(replication * len(self.i)))
                    remaindered = self.take(Float(remainder))
                    return replicated.join(remaindered)
            else: # x < 0
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return FloatArray([])
            else:
                results = []
                for y in x.i:
                    result = self.take(Integer(y))
                    if isinstance(result, Error):
                        return result
                    else:
                        results.append(result)
                return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return FloatArray([])
            else:
                results = []
                for y in x.i:
                    results.append(self.take(Float(y)))
                return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return Float([])
            else:
                results = []
                for y in x.i:
                    result = self.take(y)
                    if isinstance(result, Error):
                        return result
                    else:
                        results.append(result)
                return MixedArray(results)

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return FloatArray([])
            elif 1 <= x.i <= len(self.i):
               return FloatArray(self.i[x.i:])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            elif 1 <= x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            if 0 < x.i <= len(self.i):
                return MixedArray([FloatArray(self.i[:x.i]), FloatArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif 0.0 < x.i <= 1.0:
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
            return Integer.false()
        elif x.type == StorageType.FLOAT:
            return Integer.false()
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer.false()
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    diff = abs(y - float(z))
                    if diff > Float.tolerance():
                        return Integer.false()
                return Integer.true()
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer.false()
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    diff = abs(y - z)
                    if diff > Float.tolerance():
                        return Integer.false()
                return Integer.true()
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer(0)
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if Float(y).match(z) != Integer(1):
                        return Integer.false()
                return Integer.true()

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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
                maxy = float(y)
                for z in x.i:
                    maxy = max(maxy, float(z))
                results.append(maxy)
            return FloatArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            for y in self.i:
                maxy = y
                for z in x.i:
                    maxy = max(y, z)
                results.append(maxy)
            return FloatArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            for y in self.i:
                maxy = Float(y)
                for z in x.i:
                    maxy = maxy.max(z)
                results.append(maxy)
            return MixedArray(results)

    def min(self, x):
        if x.type == StorageType.INTEGER:
            results = []
            for y in self.i:
                if y - float(x.i) > Float.tolerance():
                    results.append(float(x.i))
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.FLOAT:
            results = []
            for y in self.i:
                if y - x.i > Float.tolerance():
                    results.append(float(x.i))
                else:
                    results.append(y)
            return FloatArray(results)
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                if len(self.i) == len(x.i):
                    for y, z in zip(self.i, x.i):
                        if y - float(z) > Float.tolerance():
                            results.append(float(z))
                        else:
                            results.append(y)
                    return FloatArray(results)
                else:
                    return Error('unequal array lengths')
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                if len(self.i) == len(x.i):
                    for y, z in zip(self.i, x.i):
                        if y - z > Float.tolerance():
                            results.append(float(z))
                        else:
                            results.append(y)
                    return FloatArray(results)
                else:
                    return Error('unequal array lengths')
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                if len(self.i) == len(x.i):
                    for y, z in zip(self.i, x.i):
                        results.append(Float(y).min(z))
                    return MixedArray(results)
                else:
                    return Error('unequal array lengths')
            else:
                return Error('unequal array lengths')

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
        if x.type == StorageType.INTEGER:
            return IntegerArray([Float(y).more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([Float(y).more(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([Float(y).more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([Float(y).more(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
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
            return Error('unsupported argument type')
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
        if len(self.i) == 0:
            return Integer(0)
        else:
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

    def atom(self):
        return Integer.false()

    # Unsupported
    def enumerate(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def transpose(self):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def remainder(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def iterate(self, f, x):
        if x.type == StorageType.INTEGER:
            if x.i >= 0:
                current = self
                truth = x
                while truth != Integer(0):
                    current = current.dispatchMonad(f)
                    truth = truth.minus(Integer(1))
                return current
            else:
                return Error('invalid adverb argument')
        else:
            return Error('unsupported argument type')

class MixedArray(Storage):
    @staticmethod
    def from_bytes(data):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = Storage.from_bytes(rest)
            results.append(result)
        return MixedArray(results), rest

    def __init__(self, x):
        super().__init__(x, StorageType.MIXED_ARRAY)

    def __str__(self):
        return "M[%s]" % ", ".join(list(map(lambda x: str(x), self.i)))

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.type.value)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += y.to_bytes()

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

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

    def each(self, f):
        return MixedArray([y.dispatchMonad(f) for y in self.i])

    def each2(self, f, x):
        if x.type == StorageType.INTEGER:
            return MixedArray([y.dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.FLOAT:
            return MixedArray([y.dispatchDyad(f, x) for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip(self.i, [Integer(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip(self.i, [Float(z) for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            results = []
            # FIXME - make this work for arrays on unequal lengths
            for y, z in zip(self.i, [z for z in x.i]):
                results.append(y.dispatchDyad(f, z))
            return MixedArray(results)

    def eachLeft(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachRight(self, f, x):
        if x.type == StorageType.INTEGER:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.FLOAT:
            return self.dispatchDyad(f, x)
        elif x.type == StorageType.INTEGER_ARRAY:
            return MixedArray([self.dispatchDyad(f, Integer(y)) for y in x.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return MixedArray([self.dispatchDyad(f, Float(y)) for y in x.i])
        elif x.type == StorageType.MIXED_ARRAY:
            return MixedArray([self.dispatchDyad(f, y) for y in x.i])

    def eachPair(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append(y.dispatchDyad(f, z))
        return MixedArray(results)

    def over(self, f):
        if len(self.i) == 0:
            return self
        elif len(self.i) == 1:
            return self
        else:
            accumulator = 0
            for index, y in enumerate(self.i):
                if index == 0:
                    accumulator = y
                else:
                    accumulator = accumulator.dispatchDyad(f, y)
            return accumulator

    def overNeutral(self, f, x):
        if len(self.i) == 0:
            return Error('empty array')
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = accumulator.dispatchDyad(f, y)
            return accumulator

    def scanOver(self, f):
        if len(self.i) == 0:
            return MixedArray([])
        else:
            current = self.i[0]
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = current.dispatchDyad(f, y)
                results.append(current)
            return MixedArray(results)

    def scanOverNeutral(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = current.dispatchDyad(f, y)
            results.append(current)
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
            elif 1 <= x.i <= len(self.i):
               return MixedArray(self.i[:x.i])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
                return MixedArray(self.i[-x.i:])
            elif x.i > len(self.i):
                copies = x.i // len(self.i)
                remainder = x.i % len(self.i)
                results = []
                for y in range(copies):
                    results = results + self.i
                results = results + self.take(Integer(remainder)).i
                return MixedArray(results)
            else:  # x.i < 0 and abs(x.i) > len(self.i)
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.FLOAT:
            if x.match(Float(0.0)) == Integer.true():
                return MixedArray([])
            elif x.match(Float(1.0)) == Integer.true():
                return self
            elif len(self.i) == 0:
                return self
            elif x.more(Float(0)) == Integer.true():
                if x.less(Float(1.0)) == Integer.true():
                    count = len(self.i)
                    extent = float(count) * x.i
                    lowIndex = int(extent)
                    return self.take(Integer(lowIndex))
                else: # x > 1.0
                    replication = int(x.i)
                    remainder = x.i - float(replication)
                    replicated = self.take(Integer(replication * len(self.i)))
                    remaindered = self.take(Float(remainder))
                    return replicated.join(remaindered)
            else: # x < 0
                return self.reverse().take(x.negate()).reverse()
        elif x.type == StorageType.INTEGER_ARRAY:
                if len(x.i) == 0:
                    return MixedArray([])
                else:
                    results = []
                    for y in x.i:
                        result = self.take(Integer(y))
                        if isinstance(result, Error):
                            return result
                        else:
                            results.append(result)
                    return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(x.i) == 0:
                return MixedArray([])
            else:
                results = []
                for y in x.i:
                    results.append(self.take(Float(y)))
                return MixedArray(results)
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return MixedArray([])
            else:
                results = []
                for y in x.i:
                    result = self.take(y)
                    if isinstance(result, Error):
                        return result
                    else:
                        results.append(result)
                return MixedArray(results)

    def drop(self, x):
        if x.type == StorageType.INTEGER:
            if len(self.i) == 0:
                return self
            elif x.i == 0:
                return self
            elif x.i >= len(self.i):
                return MixedArray([])
            elif 1 <= x.i <= len(self.i):
               return MixedArray(self.i[x.i:])
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            elif 1 <= x.i <= len(self.i):
                return self.drop(x).join(self.take(x))
            elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
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
            if 0 < x.i <= len(self.i):
                return MixedArray([MixedArray(self.i[:x.i]), MixedArray(self.i[x.i:])])
            else:
                return Error('out of bounds')
        elif x.type == StorageType.FLOAT:
            if x.i == 0.0:
                return IntegerArray([])
            elif 0.0 < x.i <= 1.0:
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
            return Integer.false()
        elif x.type == StorageType.FLOAT:
            return Integer.false()
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer.false()
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(Integer(z)) != Integer.true():
                        return Integer.false()
                return Integer.true()
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer.false()
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(Float(z)) != Integer.true():
                        return Integer.false()
                return Integer.true()
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                if len(x.i) == 0:
                    return Integer.true()
                else:
                    return Integer.false()
            elif len(self.i) != len(x.i):
                return Integer.false()
            else:
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y.match(z) != Integer.true():
                        return Integer.false()
                return Integer.true()

    def find(self, x):
        if len(self.i) == 0:
            return IntegerArray([])
        elif x.type == StorageType.INTEGER:
            return IntegerArray([y.match(x).i for  y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([y.match(x).i for  y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return IntegerArray([0] * len(self.i))
            else:
                results = []
                for offset in range(len(self.i)):
                    if len(self.i[offset:]) >= len(x.i):
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
                        arraySlice = self.i[offset:offset+len(x.i)]
                        zipped = zip(arraySlice, x.i)
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
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = y
                    for z in x.i:
                        result = result.min(Integer(z))
                    results.append(result)
                return MixedArray(results)
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.FLOAT_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = y
                    for z in x.i:
                        result = result.min(Float(z))
                    results.append(result)
                return MixedArray(results)
            else:
                return Error('unequal array lengths')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(self.i) == 0:
                return self
            elif len(self.i) == len(x.i):
                results = []
                for y in self.i:
                    result = y
                    for z in x.i:
                        result = result.min(z)
                    results.append(result)
                return MixedArray(results)
            else:
                return Error('unequal array lengths')

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
        if x.type == StorageType.INTEGER:
            return IntegerArray([y.more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT:
            return IntegerArray([y.more(x).i for y in self.i])
        elif x.type == StorageType.INTEGER_ARRAY:
            return IntegerArray([y.more(x).i for y in self.i])
        elif x.type == StorageType.FLOAT_ARRAY:
            return IntegerArray([y.more(x).i for y in self.i])
        elif x.type == StorageType.MIXED_ARRAY:
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
            return Error('unsupported argument type')
        elif x.type == StorageType.INTEGER_ARRAY:
            if len(x.i) == 0:
                return MixedArray([self])
            else:
                previous = None
                results = []
                for y in x.i:
                    if y >= 1:
                        if previous is None:
                            results.append(MixedArray(self.i[:y-1]))
                            previous = y
                        else:
                            if previous <= y:
                                results.append(MixedArray(self.i[previous-1:y-1]))
                                previous = y
                            else:
                                return Error('invalid argument value')
                    else:
                        return Error('invalid argument value')
                if previous is None:
                    return MixedArray(results)
                else:
                    results.append(MixedArray(self.i[previous-1:]))
                    return MixedArray(results)
        elif x.type == StorageType.FLOAT_ARRAY:
            return Error('invalid argument type')
        elif x.type == StorageType.MIXED_ARRAY:
            if len(x.i) == 0:
                return MixedArray([self])
            else:
                previous = None
                results = []
                for y in x.i:
                    if y.type == StorageType.INTEGER:
                        if y.i >= 1:
                            if previous is None:
                                results.append(MixedArray(self.i[:y.i-1]))
                                previous = y.i
                            else:
                                if previous <= y.i:
                                    results.append(MixedArray(self.i[previous-1:y.i-1]))
                                    previous = y.i
                                else:
                                    return Error('invalid argument value')
                        else:
                            return Error('invalid argument value')
                    else:
                        return Error('invalid argument value')

                if previous is None:
                    return MixedArray(results)
                else:
                    results.append(MixedArray(self.i[previous-1:]))
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
        if len(self.i) == 0:
            return Integer(0)
        else:
            shapes = [y.shape() for y in self.i]
            firstShape = shapes[0]
            if firstShape.type == StorageType.INTEGER: # atom in array means shape is simple vector type
                return IntegerArray([len(self.i)])
            elif firstShape.type == StorageType.INTEGER_ARRAY:
                for shape in shapes[1:]:
                    if shape != firstShape: # assorted internal shapes means shape is simple vector type
                        return IntegerArray([len(self.i)])
                return IntegerArray([len(self.i)] + firstShape.i) # identical internal shapes adds one layer to the shape vector

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

    def atom(self):
        return Integer.false()

    # Unsupported
    def enumerate(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def iterate(self, f, x):
        if x.type == StorageType.INTEGER:
            if x.i >= 0:
                current = self
                truth = x
                while truth != Integer(0):
                    current = current.dispatchMonad(f)
                    truth = truth.minus(Integer(1))
                return current
            else:
                return Error('invalid adverb argument')
        else:
            return Error('unsupported argument type')

class Error(Storage):
    def __init__(self, x):
        super().__init__(x, StorageType.ERROR)

    def monad(self, rop, op):
        return self

    def dyad(self, x, rop, op):
        return self

    def atom(self):
        return Integer.false()

    def enclose(self):
        return Error('unsupported subject type')

    def enumerate(self):
        return Error('unsupported subject type')

    def first(self):
        return Error('unsupported subject type')

    def floor(self):
        return Error('unsupported subject type')

    def gradeDown(self):
        return Error('unsupported subject type')

    def gradeUp(self):
        return Error('unsupported subject type')

    def group(self):
        return Error('unsupported subject type')

    def reverse(self):
        return Error('unsupported subject type')

    def shape(self):
        return Error('unsupported subject type')

    def size(self):
        return Error('unsupported subject type')

    def transpose(self):
        return Error('unsupported subject type')

    def count(self):
        return Error('unsupported subject type')

    def unique(self):
        return Error('unsupported subject type')

    def amend(self, x):
        return Error('unsupported subject type')

    def cut(self, x):
        return Error('unsupported subject type')

    def drop(self, x):
        return Error('unsupported subject type')

    def equal(self, x):
        return Error('unsupported subject type')

    def expand(self, x):
        return Error('unsupported subject type')

    def find(self, x):
        return Error('unsupported subject type')

    def index(self, x):
        return Error('unsupported subject type')

    def join(self, x):
        return Error('unsupported subject type')

    def less(self, x):
        return Error('unsupported subject type')

    def match(self, x):
        return Error('unsupported subject type')

    def max(self, x):
        return Error('unsupported subject type')

    def min(self, x):
        return Error('unsupported subject type')

    def more(self, x):
        return Error('unsupported subject type')

    def power(self, x):
        return Error('unsupported subject type')

    def remainder(self, x):
        return Error('unsupported subject type')

    def reshape(self, x):
        return Error('unsupported subject type')

    def rotate(self, x):
        return Error('unsupported subject type')

    def split(self, x):
        return Error('unsupported subject type')

    def take(self, x):
        return Error('unsupported subject type')

    def each(self, f):
        return Error('unsupported subject type')

    def each2(self, f, x):
        return Error('unsupported subject type')

    def eachLeft(self, f, x):
        return Error('unsupported subject type')

    def eachRight(self, f, x):
        return Error('unsupported subject type')

    def eachPair(self, f):
        return Error('unsupported subject type')

    def over(self, f):
        return Error('unsupported subject type')

    def overNeutral(self, f, x):
        return Error('unsupported subject type')

    def scanOver(self, f):
        return Error('unsupported subject type')

    def iterate(self, f, x):
        return Error('unsupported subject type')

    def scanOverNeutral(self, f, x):
        return Error('unsupported subject type')

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

    def atom(self):
        return Integer.false()
