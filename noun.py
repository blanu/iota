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
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            monad = storage.Monads(f.i)
            if not monad:
                return error.Error.bad_operation()
        else:
            return error.Error.bad_operation()

        if not (i.o, i.t) in Noun.dispatch:
            return error.Error.unsupported_object()

        verbs = Noun.dispatch[(i.o, i.t)]
        if not monad in verbs:
            return error.Error.bad_operation()

        verb = verbs[monad]
        return verb(i)

    @staticmethod
    def dispatchDyad(i, f, x):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            dyad = storage.Dyads(f.i)
            if not dyad:
                return error.Error.bad_operation()
        else:
            return error.Error.bad_operation()

        if not (i.o, i.t) in Noun.dispatch:
            return error.Error.bad_operation()

        verbs = Noun.dispatch[(i.o, i.t)]
        if not dyad in verbs:
            return error.Error.bad_operation()

        verb = verbs[dyad]
        if not (x.o, x.t) in verb:
            return error.Error.invalid_argument()

        specialization = verb[(x.o, x.t)]
        return specialization(i, x)

    @staticmethod
    def dispatchTriad(i, f, x, y):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            triad = storage.Triads(f.i)
            if not triad:
                return error.Error.bad_operation()
        else:
            return error.Error.bad_operation()

        if not (i.o, i.t) in Noun.dispatch:
            return error.Error.bad_operation()

        verbs = Noun.dispatch[(i.o, i.t)]
        if not triad in verbs:
            return error.Error.bad_operation()

        verb = verbs[triad]
        if not (x.o, x.t) in verb:
            return error.Error.invalid_argument()

        specialization = verb[(x.o, x.t)]
        return specialization(i, x, y)

    @staticmethod
    def dispatchMonadicAdverb(i, f, g):
        d = Noun.dispatch
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            symbol = storage.Adverbs(f.i)
            if not symbol:
                return error.Error.bad_operation()
        else:
            return error.Error.bad_operation()

        if not (i.o, i.t) in Noun.dispatch:
            return error.Error.bad_operation()

        adverbs = Noun.dispatch[(i.o, i.t)]

        if not symbol in adverbs:
            return error.Error.bad_operation()
        adverb = adverbs[symbol]
        return adverb(i, g)

    @staticmethod
    def dispatchDyadicAdverb(i, f, g, x):
        if i.o == storage.NounType.ERROR:
            return i

        if f.t == storage.StorageType.WORD:
            symbol = storage.Adverbs(f.i)
            if not symbol:
                return error.Error.bad_operation()
        else:
            return error.Error.bad_operation()

        if not (i.o, i.t) in Noun.dispatch:
            return error.Error.bad_operation()

        adverbs = Noun.dispatch[(i.o, i.t)]
        if not symbol in adverbs:
            return error.Error.bad_operation()

        adverb = adverbs[symbol]

        if not (x.o, x.t) in adverb:
            return error.Error.bad_operation()

        specialization = adverb[(x.o, x.t)]
        return specialization(i, g, x)
