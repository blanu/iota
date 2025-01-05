# class IStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i):
#         return IStorageRegisterNetwork(StorageRegister.allocate(i))
#
#     @staticmethod
#     def allocateZero():
#         return IStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir):
#         self.ir = ir
#
#     def dispatchMonad(self, f):
#         return self.ir.dispatchMonad(f)
#
#     def dispatchDyad(self, f, x):
#         return self.ir.dispatchDyad(f, x)
#
# class FStorageRegisterNetwork:
#     @staticmethod
#     def allocate(f):
#         return FStorageRegisterNetwork(StorageRegister.allocate(f))
#
#     def __init__(self, fr):
#         self.fr = fr
#
#     def dispatchMonad(self, i):
#         f = self.fr.i
#         return i.dispatchMonad(f)
#
#     def dispatchDyad(self, i, x):
#         f = self.fr.i
#         return i.dispatchDyad(f, x)
#
# class XStorageRegisterNetwork:
#     @staticmethod
#     def allocate(x):
#         return XStorageRegisterNetwork(StorageRegister.allocate(x))
#
#     @staticmethod
#     def allocateZero():
#         return XStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, xr):
#         self.xr = xr
#
#     def dispatchDyad(self, i, f):
#         x = self.xr.i
#         return i.dispatchDyad(f, x)
#
# class RStorageRegisterNetwork:
#     @staticmethod
#     def allocate(r):
#         return RStorageRegisterNetwork(StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZero():
#         return RStorageRegisterNetwork(StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, r):
#         self.r = r
#
#     def dispatchMonad(self, i, f):
#         self.r.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, i, f, x):
#         self.r.i = i.dispatchDyad(f, x)
#
# class IFStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, f):
#         return IFStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f))
#
#     @staticmethod
#     def allocateZero(f):
#         return IFStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(f))
#
#     def __init__(self, ir, fr):
#         self.ir = ir
#         self.fr = fr
#
#     def dispatchMonad(self):
#         i = self.ir.i
#         f = self.fr.i
#         return i.dispatchMonad(f)
#
#     def dispatchDyad(self, x):
#         i = self.ir.i
#         f = self.fr.i
#         return i.dispatchDyad(f, x)
#
# class IXStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, x):
#         return IXStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(x))
#
#     @staticmethod
#     def allocateZeros():
#         return IXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, xr):
#         self.ir = ir
#         self.xr = xr
#
#     def dispatchMonad(self, f):
#         i = self.ir.i
#         return i.dispatchMonad(f)
#
#     def dispatchDyad(self, f):
#         i = self.ir.i
#         x = self.xr.i
#         return i.dispatchDyad(f, x)
#
# class IRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, r):
#         return IRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return IRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, rr):
#         self.ir = ir
#         self.rr = rr
#
#     def dispatchMonad(self, f):
#         i = self.ir.i
#         self.ir.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, f, x):
#         i = self.ir.i
#         self.ir.i = i.dispatchDyad(f, x)
#
# class FXStorageRegisterNetwork:
#     @staticmethod
#     def allocate(f, x):
#         return FXStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(x))
#
#     @staticmethod
#     def allocateZeros():
#         return FXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, fr, xr):
#         self.fr = fr
#         self.xr = xr
#
#     def dispatchMonad(self, i):
#         f = self.fr.i
#         return i.dispatchDyad(f)
#
#     def dispatchDyad(self, i, x):
#         f = self.fr.i
#         return i.dispatchDyad(f, x)
#
# class FRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(f, r):
#         return FRStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return FRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, fr, rr):
#         self.fr = fr
#         self.rr = rr
#
#     def dispatchMonad(self, i):
#         f = self.fr.i
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, i, x):
#         f = self.fr.i
#         self.rr.i = i.dispatchDyad(f, x)
#
# class XRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(x, r):
#         return XRStorageRegisterNetwork(StorageRegister.allocate(x), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return XRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, xr, rr):
#         self.xr = xr
#         self.rr = rr
#
#     def dispatchMonad(self, i, f):
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, i, f):
#         x = self.xr.i
#         self.rr.i = i.dispatchDyad(f, x)
#
# class IFXStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, f, x):
#         return IFXStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(x))
#
#     @staticmethod
#     def allocateZeros():
#         return IFXStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, fr, xr):
#         self.ir = ir
#         self.fr = fr
#         self.xr = xr
#
#     def dispatchMonad(self):
#         i = self.ir.i
#         f = self.fr.i
#         return i.dispatchMonad(f)
#
#     def dispatchDyad(self):
#         i = self.ir.i
#         f = self.fr.i
#         x = self.xr.i
#         return i.dispatchDyad(f, x)
#
# class IFRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, f, r):
#         return IFRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return IFRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, fr, rr):
#         self.ir = ir
#         self.fr = fr
#         self.rr = rr
#
#     def dispatchMonad(self):
#         i = self.ir.i
#         f = self.fr.i
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, x):
#         i = self.ir.i
#         f = self.fr.i
#         self.rr.i = i.dispatchDyad(f, x)
#
# class IXRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, x, r):
#         return IXRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(x), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZero():
#         return IXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, xr, rr):
#         self.ir = ir
#         self.xr = xr
#         self.rr = rr
#
#     def dispatchMonad(self, f):
#         i = self.ir.i
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, f):
#         i = self.ir.i
#         x = self.xr.i
#         self.rr.i = i.dispatchDyad(f, x)
#
# class FXRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(f, x, r):
#         return FXRStorageRegisterNetwork(StorageRegister.allocate(f), StorageRegister.allocate(x), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return FXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, fr, xr, rr):
#         self.fr = fr
#         self.xr = xr
#         self.rr = rr
#
#     def dispatchMonad(self, i):
#         f = self.fr.i
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self, i):
#         f = self.fr.i
#         x = self.xr.i
#         self.rr.i = i.dispatchDyad(f, x)
#
# class IFXRStorageRegisterNetwork:
#     @staticmethod
#     def allocate(i, f, x, r):
#         return IFXRStorageRegisterNetwork(StorageRegister.allocate(i), StorageRegister.allocate(f), StorageRegister.allocate(x), StorageRegister.allocate(r))
#
#     @staticmethod
#     def allocateZeros():
#         return IFXRStorageRegisterNetwork(StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)), StorageRegister.allocate(Integer(0)))
#
#     def __init__(self, ir, fr, xr, rr):
#         self.ir = ir
#         self.fr = fr
#         self.xr = xr
#         self.rr = rr
#
#     def dispatchMonad(self):
#         i = self.ir.i
#         f = self.fr.i
#         self.rr.i = i.dispatchMonad(f)
#
#     def dispatchDyad(self):
#         i = self.ir.i
#         f = self.fr.i
#         x = self.xr.i
#         self.rr.i = i.dispatchDyad(f, x)

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
