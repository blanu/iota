import storage

def identity(i):
    return i

def expand_dispatch(f):
    return match_dispatch(f, f, f, f, f)

def match_dispatch(a, b, c, d, e, dictionary=None):
    if dictionary is None:
        return {
            (storage.NounType.INTEGER, storage.StorageType.WORD): a,
            (storage.NounType.REAL, storage.StorageType.FLOAT): b,
            (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): c,
            (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): d,
            (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): e,
        }
    else:
        return {
            (storage.NounType.INTEGER, storage.StorageType.WORD): a,
            (storage.NounType.REAL, storage.StorageType.FLOAT): b,
            (storage.NounType.LIST, storage.StorageType.WORD_ARRAY): c,
            (storage.NounType.LIST, storage.StorageType.FLOAT_ARRAY): d,
            (storage.NounType.LIST, storage.StorageType.MIXED_ARRAY): e,
            (storage.NounType.DICTIONARY, storage.StorageType.MIXED_ARRAY): dictionary,
        }
