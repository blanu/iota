import struct
from enum import Enum
import math
from squeeze import squeeze, expand
from noun import Noun
import error

class Monads(Enum):
    atom = 0
    char = 1
    complementation = 2
    enclose = 3
    enumerate = 4
    first = 6
    floor = 7
    format = 19
    gradeDown = 8
    gradeUp = 9
    group = 10
    negate = 11
    reciprocal = 12
    reverse = 13
    shape = 14
    size = 15
    transpose = 16
    unique = 17
    count = 18

    evaluate = 19

    def symbol(self):
        return Word(self.value, o=NounType.BUILTIN_MONAD)

class Dyads(Enum):
    amend = 117
    cut = 118
    divide = 119
    drop = 120
    equal = 121
    expand = 122
    find = 123
    form = 141
    format2 = 142
    index = 124
    indexInDepth = 143
    integerDivide = 144
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

    apply = 145

    def symbol(self):
        return Word(self.value, o=NounType.BUILTIN_DYAD)

class Triads(Enum):
    apply = 300

    def symbol(self):
        return Word(self.value, o=NounType.BUILTIN_TRIAD)

class Adverbs(Enum):
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

    def symbol(self):
        return Word(self.value, o=NounType.ADVERB)

class StorageType(Enum):
    WORD = 0
    FLOAT = 1
    WORD_ARRAY = 2 # all integers
    FLOAT_ARRAY = 3 # all floats
    MIXED_ARRAY = 4 # array of storage types

class NounType(Enum):
    INTEGER = 10
    REAL = 11
    CHARACTER = 12
    STRING = 13
    LIST = 14
    DICTIONARY = 15
    BUILTIN_SYMBOL = 16
    BUILTIN_MONAD = 17
    BUILTIN_DYAD = 18
    BUILTIN_TRIAD = 19
    ADVERB = 20
    USER_SYMBOL = 27
    USER_MONAD = 21
    USER_DYAD = 22
    USER_TRIAD = 23
    ERROR = 26
    EXPRESSION = 28

class SymbolType(Enum):
    i = 200
    x = 201
    y = 202
    z = 203
    f = 204
    undefined = 205

    def symbol(self):
        return Word(self.value, o=NounType.BUILTIN_SYMBOL)

class Storage:
    @staticmethod
    def from_bytes(data):
        length, typedRest = expand(data)
        typedData = typedRest[:length]
        typedRest = typedRest[length:]

        typeBytes = typedData[0:1]
        untypedData = typedData[1:]

        typeInt = struct.unpack("B", typeBytes)[0]
        storageType = StorageType(typeInt)

        if storageType == StorageType.WORD:
            result, integerRest = Word.from_bytes(untypedData)
            return result, integerRest + typedRest
        elif storageType == StorageType.FLOAT:
            return Float.from_bytes(untypedData), typedRest
        elif storageType == StorageType.WORD_ARRAY:
            result, integerArrayRest = WordArray.from_bytes(untypedData)
            return result, integerArrayRest + typedRest
        elif storageType == StorageType.FLOAT_ARRAY:
            return FloatArray.from_bytes(untypedData), typedRest
        elif storageType == StorageType.MIXED_ARRAY:
            result, mixedArrayRest = MixedArray.from_bytes(untypedData)
            return result, mixedArrayRest + typedRest

    @staticmethod
    def identity(i, *discard):
        return i

    # Monads

    @staticmethod
    def atom_list(i):
        if len(i.i) == 0:
            return Word.true()
        else:
            return Word.false()

    # char: delegated to subclass

    def complementation_impl(self):
        return Word(1).minus(self)

    # enclose word, float: delegated to subclass
    @staticmethod
    def enclose_impl(i):
        return MixedArray([i])

    # enumerate: delegated to subclass

    # expand: delegated to subclass

    # first: delegated to subclass

    # floor: delegated to subclass

    # format: delegated to subclass

    # gradeDown: delegated to subclass

    # gradeUp: delegated to subclass

    # group: delegated to subclass

    def negate_impl(self):
        return Word(0).minus(self)

    def reciprocal_impl(self):
        return Float(1).divide(self)

    # reverse: delegated to subclass

    # shape: delegated to subclass

    # size: delegated to subclass

    # transpose: delegated to subclass

    # unique: delegated to subclass

    # Dyads

    # amend: delegated to subclass

    # cut: delegated to subclass

    # divide: delegated to subclass

    # drop: delegated to subclass

    # equal: delegated to subclass

    # find: delegated to subclass

    # form:: delegated to subclass

    # format2: delegated to subclass

    # index: delegated to subclass

    # indexInDepth: delegated to subclass

    # integerDivide: delegated to subclass

    # join: delegated to subclass

    # less: delegated to subclass

    # match: delegated to subclass

    # max: delegated to subclass

    # min: delegated to subclass

    # minus: delegated to subclass

    # more: delegated to subclass

    # plus: delegated to subclass

    # power: delegated to subclass

    # reshape: delegated to subclass

    # remainder: delegated to subclass

    # rotate: delegated to subclass

    # split: delegated to subclass

    # take: delegated to subclass

    # times: delegated to subclass

    @staticmethod
    def apply_builtin_monad(i, f):
        return Noun.dispatchMonad(i, f)

    @staticmethod
    def apply_user_monad(i, f):
        reduction = Storage.reduceMonad(i, f)
        return Storage.evaluate(reduction)

    @staticmethod
    def apply_monad_expression(i, f):
        evaluated = Storage.evaluate(i)
        return evaluated.apply(f)

    @staticmethod
    def apply_builtin_dyad(i, f, x):
        return Noun.dispatchDyad(i, f, x)

    @staticmethod
    def apply_user_dyad(i, f, x):
        reduction = Storage.reduceDyad(i, f, x)
        return Storage.evaluate(reduction)

    @staticmethod
    def apply_dyad_expression(i, f, x):
        evaluated = Storage.evaluate(i)
        return evaluated.apply(f, x)

    @staticmethod
    def reduceMonad(i, f):
        return Storage.reduce_monad_expression(f, i, f)

    @staticmethod
    def reduceDyad(i, f, x):
        return Storage.reduce_dyad_expression(f, i, f, x)

    @staticmethod
    def reduce_monad_expression(e, i, f):
        results = []
        for y in e.i:
            if y.o == NounType.BUILTIN_SYMBOL:
                if y.equal(SymbolType.i.symbol()) == Word.true():
                    results.append(i)
                elif y.equal(SymbolType.f.symbol()) == Word.true():
                    results.append(f)
                else:
                    return error.Error.invalid_argument()
            elif y.o == NounType.EXPRESSION:
                reduced = Storage.reduce_monad_expression(y, i, f)
                results.append(reduced)
            else:
                results.append(y)
        return MixedArray(results, o=NounType.EXPRESSION)

    @staticmethod
    def reduce_dyad_expression(e, i, f, x):
        results = []
        for y in e.i:
            if y.o == NounType.BUILTIN_SYMBOL:
                if y.equal(SymbolType.i.symbol()) == Word.true():
                    results.append(i)
                elif y.equal(SymbolType.x.symbol()) == Word.true():
                    results.append(f, x)
                elif y.equal(SymbolType.f.symbol()) == Word.true():
                    results.append(f)
                else:
                    return error.Error.invalid_argument()
            elif y.o == NounType.EXPRESSION:
                reduced = Storage.reduce_dyad_expression(y, i, f, x)
                results.append(reduced)
            else:
                results.append(y)
        return MixedArray(results, o=NounType.EXPRESSION)

    @staticmethod
    def evaluate_impl(e):
        if len(e.i) == 0:
            return error.Error.empty_argument()

        i = e.i[0]
        f = e.i[1]

        if f.o == NounType.BUILTIN_MONAD:
            rest = e.i[2:]
            result = Noun.dispatchMonad(i, f)
            if len(rest) == 0:
                return result
            else:
                next_e = MixedArray([result] + rest, o=NounType.EXPRESSION)
                return next_e.evaluate()
        elif f.o == NounType.BUILTIN_DYAD:
            x = e.i[2]
            rest = e.i[3:]
            result = Noun.dispatchDyad(i, f, x)
            if len(rest) == 0:
                return result
            else:
                next_e = MixedArray([result] + rest, o=NounType.EXPRESSION)
                return next_e.evaluate()

    # Monadic adverbs

    @staticmethod
    def converge_impl(i, f):
        current = i
        if current.o == NounType.ERROR:
            return current

        nextValue = Noun.dispatchMonad(current, f)
        if nextValue.o == NounType.ERROR:
            return nextValue

        while nextValue.match(current) != Word.true():
            current = nextValue
            nextValue = Noun.dispatchMonad(current, f)
            if nextValue.o == NounType.ERROR:
                return nextValue
        return current

    @staticmethod
    def each_scalar(i, f):
        return Noun.dispatchMonad(i, f)

    # eachPair delegated to subclass

    # over delegated to subclass

    @staticmethod
    def scanConverging_impl(i, f):
        current = i
        results = [current]
        nextValue = Noun.dispatchMonad(current, f)
        while nextValue.match(current) != Word.true():
            current = nextValue
            results.append(current)
            nextValue = Noun.dispatchMonad(current, f)
        return MixedArray(results)

    # scanOver delegated to subclass

    # Dyadic adverbs

    def each2_scalar(self, f, x):
        return Noun.dispatchDyad(self, f, x)

    def eachLeft_scalar(self, f, x):
        return Noun.dispatchDyad(self, f, x)

    def eachLeft_words(self, f, x):
        return MixedArray([Noun.dispatchDyad(self, f, Word(y)) for y in x.i])

    def eachLeft_floats(self, f, x):
        return MixedArray([Noun.dispatchDyad(self, f, Float(y)) for y in x.i])

    def eachLeft_mixed(self, f, x):
        return MixedArray([Noun.dispatchDyad(self, f, y) for y in x.i])

    def eachRight_scalar(self, f, x):
        return Noun.dispatchDyad(x, f, self)

    def eachRight_words(self, f, x):
        return MixedArray([Noun.dispatchDyad(Word(y), f, self) for y in x.i])

    def eachRight_floats(self, f, x):
        return MixedArray([Noun.dispatchDyad(Float(y), f, self) for y in x.i])

    def eachRight_mixed(self, f, x):
        return MixedArray([Noun.dispatchDyad(y, f, self) for y in x.i])

    def overNeutral_scalar(self, f, x):
        return Noun.dispatchDyad(self, f, x)

    @staticmethod
    def iterate_word(i, f, x):
        if x.i >= 0:
            current = i
            truth = x
            while truth != Word(0):
                current = Noun.dispatchMonad(current, f)
                truth = truth.minus(Word(1))
            return current
    # iterate float, words, floats, mixed: unsupported

    @staticmethod
    def scanIterating_word(i, f, x):
        if x.i >= 0:
            current = i
            truth = x
            results = [current]
            while truth != Word(0):
                current = Noun.dispatchMonad(current, f)
                truth = truth.minus(Word(1))
                results.append(current)
            return MixedArray(results)
        else:
            return error.Error.invalid_adverb_argument()

    # scanIterating: float, words, floats, mixed - unsupported

    def scanOverNeutral_scalar(self, f, x):
        return MixedArray([self, Noun.dispatchDyad(self, f, x)])
    # scanOverNeutral words, floats, mixed: delegated to subclass

    @staticmethod
    def scanWhileOne_impl(i, f, x):
        current = i
        results = [current]
        truth = Noun.dispatchMonad(current, f)
        while truth == Word(1):
            current = Noun.dispatchMonad(current, x)
            truth = Noun.dispatchMonad(current, f)
            results.append(current)
        return MixedArray(results)

    @staticmethod
    def whileOne_impl(i, f, x):
        current = i
        truth = Noun.dispatchMonad(current, f)
        while truth == Word(1):
            current = Noun.dispatchMonad(current, x)
            truth = Noun.dispatchMonad(current, f)
        return current

    def __init__(self, o, t, x):
        self.o = o
        self.t = t
        self.i = x

    def __eq__(self, x):
        if self.t != x.t:
            return False

        return self.i == x.i

    def __hash__(self):
        return hash(self.i)

    def apply(self, f, x=None):
        if x is None:
            return Noun.dispatchDyad(self, Dyads.apply.symbol(), f)
        else:
            return Noun.dispatchTriad(self, Triads.apply.symbol(), f, x)

    def evaluate(self):
        return Noun.dispatchMonad(self, Monads.evaluate.symbol())

    # Monads
    def atom(self):
        return Noun.dispatchMonad(self, Monads.atom.symbol())

    def char(self):
        return Noun.dispatchMonad(self, Monads.char.symbol())

    def complementation(self):
        return Noun.dispatchMonad(self, Monads.complementation.symbol())

    def enclose(self):
        return Noun.dispatchMonad(self, Monads.enclose.symbol())

    def enumerate(self):
        return Noun.dispatchMonad(self, Monads.enumerate.symbol())

    def first(self):
        return Noun.dispatchMonad(self, Monads.first.symbol())

    def floor(self):
        return Noun.dispatchMonad(self, Monads.floor.symbol())

    def format(self):
        return Noun.dispatchMonad(self, Monads.format.symbol())

    def gradeDown(self):
        return Noun.dispatchMonad(self, Monads.gradeDown.symbol())

    def gradeUp(self):
        return Noun.dispatchMonad(self, Monads.gradeUp.symbol())

    def group(self):
        return Noun.dispatchMonad(self, Monads.group.symbol())

    def negate(self):
        return Noun.dispatchMonad(self, Monads.negate.symbol())

    def reciprocal(self):
        return Noun.dispatchMonad(self, Monads.reciprocal.symbol())

    def reverse(self):
        return Noun.dispatchMonad(self, Monads.reverse.symbol())

    def shape(self):
        return Noun.dispatchMonad(self, Monads.shape.symbol())

    def size(self):
        return Noun.dispatchMonad(self, Monads.size.symbol())

    def transpose(self):
        return Noun.dispatchMonad(self, Monads.transpose.symbol())

    def unique(self):
        return Noun.dispatchMonad(self, Monads.unique.symbol())

    # Dyads
    def amend(self, x):
        return Noun.dispatchDyad(self, Dyads.amend.symbol(), x)

    def cut(self, x):
        return Noun.dispatchDyad(self, Dyads.cut.symbol(), x)

    def divide(self, x):
        return Noun.dispatchDyad(self, Dyads.divide.symbol(), x)

    def drop(self, x):
        return Noun.dispatchDyad(self, Dyads.drop.symbol(), x)

    def equal(self, x):
        return Noun.dispatchDyad(self, Dyads.equal.symbol(), x)

    def expand(self, x):
        return Noun.dispatchDyad(self, Dyads.expand.symbol(), x)

    def find(self, x):
        return Noun.dispatchDyad(self, Dyads.find.symbol(), x)

    def form(self, x):
        return Noun.dispatchDyad(self, Dyads.form.symbol(), x)

    def format2(self, x):
        return Noun.dispatchDyad(self, Dyads.format2.symbol(), x)

    def index(self, x):
        return Noun.dispatchDyad(self, Dyads.index.symbol(), x)

    def indexInDepth(self, x):
        return Noun.dispatchDyad(self, Dyads.indexInDepth.symbol(), x)

    def integerDivide(self, x):
        return Noun.dispatchDyad(self, Dyads.integerDivide.symbol(), x)

    def join(self, x):
        return Noun.dispatchDyad(self, Dyads.join.symbol(), x)

    def less(self, x):
        return Noun.dispatchDyad(self, Dyads.less.symbol(), x)

    def match(self, x):
        return Noun.dispatchDyad(self, Dyads.match.symbol(), x)

    def max(self, x):
        return Noun.dispatchDyad(self, Dyads.max.symbol(), x)

    def min(self, x):
        return Noun.dispatchDyad(self, Dyads.min.symbol(), x)

    def minus(self, x):
        return Noun.dispatchDyad(self, Dyads.minus.symbol(), x)

    def more(self, x):
        return Noun.dispatchDyad(self, Dyads.more.symbol(), x)

    def plus(self, x):
        return Noun.dispatchDyad(self, Dyads.plus.symbol(), x)

    def power(self, x):
        return Noun.dispatchDyad(self, Dyads.power.symbol(), x)

    def remainder(self, x):
        return Noun.dispatchDyad(self, Dyads.remainder.symbol(), x)

    def reshape(self, x):
        return Noun.dispatchDyad(self, Dyads.reshape.symbol(), x)

    def rotate(self, x):
        return Noun.dispatchDyad(self, Dyads.rotate.symbol(), x)

    def split(self, x):
        return Noun.dispatchDyad(self, Dyads.split.symbol(), x)

    def take(self, x):
        return Noun.dispatchDyad(self, Dyads.take.symbol(), x)

    def times(self, x):
        return Noun.dispatchDyad(self, Dyads.times.symbol(), x)

    # Monadic Adverbs
    def converge(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.converge.symbol(), f)

    def each(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.each.symbol(), f)

    def eachPair(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.eachPair.symbol(), f)

    def over(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.over.symbol(), f)

    def scanConverging(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.scanConverging.symbol(), f)

    def scanOver(self, f):
        return Noun.dispatchMonadicAdverb(self, Adverbs.scanOver.symbol(), f)

    # Dyadic Adverbs
    def each2(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.each2.symbol(), f, x)

    def eachLeft(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.eachLeft.symbol(), f, x)

    def eachRight(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.eachRight.symbol(), f, x)

    def overNeutral(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.overNeutral.symbol(), f, x)

    def iterate(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.iterate.symbol(), f, x)

    def scanIterating(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.scanIterating.symbol(), f, x)

    def scanOverNeutral(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.scanOverNeutral.symbol(), f, x)

    def scanWhileOne(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.scanWhileOne.symbol(), f, x)

    def whileOne(self, f, x):
        return Noun.dispatchDyadicAdverb(self, Adverbs.whileOne.symbol(), f, x)

class Word(Storage):
    @staticmethod
    def true(*discard):
        return Word(1)

    @staticmethod
    def false(*discard):
        return Word(0)

    @staticmethod
    def zero(*discard):
        return Word(0)

    @staticmethod
    def one(*discard):
        return Word(1)

    @staticmethod
    def from_bytes(data):
        i, rest = expand(data)
        return Word(i), rest

    def __init__(self, x, o=NounType.INTEGER):
        super().__init__(o, StorageType.WORD, int(x))

    def __str__(self):
        return "I%s" % str(self.i)

    def __lt__(self, x):
        if x.t == StorageType.WORD:
            return self.less(x) == Word(1)
        elif x.t == StorageType.FLOAT:
            return self.less(x) == Word(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.t.value)
        intBytes = squeeze(self.i)
        data = typeBytes + intBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    # Monads

    # atom: Word.true

    # char: hotpatched by character.py to avoid circular imports

    # complementation: Storage.complementation

    def enclose_impl(self):
        return WordArray([self.i])

    def enumerate_impl(self):
        return WordArray(list(range(1, self.i + 1)))

    # first: Storage.identity

    # floor: Storage.identity

    # format: unimplemented FIXME

    # gradeDown: Storage.identity

    # gradeUp: Storage.identity

    # group unsupported

    # negate: Storage.negate

    # reciprocal: Storage.reciprocal

    # reverse: Storage.identity

    # shape: Word.zero

    # size: Word.zero

    # transpose: Storage.identity

    # unique: Storage.identity

    # Dyads
    def amend_impl(self, x):
            return self.enclose().amend(x.enclose())

    def cut_impl(self, x):
        return x.drop(self)

    def divide_word(self, x):
        try:
            return Float(float(self.i) / float(x.i))
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_float(self, x):
        try:
            return Float(float(self.i) / x.i)
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_words(self, x):
        try:
            return FloatArray([float(self.i) / float(y) for y in x.i])
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_floats(self, x):
        try:
            return FloatArray([float(self.i) / y for y in x.i])
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_mixed(self, x):
        results = []
        for y in x.i:
            result = self.divide(y)
            if result.o == NounType.ERROR:
                return result
            else:
                results.append(result)
        return MixedArray(results)

    # drop unsupported

    def equal_word(self, x):
        if self.i == x.i:
            return Word(1)
        else:
            return Word(0)

    def equal_float(self, x):
        if Float(self.i) == x:
            return Word(1)
        else:
            return Word(0)

    def equal_words(self, x):
        for y in x.i:
            if self.i != y:
                return Word(0)
        return Word(1)

    def equal_floats(self, x):
        for y in x.i:
            if Float(self.i) != Float(y):
                return Word(0)
        return Word(1)

    def equal_mixed(self, x):
        for y in x.i:
            if self.equal(y) != Word(1):
                return Word(0)
        return Word(1)

    # expand: unsupported

    # find word, float: unsupported
    def find_list(self, x):
        return x.find(self)

    # form: unimplemented FIXME

    # format2: unimplemented FIXME

    def index_words(self, x):
        if self.i < 1 or self.i > len(x.i):
            return error.Error.out_of_bounds()
        else:
            return Word(x.i[self.i - 1])

    def index_floats(self, x):
        if self.i < 1 or self.i > len(x.i):
            return error.Error.out_of_bounds()
        else:
            return Float(x.i[self.i - 1])

    def index_mixed(self, x):
        if self.i < 1 or self.i > len(x.i):
            return error.Error.out_of_bounds()
        else:
            return x.i[self.i - 1]

    # indexInDepth: unimplemented FIXME

    def integerDivide_word(self, x):
        try:
            return Word(self.i // x.i)
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    # integerDivide float: unsupported

    def integerDivide_words(self, x):
        try:
            return WordArray([self.i // y for y in x.i])
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    # integerDivide floats: unsupported

    def integerDivide_mixed(self, x):
        results = []
        for y in x.i:
            result = self.integerDivide(y)
            if result.o == NounType.ERROR:
                return result
            else:
                results.append(result)
        return MixedArray(results)

    def join_word(self, x):
        return WordArray([self.i, x.i])

    def join_float(self, x):
        return MixedArray([Word(self.i), Float(x.i)])

    def join_words(self, x):
        return WordArray([self.i] + x.i)

    def join_floats(self, x):
        return FloatArray([float(self.i)] + x.i)

    def join_mixed(self, x):
        return MixedArray([Word(self.i)] + x.i)

    def less_word(self, x):
        if self.i < x.i:
            return Word(1)
        else:
            return Word(0)

    def less_float(self, x):
        if float(self.i) < x.i:
            return Word(1)
        else:
            return Word(0)

    def less_words(self, x):
        for y in x.i:
            if self.i >= y:
                return Word(0)
        return Word(1)

    def less_floats(self, x):
        for y in x.i:
            if float(self.i) >= y:
                return Word(0)
        return Word(1)

    def less_mixed(self, x):
        for y in x.i:
            if self.less(y) != Word(1):
                return Word(0)
        return Word(1)

    def match_word(self, x):
        if self.i == x.i:
            return Word.true()
        else:
            return Word.false()

    def match_float(self, x):
        diff = abs(float(self.i) - x.i)
        if diff < Float.tolerance():
            return Word.true()
        else:
            return Word.false()

    # match words, floats, mixed: Word.false

    def max_word(self, x):
        if self.i >= x.i:
            return self
        else:
            return x

    def max_float(self, x):
        if float(self.i) > x.i:
            return Float(self.i)
        elif float(self.i) < x.i:
            return x
        else: #self.i == x.i
            return Float(self.i)

    def max_words(self, x):
        results = []
        for y in x.i:
            if self.i > y:
                results.append(self.i)
            else:
                results.append(y)
        return WordArray(results)

    def max_floats(self, x):
        results = []
        for y in x.i:
            if float(self.i) > y:
                results.append(self.i)
            else:
                results.append(y)
        return FloatArray(results)

    def max_mixed(self, x):
        results = []
        for y in x.i:
            results.append(self.max(y))
        return MixedArray(results)

    def min_word(self, x):
        if self.i <= x.i:
            return self
        else:
            return x

    def min_float(self, x):
        if float(self.i) < x.i:
            return Float(self.i)
        elif float(self.i) > x.i:
            return x
        else: #self.i == x.i
            return Float(self.i)

    def min_words(self, x):
        results = []
        for y in x.i:
            if self.i < y:
                results.append(self.i)
            else:
                results.append(y)
        return WordArray(results)

    def min_floats(self, x):
        results = []
        for y in x.i:
            if float(self.i) < y:
                results.append(self.i)
            else:
                results.append(y)
        return FloatArray(results)

    def min_mixed(self, x):
        results = []
        for y in x.i:
            results.append(self.min(y))
        return MixedArray(results)

    def minus_word(self, x):
        return Word(self.i - x.i)

    def minus_float(self, x):
        return Float(float(self.i) - x.i)

    def minus_words(self, x):
        return WordArray([self.i - y for y in x.i])

    def minus_floats(self, x):
        return FloatArray([float(self.i) - y for y in x.i])

    def minus_mixed(self, x):
        return MixedArray([self.minus(y) for y in x.i])

    def more_word(self, x):
        if self.i > x.i:
            return Word(1)
        else:
            return Word(0)

    def more_float(self, x):
        if float(self.i) > x.i:
            return Word(1)
        else:
            return Word(0)

    def more_words(self, x):
        for y in x.i:
            if self.i <= y:
                return Word(0)
        return Word(1)

    def more_floats(self, x):
        for y in x.i:
            if float(self.i) <= y:
                return Word(0)
        return Word(1)

    def more_mixed(self, x):
        for y in x.i:
            if self.more(y) != Word(1):
                return Word(0)
        return Word(1)

    def plus_word(self, x):
        return Word(self.i + x.i)

    def plus_float(self, x):
        return Float(float(self.i) + x.i)

    def plus_words(self, x):
        return WordArray([self.i + y for y in x.i])

    def plus_floats(self, x):
        return FloatArray([float(self.i) + y for y in x.i])

    def plus_mixed(self, x):
        return MixedArray([self.plus(y) for y in x.i])

    def power_scalar(self, x):
        return Float(math.pow(self.i, x.i))

    def power_list(self, x):
        return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))

    def power_mixed(self, x):
        return MixedArray(list(map(lambda y: self.power(y), x.i)))

    # reshape unsupported

    def remainder_word(self, x):
        return Word(self.i % x.i)

    # remainder float unsupported

    def remainder_words(self, x):
        return WordArray(list(map(lambda y: self.i % y, x.i)))

    # remainder float unsupported

    def remainder_mixed(self, x):
        return MixedArray(list(map(lambda y: self.remainder(y), x.i)))

    def rotate_impl(self, x):
        return x.rotate(self)

    def split_impl(self, x):
        return x.split(self)

    def times_word(self, x):
        return Word(self.i * x.i)

    def times_float(self, x):
        return Float(float(self.i) * x.i)

    def times_words(self, x):
        return WordArray([self.i * y for y in x.i])

    def times_floats(self, x):
        return FloatArray([float(self.i) * y for y in x.i])

    def times_mixed(self, x):
        return MixedArray([self.times(y) for y in x.i])

    # Monadic Adverbs

    # converge: Storage.converge_impl

    # each: Storage.each_scalar

    # eachPair unsupported

    # over: Storage.identity

    # scanConverging: Storage.scanConverging_impl

    def scanOver_impl(self, f):
        return WordArray([self.i])

    # Dyadic Adverbs

    # Storage.each2_scalar

    # eachLeft word: Storage.eachLeft_scalar
    # eachLeft float: Storage.eachLeft_scalar
    # eachLeft words: Storage.eachLeft_words
    # eachLeft floats: Storage.eachLeft_floats
    # eachLeft mixed: Storage.eachLeft_mixed

    # eachRight word: Storage.eachRight_scalar
    # eachRight float: Storage.eachRight_scalar
    # eachRight words: Storage.eachRight_words
    # eachRight floats: Storage.eachRight_floats
    # eachRight mixed: Storage.eachRight_mixed

    # Storage.overNeutral_scalar

    # iterate: Storage.iterate_word
    # iterate float, words, floats, mixed: unsupported

    # scanIterating: Storage.scanIterating_word
    # scanIterating: float, words, floats, mixed - unsupported

    # scanOverNeutral: Storage.scanOverNeutral_scalar

    # scanWhileOne: Storage.scanWhileOne_impl

    # whileOne: Storage.whileOne

class Float(Storage):
    @staticmethod
    def tolerance():
        return 1e-14

    @staticmethod
    def from_bytes(data):
        i = struct.unpack('f', data)
        return Float(i[0])

    def __init__(self, x, o=NounType.REAL):
        super().__init__(o, StorageType.FLOAT, float(x))

    def __str__(self):
        return "F%s" % str(self.i)

    def __lt__(self, x):
        if x.t == StorageType.WORD:
            return self.less(x) == Word(1)
        elif x.t == StorageType.FLOAT:
            return self.less(x) == Word(1)
        else:
            return False

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.t.value)
        floatBytes = struct.pack("f", self.i)
        data = typeBytes + floatBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    # Monads

    # atom: Word.true

    # char: unsupported

    # complementation: Storage.complementation_impl

    def enclose_impl(self):
        return FloatArray([self.i])

    # enumerate unsupported

    # first: Storage.identity

    def floor_impl(self):
        return Word(math.floor(self.i))

    # format: unimplemented FIXME

    # gradeDown: Storage.identity

    # gradeUp: Storage.identity

    # group unsupported

    # negate: Storage.negate_impl

    # reciprocal: Storage.reciprocal_impl

    # reverse: Storage.identity

    # shape: Word.zero

    # size: Word.zero

    # transport: Storage.identity

    # unique: Storage.identity

    # Dyads

    def amend_scalar(self, x):
        return self.enclose().amend(x.enclose())

    # amend words, floats, mixed unsupported

    # cut unsupported

    def divide_word(self, x):
        try:
            return Float(self.i / float(x.i))
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_float(self, x):
        try:
            return Float(self.i / x.i)
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_words(self, x):
        try:
            return FloatArray([self.i / float(y) for y in x.i])
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_floats(self, x):
        try:
            return FloatArray([self.i / y for y in x.i])
        except ZeroDivisionError:
            return error.Error.division_by_zero()

    def divide_mixed(self, x):
        results = []
        for y in x.i:
            result = self.divide(y)
            if result.o == NounType.ERROR:
                return result
            else:
                results.append(result)
        return MixedArray(results)

    # drop unsupported

    def equal_word(self, x):
        if self == Float(x.i):
            return Word.true()
        else:
            return Word.false()

    def equal_float(self, x):
        if self == x:
            return Word.true()
        else:
            return Word.false()

    def equal_words(self, x):
        for y in x.i:
            if self != Float(y):
                return Word.false()
        return Word.true()

    def equal_floats(self, x):
        for y in x.i:
            if self.i != y:
                return Word.false()
        return Word.true()

    def equal_mixed(self, x):
        for y in x.i:
            if self.equal(y) != Word.true():
                return Word.false()
        return Word.true()

    # expand: unsupported

    # find word, float: unsupported
    def find_list(self, x):
        return x.find(FloatArray([self.i]))

    # form: unimplemented FIXME

    # format2: unimplemented FIXME

    # index word, float: unsupported
    def index_words(self, x):
        count = len(x.i)
        extent = self.i * float(count)
        offset = int(extent)
        return Word(offset).index(x)

    def index_floats(self, x):
        count = len(x.i)
        extent = self.i * float(count)
        offset = int(extent)
        return Word(offset).index(x)

    def index_mixed(self, x):
        count = len(x.i)
        extent = self.i * float(count)
        offset = int(extent)
        return Word(offset).index(x)

    # indexInDepth: unimplemented FIXME

    # integerDivide: unsupported

    def join_word(self, x):
        return MixedArray([Float(self.i), Word(x.i)])

    def join_float(self, x):
        return FloatArray([self.i, x.i])

    def join_words(self, x):
        return FloatArray([self.i] + [float(y) for y in x.i])

    def join_floats(self, x):
        return FloatArray([self.i] + x.i)

    def join_mixed(self, x):
        return MixedArray([Float(self.i)] + x.i)

    def less_word(self, x):
        if self.i < float(x.i):
            return Word.true()
        else:
            return Word.false()

    def less_float(self, x):
        if self.i < x.i:
            return Word.true()
        else:
            return Word.false()

    def less_words(self, x):
        for y in x.i:
            if self.i >= float(y):
                return Word(0)
        return Word(1)

    def less_floats(self, x):
        for y in x.i:
            if self.i >= y:
                return Word(0)
        return Word(1)

    def less_mixed(self, x):
        for y in x.i:
            if self.less(y) != Word(1):
                return Word(0)
        return Word(1)

    def match_word(self, x):
        diff = abs(self.i - float(x.i))
        if diff < Float.tolerance():
            return Word.true()
        else:
            return Word.false()

    def match_float(self, x):
        diff = abs(self.i - x.i)
        if diff < Float.tolerance():
            return Word.true()
        else:
            return Word.false()

    # match words, floats, mixed: Word.false

    def max_word(self, x):
        if self.i >= float(x.i):
            return self
        else:
            return Float(x.i)

    def max_float(self, x):
        if self.i > x.i:
            return self
        elif self.i < x.i:
            return x
        else: #self.i == x.i
            return self

    def max_words(self, x):
        results = []
        for y in x.i:
            if self.i > float(y):
                results.append(self.i)
            else:
                results.append(float(y))
        return FloatArray(results)

    def max_floats(self, x):
        results = []
        for y in x.i:
            if self.i > y:
                results.append(self.i)
            else:
                results.append(y)
        return FloatArray(results)

    def max_mixed(self, x):
        results = []
        for y in x.i:
            results.append(self.max(y))
        return MixedArray(results)

    def min_word(self, x):
        if self.i <= float(x.i):
            return self
        else:
            return Float(x.i)

    def min_float(self, x):
        if self.i < x.i:
            return self
        elif self.i > x.i:
            return x
        else: #self.i == x.i
            return self

    def min_words(self, x):
        results = []
        for y in x.i:
            if self.i < float(y):
                results.append(self.i)
            else:
                results.append(float(y))
        return FloatArray(results)

    def min_floats(self, x):
        results = []
        for y in x.i:
            if self.i < y:
                results.append(self.i)
            else:
                results.append(y)
        return FloatArray(results)

    def min_mixed(self, x):
        results = []
        for y in x.i:
            results.append(self.min(y))
        return MixedArray(results)

    def minus_word(self, x):
        return Float(self.i - float(x.i))

    def minus_float(self, x):
        return Float(self.i - x.i)

    def minus_words(self, x):
        return FloatArray([self.i - float(y) for y in x.i])

    def minus_floats(self, x):
        return FloatArray([self.i - y for y in x.i])

    def minus_mixed(self, x):
        return MixedArray([self.minus(y) for y in x.i])

    def more_word(self, x):
        if self.i > float(x.i):
            return Word(1)
        else:
            return Word(0)

    def more_float(self, x):
        if self.i > x.i:
            return Word(1)
        else:
            return Word(0)

    def more_words(self, x):
        for y in x.i:
            if self.i <= float(y):
                return Word(0)
        return Word(1)

    def more_floats(self, x):
        for y in x.i:
            if self.i <= y:
                return Word(0)
        return Word(1)

    def more_mixed(self, x):
        for y in x.i:
            if self.more(y) != Word(1):
                return Word(0)
        return Word(1)

    def plus_word(self, x):
        return Float(self.i + float(x.i))

    def plus_float(self, x):
        return Float(self.i + x.i)

    def plus_words(self, x):
        return FloatArray([self.i + float(y) for y in x.i])

    def plus_floats(self, x):
        return FloatArray([self.i + y for y in x.i])

    def plus_mixed(self, x):
        return MixedArray([self.plus(y) for y in x.i])

    def power_scalar(self, x):
        return Float(math.pow(self.i, x.i))

    def power_list(self, x):
        return FloatArray(list(map(lambda y: math.pow(self.i, y), x.i)))

    def power_mixed(self, x):
        return MixedArray(list(map(lambda y: self.power(y), x.i)))

    # reshape unsupported

    # remainder unsupported

    # rotate unsupported

    # split word, float: unsupported
    def split_list(self, x):
        return x.split(self)

    # take unsupported

    def times_word(self, x):
        return Float(self.i * float(x.i))

    def times_float(self, x):
        return Float(self.i * x.i)

    def times_words(self, x):
        return FloatArray([self.i * float(y) for y in x.i])

    def times_floats(self, x):
        return FloatArray([self.i * y for y in x.i])

    def times_mixed(self, x):
        return MixedArray([self.times(y) for y in x.i])

    # Monadic adverbs

    # converge: Storage.converge_impl

    # each: Storage.each_scalar

    # eachPair unsupported

    # over: Storage.identity

    # scanConverging: Storge.scanConverging_impl

    def scanOver_impl(self, f):
        return FloatArray([self.i])

    # Dyadic adverbs

    # Storage.each2_scalar

    # eachLeft word: Storage.eachLeft_scalar
    # eachLeft float: Storage.eachLeft_scalar
    # eachLeft words: Storage.eachLeft_words
    # eachLeft floats: Storage.eachLeft_floats
    # eachLeft mixed: Storage.eachLeft_mixed

    # eachRight word: Storage.eachRight_scalar
    # eachRight float: Storage.eachRight_scalar
    # eachRight words: Storage.eachRight_words
    # eachRight floats: Storage.eachRight_floats
    # eachRight mixed: Storage.eachRight_mixed

    # Storage.overNeutral_scalar

    # iterate: unsupported

    # scanIterating: unsupported

    # scanOverNeutral: Storage.scanOverNeutral_scalar

    # scanWhileOne: Storage.scanWhileOne_impl

    # whileOne: Storage.whileOne

class WordArray(Storage):
    @staticmethod
    def from_bytes(data):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = expand(rest)
            results.append(result)
        return WordArray(results), rest

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.WORD_ARRAY, [int(y) for y in x])

    def __str__(self):
        return "I%s" % str(self.i)

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.t.value)

        intArrayBytes = b''
        for y in self.i:
            intArrayBytes += squeeze(y)

        data = typeBytes + intArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    # Monads

    # atom: Storage.atom_list

    # char: hotpatched by character.py to avoid circular imports

    # complementation: Storage.complementation_impl

    # enclose: Storage.enclose_impl

    # enumerate unsupported

    def first_impl(self):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            return Word(self.i[0])

    # floor: Storage.identity

    # format: unimplemented FIXME

    def gradeDown_impl(self):
        return self.gradeUp().reverse()

    def gradeUp_impl(self):
        return WordArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    # FIXME
    # def group_impl(self):
    #     keys = self.unique()
    #     values = []
    #     for key in keys.i:
    #         indexes = []
    #         for index in range(len(self.i)):
    #             if self.i[index] == key:
    #                 indexes.append(index + 1)
    #         values.append(WordArray(indexes))
    #     return Dictionary(keys, MixedArray(values))

    # negate: Storage.negate_impl

    # reciprocal: Storage.reciprocal_impl

    def reverse_impl(self):
        return WordArray(list(reversed(self.i)))

    def shape_impl(self):
        if len(self.i) == 0:
            return Word(0)
        else:
            return WordArray([len(self.i)])

    def size_impl(self):
        return Word(len(self.i))

    # transpose: Storage.identity

    def unique_impl(self):
        return WordArray(list(dict.fromkeys(self.i)))

    # Dyads

    # amend integer, real: unsupported
    # def amend_words(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_floats(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_mixed(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()

    def cut_word(self, x):
        return self.drop(x)

    # cut float: unsupported

    def cut_words(self, x):
        if len(x.i) == 0:
            return self
        else:
            first = x.i[0] - 1
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y - 1
                if first <= last:
                    results.append(WordArray(self.i[first:last]))
                    first = last
                else:
                    return error.Error.invalid_argument()
            return MixedArray(results)

    def cut_floats(self, x):
        if len(x.i) == 0:
            return MixedArray([self])
        else:
            previous = None
            results = []
            for y in x.i:
                if y >= 0.0:
                    last = int(y * len(self.i))
                    if previous is None:
                        results.append(WordArray(self.i[:last]))
                        previous = last
                    else:
                        if previous <= last:
                            results.append(WordArray(self.i[previous:last]))
                            previous = last
                        else:
                            return error.Error.invalid_argument()
                else:
                    return error.Error.invalid_argument()
            if previous is None:
                return MixedArray(results)
            else:
                results.append(WordArray(self.i[previous:]))
                return MixedArray(results)

    def cut_mixed(self, x):
        if len(x.i) == 0:
            return self
        else:
            first = x.i[0]
            if first.t != StorageType.WORD:
                return error.Error.invalid_argument()
            rest = x.i[1:]
            results = []
            for y in rest:
                last = y
                if last.t != StorageType.WORD:
                    return error.Error.invalid_argument()
                if first.i <= last.i:
                    results.append(WordArray(self.i[first.i:last.i]))
                else:
                    return error.Error.invalid_argument()
            return MixedArray(results)

    def divide_word(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return WordArray([float(y) / float(x.i) for y in self.i])

    def divide_float(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return FloatArray([float(y) / x.i for y in self.i])

    def divide_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.i == 0:
                    return error.Error.division_by_zero()
                else:
                    results.append(float(y) / float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.i == 0:
                    return error.Error.division_by_zero()
                else:
                    results.append(float(y) / z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = Word(y).divide(z)
                if result.o == NounType.ERROR:
                    return result
                else:
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def drop_word(self, x):
        if len(self.i) == 0:
            return self
        elif x.i == 0:
            return self
        elif x.i >= len(self.i):
            return WordArray([])
        elif 1 <= x.i <= len(self.i):
           return WordArray(self.i[x.i:])
        elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return WordArray(self.i[:x.i])
        else: # abs(x.i) > len(self.i)
            return WordArray([])

    # drop float, words, floats, mixed: unsupported

    def equal_scalar(self, x):
        return WordArray([Word(y).equal(x).i for y in self.i])

    def equal_words(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if y == z:
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    def equal_floats(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if Word(y).equal(Float(z)) == Word(1):
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    def equal_mixed(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if Word(y).equal(z) == Word(1):
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    # expand: unimplemented FIXME

    def find_word(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return self.find(WordArray([x.i]))

    def find_float(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return self.find(FloatArray([x.i]))

    def find_words(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
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
            return WordArray(results)

    def find_floats(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if Word(y).match(Float(z)) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    def find_mixed(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if Word(y).match(z) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    # form: unimplemented FIXME

    # format2: unimplemented FIXME

    def index_word(self, x):
        if x.i < 1 or x.i > len(self.i):
            return error.Error.out_of_bounds()
        else:
            return Word(self.i[x.i - 1])

    def index_float(self, x):
        count = len(self.i)
        extent = x.i * float(count)
        offset = int(extent)
        return self.index(Word(offset))

    def index_words(self, x):
        return WordArray([self.i[y - 1] for y in x.i])

    def index_floats(self, x):
        return WordArray([self.index(Float(y)).i for y in x.i])

    def index_mixed(self, x):
        return WordArray([self.index(y).i for y in x.i])

    # indexInDepth: unimplemented FIXME

    def integerDivide_word(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return WordArray([y // x.i for y in self.i])

    # integerDivide float: unsupported

    def integerDivide_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.i == 0:
                    return error.Error.division_by_zero()
                else:
                    results.append(y // z)
            return WordArray(results)
        else:
            return error.Error.unequal_array_lengths()

    # integerDivide floats: unsupported

    def integerDivide_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = Word(y).integerDivide(z)
                if result.o == NounType.ERROR:
                    return result
                else:
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def join_word(self, x):
        return WordArray(self.i + [x.i])

    def join_float(self, x):
        return FloatArray([float(y) for y in self.i] + [x.i])

    def join_words(self, x):
        return WordArray(self.i + x.i)

    def join_floats(self, x):
        return FloatArray([float(y) for y in self.i] + x.i)

    def join_mixed(self, x):
        return MixedArray([Word(y) for y in self.i] + x.i)

    def join_dictionary(self, x):
        if len(self.i) == 2:
            y = Word(self.i[0])

            results = []
            matched = False
            for pair in x.i:
                key = pair.first()
                if key.match(y) == Word.true():
                    matched = True
                    results.append(x)
                else:
                    results.append(pair)
            if not matched:
                results.append(x)
            return MixedArray(results)
        else:
            return MixedArray([self, x])

    def less_scalar(self, x):
        return WordArray([Word(y).less(x).i for y in self.i])

    def less_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).less(Word(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def less_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).less(Float(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def less_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).less(z).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    # match Integer: Word.false
    # match Real: Word.false
    def match_words(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        else:
            if len(self.i) == len(x.i):
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if y != z:
                        return Word.false()
                return Word.true()
            else:
                return Word.false()

    def match_floats(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        else:
            if len(self.i) == len(x.i):
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    diff = abs(float(y) - z)
                    if diff > Float.tolerance():
                        return Word.false()
                return Word.true()
            else:
                return Word.false()

    def match_mixed(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        else:
            if len(self.i) == len(x.i):
                zipped = zip(self.i, x.i)
                for y, z in zipped:
                    if Float(y).match(z) != Word.true():
                        return Word.false()
                return Word.true()
            else:
                return Word.false()

    def max_word(self, x):
        results = []
        for y in self.i:
            if y > x.i:
                results.append(y)
            else:
                results.append(x.i)
        return WordArray(results)

    def max_float(self, x):
        results = []
        for y in self.i:
            if float(y) > x.i:
                results.append(y)
            else:
                results.append(x.i)
        return FloatArray(results)

    def max_words(self, x):
        results = []
        for y in self.i:
            result = Word(y)
            for z in x.i:
                result = result.max(Word(z))
            results.append(result.i)
        return WordArray(results)

    def max_floats(self, x):
        results = []
        for y in self.i:
            result = Float(y)
            for z in x.i:
                result = result.max(Float(z))
            results.append(result.i)
        return FloatArray(results)

    def max_mixed(self, x):
        results = []
        for y in self.i:
            result = Float(y)
            for z in x.i:
                result = result.max(z)
            results.append(result)
        return MixedArray(results)

    def min_word(self, x):
        results = []
        for y in self.i:
            if y < x.i:
                results.append(y)
            else:
                results.append(x.i)
        return WordArray(results)

    def min_float(self, x):
        results = []
        for y in self.i:
            if float(y) < x.i:
                results.append(y)
            else:
                results.append(x.i)
        return FloatArray(results)

    def min_words(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = Word(y)
                for z in x.i:
                    result = result.min(Word(z))
                results.append(result.i)
            return WordArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def min_floats(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.min(Float(z))
                results.append(result.i)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def min_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = Float(y)
                for z in x.i:
                    result = result.min(z)
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_word(self, x):
        return WordArray([y - x.i for y in self.i])

    def minus_float(self, x):
        return FloatArray([float(y) - x.i for y in self.i])

    def minus_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y - z)
            return WordArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(float(y) - z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Word(y).minus(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def more_scalar(self, x):
        return WordArray([Word(y).more(x).i for y in self.i])

    def more_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).more(Word(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def more_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).more(Float(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def more_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Word(y).more(z).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def plus_word(self, x):
        return WordArray([float(y) + float(x.i) for y in self.i])

    def plus_float(self, x):
        return FloatArray([float(y) + x.i for y in self.i])

    def plus_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(float(y) + float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(float(y) + z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Word(y).plus(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def power_scalar(self, x):
        return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))

    def power_list(self, x):
        return MixedArray(list(map(lambda y: Word(y).power(x), self.i)))

    # FIXME implement reshape

    def remainder_word(self, x):
        return WordArray(list(map(lambda y: y % x.i, self.i)))

    # remainder float unsupported

    def remainder_words(self, x):
        return MixedArray(list(map(lambda y: Word(y).remainder(x), self.i)))

    # remainder floats unsupported

    def remainder_mixed(self, x):
        return MixedArray(list(map(lambda y: Word(y).remainder(x), self.i)))

    def rotate_word(self, x):
        if len(self.i) == 0:
            return self
        elif x.i == 0:
            return self
        elif 1 <= x.i <= len(self.i):
            return self.drop(x).join(self.take(x))
        elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return self.reverse().rotate(x.negate()).reverse()
        elif x.i > len(self.i):
            return self.rotate(Word(x.i % len(self.i)))
        elif x.i < 0 and abs(x.i) > len(self.i):
            return self.rotate(Word(-(abs(x.i) % len(self.i))))

    # rotate float, words, floats, mixed: unsupported

    def split_word(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        elif 0 < x.i <= len(self.i):
            return MixedArray([WordArray(self.i[:x.i]), WordArray(self.i[x.i:])])
        else:
            return error.Error.out_of_bounds()

    def split_float(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        elif x.i == 0.0:
            return WordArray([])
        elif 0.0 < x.i <= 1.0:
            count = len(self.i)
            extent = float(count) * x.i
            lowIndex = int(extent)
            return self.split(Word(lowIndex))
        else:
            return error.Error.out_of_bounds()

    def split_words(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = x.i[index]
                split  = working.split(Word(offset))
                if split.o == NounType.ERROR:
                    return split

                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def split_floats(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = Float(x.i[index])
                split  = working.split(offset)
                if len(split.i) != 2:
                    return error.Error.out_of_bounds()
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def split_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = x.i[index]
                split  = working.split(offset)
                if len(split.i) != 2:
                    return error.Error.out_of_bounds()
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def take_word(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        elif x.i == 0:
            return WordArray([])
        elif 1 <= x.i <= len(self.i):
           return WordArray(self.i[:x.i])
        elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return WordArray(self.i[-x.i:])
        elif x.i > len(self.i):
            copies = x.i // len(self.i)
            remainder = x.i % len(self.i)
            results = []
            for y in range(copies):
                results = results + self.i
            results = results + self.take(Word(remainder)).i
            return WordArray(results)
        else: # x.i < 0 and abs(x.i) > len(self.i)
            return self.reverse().take(x.negate()).reverse()

    def take_float(self, x):
        if x.match(Float(0.0)) == Word.true():
            return WordArray([])
        elif x.match(Float(1.0)) == Word.true():
            return self
        elif len(self.i) == 0:
            return self
        elif x.more(Float(0)) == Word.true():
            if x.less(Float(1.0)) == Word.true():
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.take(Word(lowIndex))
            else: # x > 1.0
                replication = int(x.i)
                remainder = x.i - float(replication)
                replicated = self.take(Word(replication * len(self.i)))
                remaindered = self.take(Float(remainder))
                return replicated.join(remaindered)
        else: # x < 0
            return self.reverse().take(x.negate()).reverse()

    def take_words(self, x):
        if len(self.i) == 0:
            return WordArray([])

        if len(x.i) == 0:
            return WordArray([])
        else:
            results = []
            for y in x.i:
                result = self.take(Word(y))
                if isinstance(result, error.Error):
                    return result
                else:
                    results.append(result)
            return MixedArray(results)

    def take_floats(self, x):
        if len(self.i) == 0:
            return WordArray([])

        if len(x.i) == 0:
            return WordArray([])
        else:
            results = []
            for y in x.i:
                results.append(self.take(Float(y)))
            return MixedArray(results)

    def take_mixed(self, x):
        if len(self.i) == 0:
            return WordArray([])

        if len(x.i) == 0:
            return WordArray([])
        else:
            results = []
            for y in x.i:
                result = self.take(y)
                if isinstance(result, error.Error):
                    return result
                else:
                    results.append(result)
            return MixedArray(results)

    def times_word(self, x):
        return WordArray([y * x.i for y in self.i])

    def times_float(self, x):
        return FloatArray([float(y) * x.i for y in self.i])

    def times_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y * z)
            return WordArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(float(y) * z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Word(y).times(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    # def replicate(self, x):
    #     if x.t == StorageType.WORD_ARRAY:
    #         if len(self.i) == len(x.i):
    #             results = []
    #             zipped = zip(self.i, x.i)
    #             for y, z in zipped:
    #                 results = results + ([y]*z)
    #             return WordArray(results)
    #         else:
    #             return error.Error.invalid_argument()
    #     else:
    #         return error.Error.invalid_argument()

    # Monadic adverbs

    # converge: Storage.converge

    @staticmethod
    def each_impl(i, f):
        return MixedArray([Noun.dispatchMonad(Word(y), f) for y in i.i])

    def eachPair_impl(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append(Noun.dispatchDyad(Word(y), f, Word(z)))
        return MixedArray(results)

    def over_impl(self, f):
        if len(self.i) == 0:
            return self
        elif len(self.i) == 1:
            return self
        else:
            accumulator = 0
            for index, y in enumerate(self.i):
                if index == 0:
                    accumulator = Word(y)
                else:
                    accumulator = Noun.dispatchDyad(accumulator, f, Word(y))
            return accumulator

    # scanConverging: Storage.scanConverging_impl

    def scanOver_impl(self, f):
        if len(self.i) == 0:
            return WordArray([])
        else:
            current = Word(self.i[0])
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = Noun.dispatchDyad(current, f, Word(y))
                results.append(current)
            return MixedArray(results)

    # Dyadic adverbs
    def each2_scalar(self, f, x):
        return MixedArray([Noun.dispatchDyad(Word(y), f, x) for y in self.i])

    def each2_words(self, f, x):
        results = []
        #FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [Word(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_floats(self, f, x):
        results = []
        #FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [Float(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_mixed(self, f, x):
        results = []
        #FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [z for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    # eachLeft word: Storage.eachLeft_scalar
    # eachLeft float: Storage.eachLeft_scalar
    # eachLeft words: Storage.eachLeft_words
    # eachLeft floats: Storage.eachLeft_floats
    # eachLeft mixed: Storage.eachLeft_mixed

    # eachRight word: Storage.eachRight_scalar
    # eachRight float: Storage.eachRight_scalar
    # eachRight words: Storage.eachRight_words
    # eachRight floats: Storage.eachRight_floats
    # eachRight mixed: Storage.eachRight_mixed

    def overNeutral_impl(self, f, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = Noun.dispatchDyad(accumulator, f, Word(y))
            return accumulator

    # iterate: Storage.iterate_word

    # scanIterating: Storage.scanIterating_word

    def scanOverNeutral_impl(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = Noun.dispatchDyad(current, f, Word(y))
            results.append(current)
        return MixedArray(results)

    # scanWhileOne: Storage.scanWhileOne_impl

    # whileOne: Storage.whileOne_impl

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

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.FLOAT_ARRAY, list(map(lambda y: float(y), x)))

    def __str__(self):
        return "F%s" % str(self.i)

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.t.value)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += struct.pack("f", y)

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    # Monads

    # atom: Storage.atom_list

    # char: unsupported

    # complementation: Storage.complementation

    # enclose: Storage.enclose_impl

    # enumerate: unsupported

    def first_impl(self):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            return Float(self.i[0])

    def floor_impl(self):
        return WordArray([math.floor(y) for y in self.i])

    # format: unimplemented FIXME

    def gradeDown_impl(self):
        return self.gradeUp().reverse()

    def gradeUp_impl(self):
        return WordArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    # def group_impl(self):
    #     keys = self.unique()
    #     values = []
    #     for key in keys.i:
    #         indexes = []
    #         for index in range(len(self.i)):
    #             if self.i[index] == key:
    #                 indexes.append(index + 1)
    #         values.append(WordArray(indexes))
    #     return Dictionary(keys, MixedArray(values))

    # negate: Storage.negate_impl

    # reciprocal: Storage.reciprocal

    def reverse_impl(self):
        return FloatArray(list(reversed(self.i)))

    def shape_impl(self):
        if len(self.i) == 0:
            return Word(0)
        else:
            return WordArray([len(self.i)])

    def size_impl(self):
        return Word(len(self.i))

    # transpose: Storage.identity

    def unique_impl(self):
        return FloatArray(list(dict.fromkeys(self.i)))

    # Dyads

    # amend word, float: unsupported
    # def amend_words(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_floats(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_mixed(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()

    def cut_word(self, x):
        return self.drop(x)

    # cut float: unsupported

    def cut_words(self, x):
        if len(x.i) == 0:
            return MixedArray([self])
        else:
            previous = None
            results = []
            for y in x.i:
                if y >= 1:
                    if previous is None:
                        results.append(WordArray(self.i[:y - 1]))
                        previous = y
                    else:
                        if previous <= y:
                            results.append(WordArray(self.i[previous - 1:y - 1]))
                            previous = y
                        else:
                            return error.Error.invalid_argument()
                else:
                    return error.Error.invalid_argument()
            if previous is None:
                return MixedArray(results)
            else:
                results.append(WordArray(self.i[previous - 1:]))
                return MixedArray(results)

    # cut floats: unsupported

    def cut_mixed(self, x):
        first = x.i[0]
        if first.t != StorageType.WORD:
            return error.Error.invalid_argument()
        rest = x.i[1:]
        results = []
        for y in rest:
            last = y
            if last.t != StorageType.WORD:
                return error.Error.invalid_argument()
            if first.i <= last.i:
                results.append(FloatArray(self.i[first.i:last.i]))
            else:
                return error.Error.invalid_argument()
        return MixedArray(results)

    def divide_word(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return WordArray([float(y) / float(x.i) for y in self.i])

    def divide_float(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return FloatArray([float(y) / x.i for y in self.i])

    def divide_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.i == 0:
                    return error.Error.division_by_zero()
                else:
                    results.append(y / float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.i == 0:
                    return error.Error.division_by_zero()
                else:
                    results.append(y / z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                if x.match(Word(0)):
                    return error.Error.division_by_zero()
                else:
                    results.append(Float(y).divide(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def drop_word(self, x):
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
        else: # abs(x.i) > len(self.i)
            return FloatArray([])

    # drop float, words, floats, mixed: unsupported

    def equal_scalar(self, x):
        return WordArray([Float(y).equal(x).i for y in self.i])

    def equal_words(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if Float(y).match(Word(z)) == Word.true():
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    def equal_floats(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if Float(y).match(Float(z)) == Word.true():
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    def equal_mixed(self, x):
        if len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if Float(y).equal(z) == Word.true():
                    results.append(1)
                else:
                    results.append(0)
            return WordArray(results)
        else:
            return error.Error.shape_mismatch()

    def find_word(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return self.find(WordArray([x.i]))

    def find_float(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return self.find(FloatArray([x.i]))

    def find_words(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if Float(y).match(Word(z)) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    def find_floats(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
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
            return WordArray(results)

    def find_mixed(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if Float(y).match(z) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    # form: unimplemented FIXME

    # format2: unimplemented FIXME

    def index_word(self, x):
        if x.i < 1 or x.i > len(self.i):
            return error.Error.out_of_bounds()
        else:
            return Float(self.i[x.i - 1])

    def index_float(self, x):
        count = len(self.i)
        extent = x.i * float(count)
        offset = int(extent)
        return self.index(Word(offset))

    def index_words(self, x):
        return FloatArray([self.i[y-1] for y in x.i])

    def index_floats(self, x):
        return FloatArray([self.index(Float(y)).i for y in x.i])

    def index_mixed(self, x):
        return FloatArray([self.index(y).i for y in x.i])

    # indexInDepth: unimplemented FIXME

    # integerDivide: unimplemented FIXME

    def join_word(self, x):
        return FloatArray(self.i + [float(x.i)])

    def join_float(self, x):
        return FloatArray(self.i + [x.i])

    def join_words(self, x):
        return FloatArray(self.i + [float(y) for y in x.i])

    def join_floats(self, x):
        return FloatArray(self.i + x.i)

    def join_mixed(self, x):
        return MixedArray([Float(y) for y in self.i] + x.i)

    def join_dictionary(self, x):
        if len(self.i) == 2:
            y = Float(self.i[0])

            results = []
            matched = False
            for pair in x.i:
                key = pair.first()
                if key.match(y) == Word.true():
                    matched = True
                    results.append(x)
                else:
                    results.append(pair)
            if not matched:
                results.append(x)
            return MixedArray(results)
        else:
            return MixedArray([self, x])

    def less_scalar(self, x):
        return WordArray([Float(y).less(x).i for y in self.i])

    def less_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).less(Word(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def less_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).less(Float(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def less_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).less(z).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    # match word, float: Word.false
    def match_words(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word.false()
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                diff = abs(y - float(z))
                if diff > Float.tolerance():
                    return Word.false()
            return Word.true()

    def match_floats(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word.false()
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                diff = abs(y - z)
                if diff > Float.tolerance():
                    return Word.false()
            return Word.true()

    def match_mixed(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word(0)
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                if Float(y).match(z) != Word(1):
                    return Word.false()
            return Word.true()

    def max_word(self, x):
        results = []
        for y in self.i:
            if y > float(x.i):
                results.append(y)
            else:
                results.append(float(x.i))
        return FloatArray(results)

    def max_float(self, x):
        results = []
        for y in self.i:
            if y > x.i:
                results.append(y)
            else:
                results.append(x.i)
        return FloatArray(results)

    def max_words(self, x):
        results = []
        for y in self.i:
            maxy = float(y)
            for z in x.i:
                maxy = max(maxy, float(z))
            results.append(maxy)
        return FloatArray(results)

    def max_floats(self, x):
        results = []
        for y in self.i:
            maxy = y
            for z in x.i:
                maxy = max(y, z)
            results.append(maxy)
        return FloatArray(results)

    def max_mixed(self, x):
        results = []
        for y in self.i:
            maxy = Float(y)
            for z in x.i:
                maxy = maxy.max(z)
            results.append(maxy)
        return MixedArray(results)

    def min_word(self, x):
        results = []
        for y in self.i:
            if y - float(x.i) > Float.tolerance():
                results.append(float(x.i))
            else:
                results.append(y)
        return FloatArray(results)

    def min_float(self, x):
        results = []
        for y in self.i:
            if y - x.i > Float.tolerance():
                results.append(float(x.i))
            else:
                results.append(y)
        return FloatArray(results)

    def min_words(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
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
                return error.Error.unequal_array_lengths()
        else:
            return error.Error.unequal_array_lengths()

    def min_floats(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
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
                return error.Error.unequal_array_lengths()
        else:
            return error.Error.unequal_array_lengths()

    def min_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            if len(self.i) == len(x.i):
                for y, z in zip(self.i, x.i):
                    results.append(Float(y).min(z))
                return MixedArray(results)
            else:
                return error.Error.unequal_array_lengths()
        else:
            return error.Error.unequal_array_lengths()

    def minus_word(self, x):
        return FloatArray([y - float(x.i) for y in self.i])

    def minus_float(self, x):
        return FloatArray([y - x.i for y in self.i])

    def minus_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y - float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y - z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Float(y).minus(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def more_scalar(self, x):
        return WordArray([Float(y).more(x).i for y in self.i])

    def more_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).more(Float(float(z))).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def more_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).more(Float(z)).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def more_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return WordArray([])
        elif len(self.i) == len(x.i):
            return WordArray([Float(y).more(z).i for y, z in zip(self.i, x.i)])
        else:
            return error.Error.unequal_array_lengths()

    def plus_word(self, x):
        return FloatArray([y + float(x.i) for y in self.i])

    def plus_float(self, x):
        return FloatArray([y + x.i for y in self.i])

    def plus_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y + float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y + z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Float(y).plus(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def power_scalar(self, x):
        return FloatArray(list(map(lambda y: math.pow(y, x.i), self.i)))

    def power_list(self, x):
        return MixedArray(list(map(lambda y: Float(y).power(x), self.i)))

    # FIXME implement reshape

    # remainder unsupported

    def rotate_word(self, x):
        if len(self.i) == 0:
            return self
        elif x.i == 0:
            return self
        elif 1 <= x.i <= len(self.i):
            return self.drop(x).join(self.take(x))
        elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return self.reverse().rotate(x.negate()).reverse()
        elif x.i > len(self.i):
            return self.rotate(Word(x.i % len(self.i)))
        elif x.i < 0 and abs(x.i) > len(self.i):
            return self.rotate(Word(-(abs(x.i) % len(self.i))))

    # rotate float, words, floats, mixed: unsupported

    def split_word(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            if 0 < x.i <= len(self.i):
                return MixedArray([FloatArray(self.i[:x.i]), FloatArray(self.i[x.i:])])
            else:
                return error.Error.out_of_bounds()

    def split_float(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            if x.i == 0.0:
                return FloatArray([])
            elif 0.0 < x.i <= 1.0:
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.split(Word(lowIndex))
            else:
                return error.Error.out_of_bounds()

    def split_words(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in x.i:
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = Word(x.i[index])
                split  = working.split(offset)
                if split.o == NounType.ERROR:
                    return split
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def split_floats(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            if len(x.i) == 0:
                return FloatArray([])
            else:
                results = []
                working = self
                for extent in x.i:
                    offset = int(extent * len(working.i))
                    split  = working.split(Word(offset))
                    if split.o == NounType.ERROR:
                        return split
                    else:
                        results.append(split.i[0])
                        working = split.i[1]
                results.append(working)
                return MixedArray(results)

    def split_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            if len(x.i) == 0:
                return FloatArray([])
            else:
                results = []
                working = self
                for y in x.i:
                    split  = working.split(y)
                    if split.o == NounType.ERROR:
                        return split
                    else:
                        results.append(split.i[0])
                        working = split.i[1]
                results.append(working)
                return MixedArray(results)

    def take_word(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
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
            results = results + self.take(Word(remainder)).i
            return FloatArray(results)
        else:  # x.i < 0 and abs(x.i) > len(self.i)
            return self.reverse().take(x.negate()).reverse()

    def take_float(self, x):
        if x.match(Float(0.0)) == Word.true():
            return FloatArray([])
        elif x.match(Float(1.0)) == Word.true():
            return self
        elif len(self.i) == 0:
            return self
        elif x.more(Float(0)) == Word.true():
            if x.less(Float(1.0)) == Word.true():
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.take(Word(lowIndex))
            else: # x > 1.0
                replication = int(x.i)
                remainder = x.i - float(replication)
                replicated = self.take(Word(replication * len(self.i)))
                remaindered = self.take(Float(remainder))
                return replicated.join(remaindered)
        else: # x < 0
            return self.reverse().take(x.negate()).reverse()

    def take_words(self, x):
        if len(self.i) == 0:
            return FloatArray([])

        if len(x.i) == 0:
            return FloatArray([])
        else:
            results = []
            for y in x.i:
                result = self.take(Word(y))
                if isinstance(result, error.Error):
                    return result
                else:
                    results.append(result)
            return MixedArray(results)

    def take_floats(self, x):
        if len(self.i) == 0:
            return FloatArray([])

        if len(x.i) == 0:
            return FloatArray([])
        else:
            results = []
            for y in x.i:
                results.append(self.take(Float(y)))
            return MixedArray(results)

    def take_mixed(self, x):
        if len(self.i) == 0:
            return FloatArray([])

        if len(x.i) == 0:
            return FloatArray([])
        else:
            results = []
            for y in x.i:
                result = self.take(y)
                if isinstance(result, error.Error):
                    return result
                else:
                    results.append(result)
            return MixedArray(results)

    def times_word(self, x):
        return FloatArray([y * float(x.i) for y in self.i])

    def times_float(self, x):
        return FloatArray([y * x.i for y in self.i])

    def times_words(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y * float(z))
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_floats(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(y * z)
            return FloatArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_mixed(self, x):
        if len(self.i) == 0 and len(x.i) == 0:
            return self
        elif len(x.i) == len(self.i):
            results = []
            for y, z in zip(self.i, x.i):
                results.append(Float(y).times(z))
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    # Monadic adverbs

    # converge: Storage.converge_impl

    @staticmethod
    def each_impl(i, f):
        return MixedArray([Noun.dispatchMonad(Float(y), f) for y in i.i])

    def eachPair_impl(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append((Noun.dispatchDyad(Float(y), f, Float(z))))
        return MixedArray(results)

    def over_impl(self, f):
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
                    accumulator = Noun.dispatchDyad(accumulator, f, Float(y))
            return accumulator

    # scanConverging: Storage.scanConverging_impl

    def scanOver_impl(self, f):
        if len(self.i) == 0:
            return FloatArray([])
        else:
            current = Float(self.i[0])
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = Noun.dispatchDyad(current, f, Float(y))
                results.append(current)
            return MixedArray(results)

    # Dyadic adverbs

    def each2_scalar(self, f, x):
        return MixedArray([Noun.dispatchDyad(Float(y), f, x) for y in self.i])

    def each2_words(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [Word(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_floats(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [Float(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_mixed(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip([Word(y) for y in self.i], [z for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    # eachLeft word: Storage.eachLeft_scalar
    # eachLeft float: Storage.eachLeft_scalar
    # eachLeft words: Storage.eachLeft_words
    # eachLeft floats: Storage.eachLeft_floats
    # eachLeft mixed: Storage.eachLeft_mixed

    # eachRight word: Storage.eachRight_scalar
    # eachRight float: Storage.eachRight_scalar
    # eachRight words: Storage.eachRight_words
    # eachRight floats: Storage.eachRight_floats
    # eachRight mixed: Storage.eachRight_mixed

    def overNeutral_impl(self, f, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = Noun.dispatchDyad(accumulator, f, Float(y))
            return accumulator

    # iterate word: Storage.iterate_word
    # iterate float, words, floats, mixed: unsupported

    # scanIterating word: Storage.scanIterating_word
    # scanIterating float, words, floats, mixed: unsupported

    def scanOverNeutral_impl(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = Noun.dispatchDyad(current, f, Float(y))
            results.append(current)
        return MixedArray(results)

    # scanWhileOne: Storage.scanWhileOne_impl

    # whileOne: Storage.whileOne_impl

    # def replicate(self, x):
    #     if x.t == StorageType.WORD_ARRAY:
    #         if len(self.i) == len(x.i):
    #             results = []
    #             zipped = zip(self.i, x.i)
    #             for y, z in zipped:
    #                 results = results + ([y]*z)
    #             return FloatArray(results)
    #         else:
    #             return error.Error.invalid_argument()
    #     else:
    #         return error.Error.invalid_argument()

    # def iterate(self, f, x):
    #     if x.t == StorageType.WORD:
    #         if x.i >= 0:
    #             current = self
    #             truth = x
    #             while truth != Word(0):
    #                 current = Noun.dispatchMonad(current, f)
    #                 truth = truth.minus(Word(1))
    #             return current
    #         else:
    #             return error.Error.invalid_adverb_argument()
    #     else:
    #         return error.Error.invalid_argument()

class MixedArray(Storage):
    @staticmethod
    def from_bytes(data):
        rest = data
        results = []
        while len(rest) > 0:
            result, rest = Storage.from_bytes(rest)
            results.append(result)
        return MixedArray(results), rest

    def __init__(self, x, o=NounType.LIST):
        super().__init__(o, StorageType.MIXED_ARRAY, x)

    def __str__(self):
        return "M[%s]" % ", ".join(list(map(lambda x: str(x), self.i)))

    def __hash__(self):
        return hash(self.i)

    def to_bytes(self):
        typeBytes = struct.pack("B", self.t.value)

        floatArrayBytes = b''
        for y in self.i:
            floatArrayBytes += y.to_bytes()

        data = typeBytes + floatArrayBytes

        length = len(data)
        lengthBytes = squeeze(length)

        return lengthBytes + data

    # Monads

    # atom: Storage.atom_list

    # char: hotpatched by character.py to avoid circular imports

    # complementation: Storage.complementation_impl

    # enclose: Storage.enclose_impl

    # enumerate: unsupported

    def first_impl(self):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            return self.i[0]

    def floor_impl(self):
        return MixedArray([x.floor() for x in self.i])

    # format: unimplemented FIXME

    def gradeDown_impl(self):
        return self.gradeUp().reverse()

    def gradeUp_impl(self):
        return WordArray(sorted(range(1, len(self.i) + 1), key=lambda y: self.i[y - 1]))

    # def group_impl(self):
    #     keys = self.unique()
    #     values = []
    #     for key in keys.i:
    #         indexes = []
    #         for index in range(len(self.i)):
    #             if self.i[index] == key:
    #                 indexes.append(index + 1)
    #         values.append(WordArray(indexes))
    #     return Dictionary(keys, MixedArray(values))

    # negate: Storage.negate_impl

    # reciprocal: Storage.reciprocal

    def reverse_impl(self):
        return MixedArray(list(reversed(self.i)))

    def shape_impl(self):
        if len(self.i) == 0:
            return Word(0)
        else:
            shapes = [y.shape() for y in self.i]
            firstShape = shapes[0]
            if firstShape.t == StorageType.WORD: # atom in array means shape is simple vector type
                return WordArray([len(self.i)])
            elif firstShape.t == StorageType.WORD_ARRAY:
                for shape in shapes[1:]:
                    if shape != firstShape: # assorted internal shapes means shape is simple vector type
                        return WordArray([len(self.i)])
                return WordArray([len(self.i)] + firstShape.i) # identical internal shapes adds one layer to the shape vector

    def size_impl(self):
        return Word(len(self.i))

    def transpose_impl(self):
        if len(self.i) == 0:
            return self
        elif all(map(lambda y: y.t == StorageType.WORD_ARRAY, self.i)):
            zipped = list(zip(*[y.i for y in self.i]))
            arrays = [WordArray(list(y)) for y in zipped]
            return MixedArray(arrays)
        elif all(map(lambda y: y.t == StorageType.FLOAT_ARRAY, self.i)):
            zipped = list(zip(*[y.i for y in self.i]))
            arrays = [FloatArray(list(y)) for y in zipped]
            return MixedArray(arrays)
        else:
            return error.Error.invalid_argument()

    def unique_impl(self):
        return MixedArray(list(dict.fromkeys(self.i)))

    # Dyads

    # amend word, float: unsupported
    # def amend_words(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_floats(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()
    #
    # def amend_mixed(self, x):
    #     if len(self.i) == len(x.i):
    #         return Dictionary(self, x)
    #     else:
    #         return error.Error.invalid_argument()

    def cut_word(self, x):
        return self.drop(x)

    # cut float: unsupported

    def cut_words(self, x):
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
                            return error.Error.invalid_argument()
                else:
                    return error.Error.invalid_argument()
            if previous is None:
                return MixedArray(results)
            else:
                results.append(MixedArray(self.i[previous-1:]))
                return MixedArray(results)

    # cut floats: unsupported

    def cut_mixed(self, x):
        if len(x.i) == 0:
            return MixedArray([self])
        else:
            previous = None
            results = []
            for y in x.i:
                if y.t == StorageType.WORD:
                    if y.i >= 1:
                        if previous is None:
                            results.append(MixedArray(self.i[:y.i-1]))
                            previous = y.i
                        else:
                            if previous <= y.i:
                                results.append(MixedArray(self.i[previous-1:y.i-1]))
                                previous = y.i
                            else:
                                return error.Error.invalid_argument()
                    else:
                        return error.Error.invalid_argument()
                else:
                    return error.Error.invalid_argument()

            if previous is None:
                return MixedArray(results)
            else:
                results.append(MixedArray(self.i[previous-1:]))
                return MixedArray(results)

    def divide_word(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return MixedArray([y.divide(x) for y in self.i])

    def divide_float(self, x):
        results = []
        for y in self.i:
            result = y.divide(x)
            if result.o == NounType.ERROR:
                return result
            else:
                results.append(result)
        return MixedArray(results)

    def divide_words(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if z == 0:
                    return error.Error.division_by_zero()
                else:
                    result = y.divide(Word(z))
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_floats(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.divide(Float(z))
                if result.o == NounType.ERROR:
                    return result
                else:
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def divide_mixed(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.divide(z)
                if result.o == NounType.ERROR:
                    return result
                else:
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def drop_word(self, x):
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
            return MixedArray([])

    # drop float, words, floats, mixed: unsupported

    def equal_impl(self, x):
        return WordArray([y.equal(x).i for y in self.i])

    # expand: unimplemented FIXME

    def find_word(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return WordArray([y.match(x).i for y in self.i])

    def find_float(self, x):
        if len(self.i) == 0:
            return WordArray([])
        else:
            return WordArray([y.match(x).i for y in self.i])

    def find_words(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if y.match(Word(z)) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    def find_floats(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if y.match(Float(z)) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    def find_mixed(self, x):
        if len(self.i) == 0:
            return WordArray([])
        elif len(x.i) == 0:
            return WordArray([0] * len(self.i))
        else:
            results = []
            for offset in range(len(self.i)):
                if len(self.i[offset:]) >= len(x.i):
                    arraySlice = self.i[offset:offset+len(x.i)]
                    zipped = zip(arraySlice, x.i)
                    matched = True
                    for y, z in zipped:
                        if y.match(z) != Word(1):
                            matched = False
                            break
                    if matched:
                        results.append(1)
                    else:
                        results.append(0)
                else:
                    results.append(0)
            return WordArray(results)

    # form: unimplemented FIXME

    # format2: unimplemented FIXME

    def index_word(self, x):
        if x.i < 1 or x.i > len(self.i):
            return error.Error.out_of_bounds()
        else:
            return self.i[x.i - 1]

    def index_float(self, x):
        count = len(self.i)
        extent = x.i * float(count)
        offset = int(extent)
        return self.index(Word(offset))

    def index_words(self, x):
        return MixedArray([self.index(Word(y)) for y in x.i])

    def index_floats(self, x):
        return MixedArray([self.index(Float(y)) for y in x.i])

    def index_mixed(self, x):
        return MixedArray([self.index(y) for y in x.i])

    # indexInDepth: unimplemented FIXME

    def integerDivide_word(self, x):
        if x.i == 0:
            return error.Error.division_by_zero()
        else:
            return MixedArray([y.integerDivide(x) for y in self.i])

    # integerDivide float: unsupported

    def integerDivide_words(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                if z == 0:
                    return error.Error.division_by_zero()
                else:
                    result = y.integerDivide(Word(z))
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    # integerDivide floats: unsupported

    def integerDivide_mixed(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.integerDivide(z)
                if result.o == NounType.ERROR:
                    return result
                else:
                    results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def join_scalar(self, x):
        return MixedArray(self.i + [x])

    def join_words(self, x):
        return MixedArray(self.i + [Word(y) for y in x.i])

    def join_floats(self, x):
        return MixedArray(self.i + [Float(y) for y in x.i])

    def join_mixed(self, x):
        return MixedArray(self.i + x.i)

    def join_dictionary(self, x):
        if len(self.i) == 2:
            y = self.i[0]

            results = []
            matched = False
            for pair in x.i:
                key = pair.first()
                if key.match(y) == Word.true():
                    matched = True
                    results.append(x)
                else:
                    results.append(pair)
            if not matched:
                results.append(x)
            return MixedArray(results)
        else:
            return MixedArray([self, x])

    def less_impl(self, x):
        return WordArray([y.less(x).i for y in self.i])

    # match word, float: Word.false
    def match_words(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word.false()
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                if y.match(Word(z)) != Word.true():
                    return Word.false()
            return Word.true()

    def match_floats(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word.false()
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                if y.match(Float(z)) != Word.true():
                    return Word.false()
            return Word.true()

    def match_mixed(self, x):
        if len(self.i) == 0:
            if len(x.i) == 0:
                return Word.true()
            else:
                return Word.false()
        elif len(self.i) != len(x.i):
            return Word.false()
        else:
            zipped = zip(self.i, x.i)
            for y, z in zipped:
                if y.match(z) != Word.true():
                    return Word.false()
            return Word.true()

    def max_word(self, x):
        results = []
        for y in self.i:
            results.append(y.max(x))
        return MixedArray(results)

    def max_float(self, x):
        results = []
        for y in self.i:
            results.append(y.max(x))
        return MixedArray(results)

    def max_words(self, x):
        results = []
        for y in self.i:
            result = y
            for z in x.i:
                result = result.max(Word(z))
            results.append(result)
        return MixedArray(results)

    def max_floats(self, x):
        results = []
        for y in self.i:
            result = y
            for z in x.i:
                result = result.max(Float(z))
            results.append(result)
        return MixedArray(results)

    def max_mixed(self, x):
        results = []
        for y in self.i:
            result = y
            for z in x.i:
                result = result.max(z)
            results.append(result)
        return MixedArray(results)

    def min_word(self, x):
        results = []
        for y in self.i:
            results.append(y.min(x))
        return MixedArray(results)

    def min_float(self, x):
        results = []
        for y in self.i:
            results.append(y.min(x))
        return MixedArray(results)

    def min_words(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(Word(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def min_floats(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(Float(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def min_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        elif len(x.i) == 0:
            return error.Error.empty_argument()
        elif len(self.i) == len(x.i):
            results = []
            for y in self.i:
                result = y
                for z in x.i:
                    result = result.min(z)
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_word(self, x):
        return MixedArray([y.minus(x) for y in self.i])

    def minus_float(self, x):
        results = []
        for y in self.i:
            result = y.minus(x)
            results.append(result)
        return MixedArray(results)

    def minus_words(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.minus(Word(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_floats(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.minus(Float(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def minus_mixed(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.minus(z)
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def more_impl(self, x):
        return WordArray([y.more(x).i for y in self.i])

    def plus_word(self, x):
        return MixedArray([y.plus(x) for y in self.i])

    def plus_float(self, x):
        results = []
        for y in self.i:
            result = y.plus(x)
            results.append(result)
        return MixedArray(results)

    def plus_words(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.plus(Word(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_floats(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.plus(Float(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def plus_mixed(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.plus(z)
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def power_impl(self, x):
        return MixedArray(list(map(lambda y: y.power(x), self.i)))

    # FIXME reshape unimplemented

    def remainder_impl(self, x):
        return MixedArray(list(map(lambda y: y.remainder(x), self.i)))

    # remainder float, floats: unsupported

    def rotate_word(self, x):
        if len(self.i) == 0:
            return self
        elif x.i == 0:
            return self
        elif 1 <= x.i <= len(self.i):
            return self.drop(x).join(self.take(x))
        elif x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return self.reverse().rotate(x.negate()).reverse()
        elif x.i > len(self.i):
            return self.rotate(Word(x.i % len(self.i)))
        elif x.i < 0 and abs(x.i) > len(self.i):
            return self.rotate(Word(-(abs(x.i) % len(self.i))))

    def split_word(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        elif 0 < x.i <= len(self.i):
            return MixedArray([MixedArray(self.i[:x.i]), MixedArray(self.i[x.i:])])
        else:
            return error.Error.out_of_bounds()

    def split_float(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        elif x.i == 0.0:
            return MixedArray([])
        elif 0.0 < x.i <= 1.0:
            count = len(self.i)
            extent = float(count) * x.i
            lowIndex = int(extent)
            return self.split(Word(lowIndex))
        else:
            return error.Error.out_of_bounds()

    def split_words(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = Word(x.i[index])
                split  = working.split(offset)
                if split.o == NounType.ERROR:
                    return split
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def split_floats(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = Float(x.i[index])
                split  = working.split(offset)
                if split.o == NounType.ERROR:
                    return split
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def split_mixed(self, x):
        if len(self.i) == 0:
            return error.Error.out_of_bounds()
        else:
            results = []
            working = self
            for index in range(len(x.i)):
                if len(working.i) == 0:
                    return error.Error.out_of_bounds()
                offset = x.i[index]
                split  = working.split(offset)
                if split.o == NounType.ERROR:
                    return split
                results.append(split.i[0])
                working = split.i[1]
            results.append(working)
            return MixedArray(results)

    def take_word(self, x):
        if len(self.i) == 0:
            return MixedArray([])

        if x.i == 0:
            return MixedArray([])

        if 1 <= x.i <= len(self.i):
           return MixedArray(self.i[:x.i])

        if x.i < 0 and 1 <= abs(x.i) <= len(self.i):
            return MixedArray(self.i[-x.i:])

        if x.i > len(self.i):
            copies = x.i // len(self.i)
            remainder = x.i % len(self.i)
            results = []
            for y in range(copies):
                results = results + self.i
            results = results + self.take(Word(remainder)).i
            return MixedArray(results)

        # x.i < 0 and abs(x.i) > len(self.i)
        return self.reverse().take(x.negate()).reverse()

    def take_float(self, x):
        if len(self.i) == 0:
            return MixedArray([])

        if x.match(Float(0.0)) == Word.true():
            return MixedArray([])

        if x.match(Float(1.0)) == Word.true():
            return self

        if len(self.i) == 0:
            return self

        if x.more(Float(0)) == Word.true():
            if x.less(Float(1.0)) == Word.true():
                count = len(self.i)
                extent = float(count) * x.i
                lowIndex = int(extent)
                return self.take(Word(lowIndex))
            else: # x > 1.0
                replication = int(x.i)
                remainder = x.i - float(replication)
                replicated = self.take(Word(replication * len(self.i)))
                remaindered = self.take(Float(remainder))
                return replicated.join(remaindered)

        # x < 0
        return self.reverse().take(x.negate()).reverse()

    def take_words(self, x):
        if len(self.i) == 0:
            return MixedArray([])

        if len(x.i) == 0:
            return MixedArray([])

        results = []
        for y in x.i:
            result = self.take(Word(y))
            if isinstance(result, error.Error):
                return result
            else:
                results.append(result)
        return MixedArray(results)

    def take_floats(self, x):
        if len(self.i) == 0:
            return MixedArray([])

        if len(x.i) == 0:
            return MixedArray([])

        results = []
        for y in x.i:
            results.append(self.take(Float(y)))
        return MixedArray(results)

    def take_mixed(self, x):
        if len(self.i) == 0:
            return MixedArray([])

        if len(x.i) == 0:
            return MixedArray([])

        results = []
        for y in x.i:
            result = self.take(y)
            if isinstance(result, error.Error):
                return result
            else:
                results.append(result)
        return MixedArray(results)

    def times_word(self, x):
        return MixedArray([y.times(x) for y in self.i])

    def times_float(self, x):
        results = []
        for y in self.i:
            result = y.times(x)
            results.append(result)
        return MixedArray(results)

    def times_words(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.times(Word(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_floats(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.times(Float(z))
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    def times_mixed(self, x):
        if len(self.i) == 0:
            return self
        elif len(self.i) == len(x.i):
            results = []
            for y, z in zip(self.i, x.i):
                result = y.times(z)
                results.append(result)
            return MixedArray(results)
        else:
            return error.Error.unequal_array_lengths()

    # def replicate(self, x):
    #     if x.t == StorageType.WORD_ARRAY:
    #         if len(self.i) == len(x.i):
    #             results = []
    #             zipped = zip(self.i, x.i)
    #             for y, z in zipped:
    #                 results = results + ([y]*z)
    #             return MixedArray(results)
    #         else:
    #             return error.Error.invalid_argument()
    #     else:
    #         return error.Error.invalid_argument()

    # Monadic adverbs

    # Dyadic adverbs

    # Monadic adverbs

    # converge: Storage.converge_impl

    @staticmethod
    def each_impl(i, f):
        return MixedArray([Noun.dispatchMonad(y, f) for y in i.i])

    def eachPair_impl(self, f):
        results = []
        for index, y in enumerate(self.i):
            if index != len(self.i) - 1:
                z = self.i[index + 1]
                results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def over_impl(self, f):
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
                    accumulator = Noun.dispatchDyad(accumulator, f, y)
            return accumulator

    # scanConverging: FIXME - unimplemented

    def scanOver_impl(self, f):
        if len(self.i) == 0:
            return MixedArray([])
        else:
            current = self.i[0]
            rest = self.i[1:]
            results = [current]
            for y in rest:
                current = Noun.dispatchDyad(current, f, y)
                results.append(current)
            return MixedArray(results)

    # Dyadic adverbs

    def each2_scalar(self, f, x):
        return MixedArray([Noun.dispatchDyad(y, f, x) for y in self.i])

    def each2_words(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip(self.i, [Word(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_floats(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip(self.i, [Float(z) for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    def each2_mixed(self, f, x):
        results = []
        # FIXME - make this work for arrays on unequal lengths
        for y, z in zip(self.i, [z for z in x.i]):
            results.append(Noun.dispatchDyad(y, f, z))
        return MixedArray(results)

    # eachLeft word: Storage.eachLeft_scalar
    # eachLeft float: Storage.eachLeft_scalar
    # eachLeft words: Storage.eachLeft_words
    # eachLeft floats: Storage.eachLeft_floats
    # eachLeft mixed: Storage.eachLeft_mixed

    # eachRight word: Storage.eachRight_scalar
    # eachRight float: Storage.eachRight_scalar
    # eachRight words: Storage.eachRight_words
    # eachRight floats: Storage.eachRight_floats
    # eachRight mixed: Storage.eachRight_mixed

    def overNeutral_impl(self, f, x):
        if len(self.i) == 0:
            return error.Error.empty_argument()
        else:
            accumulator = x
            for index, y in enumerate(self.i):
                accumulator = Noun.dispatchDyad(accumulator, f, y)
            return accumulator

    # iterate: Storage.iterate_word
    # iterate float, words, floats, mixed: unsupported

    # scanIterating: Storage.scanIterating_word
    # scanIterating float, words, floats, mixed: unsupported

    def scanOverNeutral_impl(self, f, x):
        current = x
        results = [current]
        for y in self.i:
            current = Noun.dispatchDyad(current, f, y)
            results.append(current)
        return MixedArray(results)

    # scanWhileOne: Storage.scanWhileOne_impl

    # whileOne: Storage.whileOne_impl

    # def apply(self, x, rop):
    #     results = []
    #     for y in self.i:
    #         result = rop(x, y)
    #         if result.o == NounType.ERROR:
    #             return result
    #         else:
    #             results.append(result)
    #
    #     return MixedArray(results)

    # def iterate(self, f, x):
    #     if x.t == StorageType.WORD:
    #         if x.i >= 0:
    #             current = self
    #             truth = x
    #             while truth != Word(0):
    #                 current = Noun.dispatchMonad(current, f)
    #                 truth = truth.minus(Word(1))
    #             return current
    #         else:
    #             return error.Error.invalid_adverb_argument()
    #     else:
    #         return error.Error.invalid_argument()

# class Dictionary:
#     def __init__(self, keys, values):
#         self.map = {}
#         if keys.t == StorageType.WORD_ARRAY:
#             for index, key in enumerate(keys.i):
#                 value = values.index(Word(index + 1))
#                 self.map[Word(key)] = value
#         elif keys.t == StorageType.FLOAT_ARRAY:
#             for index, key in enumerate(keys.i):
#                 value = values.index(Word(index + 1))
#                 self.map[Word(key)] = value
#         if keys.t == StorageType.MIXED_ARRAY:
#             for index, key in enumerate(keys.i):
#                 value = values.index(Word(index + 1))
#                 self.map[key] = value
#
#     def __eq__(self, x):
#         if not isinstance(x, Dictionary):
#             return False
#         return self.map == x.map
#
#     def __str__(self):
#         result = "{"
#         for key, value in self.map.items():
#             result += str(key) + ":" + str(value) + ", "
#         result += "}"
#         return result
#
#     def get(self, key):
#         if key in self.map:
#             return self.map[key]
#         else:
#             return error.Error.unknown_key()
#
#     def put(self, key, value):
#         newMap = self.map.copy()
#         newMap[key] = value
#         keys = []
#         values = []
#         for key, value in newMap.items():
#             keys.append(key)
#             values.append(value)
#         if all(map(lambda y: y.t == StorageType.WORD, keys)):
#             if all(map(lambda y: y.t == StorageType.WORD, values)):
#                 return Dictionary(WordArray([y.i for y in keys]), WordArray([y.i for y in values]))
#             elif all(map(lambda y: y.t == StorageType.FLOAT, values)):
#                 return Dictionary(WordArray([y.i for y in keys]), FloatArray([y.i for y in values]))
#             else:
#                 return Dictionary(WordArray(keys), MixedArray(values))
#         elif all(map(lambda y: y.t == StorageType.FLOAT, keys)):
#             if all(map(lambda y: y.t == StorageType.WORD, values)):
#                 return Dictionary(FloatArray([y.i for y in keys]), WordArray([y.i for y in values]))
#             elif all(map(lambda y: y.t == StorageType.FLOAT, values)):
#                 return Dictionary(FloatArray([y.i for y in keys]), FloatArray([y.i for y in values]))
#             else:
#                 return Dictionary(FloatArray([y.i for y in keys]), MixedArray(values))
#         else:
#             if all(map(lambda y: y.t == StorageType.WORD, values)):
#                 return Dictionary(MixedArray(keys), WordArray([y.i for y in values]))
#             elif all(map(lambda y: y.t == StorageType.FLOAT, values)):
#                 return Dictionary(MixedArray(keys), FloatArray([y.i for y in values]))
#             else:
#                 return Dictionary(MixedArray(keys), MixedArray(values))
#
#     def contains(self, key):
#         if key in self.map:
#             return Word(1)
#         else:
#             return Word(0)
#
#     def remove(self, key):
#         pairs = self.items()
#         transposed = pairs.transpose()
#         keys = transposed.index(Word(1))
#         values = transposed.index(Word(2))
#         if keys.t == StorageType.WORD_ARRAY:
#             index = keys.i.index(key.i)
#             if index == -1:
#                 return error.Error.unknown_key()
#             del keys.i[index]
#             del values.i[index]
#             return Dictionary(keys, values)
#         elif keys.t == StorageType.FLOAT_ARRAY:
#             index = keys.i.index(key.i)
#             if index == -1:
#                 return error.Error.unknown_key()
#             del keys.i[index]
#             del values.i[index]
#             return Dictionary(keys, values)
#         elif keys.t == StorageType.MIXED_ARRAY:
#             index = keys.i.index(key)
#             if index == -1:
#                 return error.Error.unknown_key()
#             del keys.i[index]
#             del values.i[index]
#             return Dictionary(keys, values)
#         else:
#             return error.Error.unsupported_object()
#
#     def keys(self):
#         result = self.map.keys()
#         if all(map(lambda y: y.t == StorageType.WORD, result)):
#             return WordArray([y.i for y in result])
#         elif all(map(lambda y: y.t == StorageType.FLOAT, result)):
#             return FloatArray([y.i for y in result])
#         else:
#             return MixedArray(result)
#
#     def values(self):
#         result = self.map.values()
#         if all(map(lambda y: y.t == StorageType.WORD, result)):
#             return WordArray([y.i for y in result])
#         elif all(map(lambda y: y.t == StorageType.FLOAT, result)):
#             return FloatArray([y.i for y in result])
#         else:
#             return MixedArray(result)
#
#     def items(self):
#         results = []
#         for key, value in self.map.items():
#             if key.t == StorageType.WORD and value.t == StorageType.WORD:
#                 results.append(WordArray([key.i, value.i]))
#             elif key.t == StorageType.FLOAT and value.t == StorageType.FLOAT:
#                 results.append(FloatArray([key.i, value.i]))
#             else:
#                 results.append(MixedArray([key, value]))
#         return MixedArray(results)
