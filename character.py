# from iota import *
# from noun import Noun, MetaNoun
# from integer import Integer
# from real import Real

# class Character(Noun):
#     def __init__(self, s):
#         if isinstance(s, Word):
#             super().__init__(ObjectType.CHARACTER, s)
#         elif isinstance(s, Character):
#             super().__init__(ObjectType.CHARACTER, s.s)
#         elif type(s) == str:
#             super().__init__(ObjectType.CHARACTER, Word(s))
#         else:
#             raise Exception('invalid argument type')
#
#         self.monadDispatchTable = {
#             StorageMonads.atom: self.atom
#         }
#
#         self.dyadDispatchTable = {}
#         for symbol, function in [
#             (StorageDyads.cut, self.__cut),
#             (StorageDyads.divide, self.__divide),
#             (StorageDyads.drop, self.__drop),
#         ]:
#             self.dyadDispatchTable[symbol] = {}
#             for objectType in [ObjectType.INTEGER, ObjectType.REAL, ObjectType.LIST]:
#                 self.dyadDispatchTable[symbol][objectType] = lambda x: function(x)
#
#     def amend(self, x):
#         return Error('invalid argument type')
#
#     # Returns - Word(1), in other words true
#     def atom(self):
#         return self.s.atom()
#
#     def char(self):
#         return Error('invalid argument type')
#
#     def cut(self, x):
#         return self.dispatchDyad(StorageDyads.cut, x)
#
#     def __cut(self, x):
#         return self.s.cut(x.s)
#
#     def define(self):
#         pass
#
#     def divide(self, x):
#         return self.dispatchDyad(StorageDyads.divide, x)
#
#     def __divide(self, x):
#         r = self.s.divide(x.s)
#         if r.t == StorageType.ERROR:
#             return r
#         else:
#             return Integer(r)
#
#     def drop(self, x):
#         return self.dispatchDyad(StorageDyads.drop, x)
#
#     def __drop(self, x):
#         return self.s.drop(x.s)
#
#     def enumerate(self):
#         return self.dispatchMonad(StorageMonads.enumerate)
#
#     def equal(self, x):
#         return self.s.equal(x.s)
#
#     def expand(self, x):
#         return self.s.expand(x.s)
#
#     def find(self, x):
#         return self.s.find(x.s)
#
#     def first(self):
#         return self.dispatchMonad(StorageMonads.first)
#
#     def floor(self):
#         return self.dispatchMonad(StorageMonads.floor)
#
#     def form(self):
#         pass
#
#     def format(self):
#         pass
#
#     def format2(self):
#         pass
#
#     def gradeUp(self):
#         return self.dispatchMonad(StorageMonads.gradeUp)
#
#     def gradeDown(self):
#         return self.dispatchMonad(StorageMonads.gradeDown)
#
#     def group(self):
#         pass
#
#     def index(self, x):
#         return self.s.index(x.s)
#
#     def indexInDepth(self, x):
#         return self.s.indexInDepth(x.s)
#
#     def integerDivide(self, x):
#         return self.s.integerDivide(x.s)
#
#     def join(self, x):
#         return self.s.join(x.s)
#
#     def less(self, x):
#         return self.s.less(x.s)
#
#     def list(self):
#         pass
#
#     def match(self, x):
#         return self.s.match(x.s)
#
#     def max(self, x):
#         return self.s.max(x.s)
#
#     def min(self, x):
#         return self.s.min(x.s)
#
#     def minus(self, x):
#         return self.s.minus(x.s)
#
#     def more(self, x):
#         return self.s.more(x.s)
#
#     def negate(self):
#         return self.dispatchMonad(StorageMonads.negate)
#
#     def complementation(self):
#         return self.dispatchMonad(StorageMonads.complementation)
#
#     def plus(self, x):
#         return self.s.plus(x.s)
#
#     def power(self, x):
#         return self.s.power(x.s)
#
#     def range(self, x):
#         pass
#
#     def reciprocal(self):
#         return self.dispatchMonad(StorageMonads.reciprocal)
#
#     def reshape(self, x):
#         pass
#
#     def remainder(self, x):
#         return self.s.remainder(x.s)
#
#     def reverse(self):
#         return self.dispatchMonad(StorageMonads.reverse)
#
#     def rotate(self, x):
#         pass
#
#     def shape(self):
#         return self.dispatchMonad(StorageMonads.shape)
#
#     def size(self):
#         return self.dispatchMonad(StorageMonads.size)
#
#     def split(self, x):
#         return self.s.split(x.s)
#
#     def take(self, x):
#         return self.s.take(x.s)
#
#     def times(self, x):
#         return self.s.times(x.s)
#
#     def transpose(self):
#         return self.dispatchMonad(StorageMonads.transpose)
#
#     def undefined(self):
#         pass
