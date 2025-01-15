import error
import storage

class MetaNoun(type):
    def __new__(cls, name, bases, dct):
        # Create the class
        obj = super().__new__(cls, name, bases, dct)

        # Initialize static properties
        obj.dispatch = {}

        return obj

class Noun(metaclass=MetaNoun):
    @staticmethod
    def dispatchMonad(i, f):
        d = Noun.dispatch
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            monad = storage.Monads(f.i)
            if not monad:
                return storage.Word(error.ErrorTypes.BAD_OPERATION, o=storage.NounType.ERROR)
        else:
            return storage.Word(error.ErrorTypes.BAD_OPERATION, o=storage.NounType.ERROR)

        if not (i.o, i.t) in Noun.dispatch:
            return storage.Word(error.ErrorTypes.UNSUPPORTED_OBJECT.value, o=storage.NounType.ERROR)

        verbs = Noun.dispatch[(i.o, i.t)]
        if not monad in verbs:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        verb = verbs[monad]
        return verb(i)

    @staticmethod
    def dispatchDyad(i, f, x):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            dyad = storage.Dyads(f.i)
            if not dyad:
                return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)
        else:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        if not (i.o, i.t) in Noun.dispatch:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        verbs = Noun.dispatch[(i.o, i.t)]
        if not dyad in verbs:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        verb = verbs[dyad]
        if not (x.o, x.t) in verb:
            return storage.Word(error.ErrorTypes.INVALID_ARGUMENT.value, o=storage.NounType.ERROR)

        specialization = verb[(x.o, x.t)]
        return specialization(i, x)

    @staticmethod
    def dispatchTriad(i, f, x, y):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            triad = storage.Triads(f.i)
            if not triad:
                return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)
        else:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        if not (i.o, i.t) in Noun.dispatch:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        verbs = Noun.dispatch[(i.o, i.t)]
        if not triad in verbs:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        verb = verbs[triad]
        if not (x.o, x.t) in verb:
            return storage.Word(error.ErrorTypes.INVALID_ARGUMENT.value, o=storage.NounType.ERROR)

        specialization = verb[(x.o, x.t)]
        return specialization(i, x, y)

    @staticmethod
    def dispatchMonadicAdverb(i, f, g):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            symbol = storage.MonadicAdverbs(f.i)
            if not symbol:
                return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)
        else:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        if not (i.o, i.t) in Noun.dispatch:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        adverbs = Noun.dispatch[(i.o, i.t)]

        if not symbol in adverbs:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)
        adverb = adverbs[symbol]
        return adverb(i, g)

    @staticmethod
    def dispatchDyadicAdverb(i, f, g, x):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            symbol = storage.DyadicAdverbs(f.i)
            if not symbol:
                return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)
        else:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        if not (i.o, i.t) in Noun.dispatch:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        adverbs = Noun.dispatch[(i.o, i.t)]
        if not symbol in adverbs:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        adverb = adverbs[symbol]

        if not (x.o, x.t) in adverb:
            return storage.Word(error.ErrorTypes.BAD_OPERATION.value, o=storage.NounType.ERROR)

        specialization = adverb[(x.o, x.t)]
        return specialization(i, g, x)
