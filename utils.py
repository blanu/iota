from storage import NounType, StorageType

def identity(i):
    return i

def expand_dispatch(f):
    return match_dispatch(f, f, f, f, f)

def match_dispatch(a, b, c, d, e, dictionary=None):
    if dictionary is None:
        return {
            (NounType.INTEGER, StorageType.WORD): a,
            (NounType.REAL, StorageType.FLOAT): b,
            (NounType.LIST, StorageType.WORD_ARRAY): c,
            (NounType.LIST, StorageType.FLOAT_ARRAY): d,
            (NounType.LIST, StorageType.MIXED_ARRAY): e,
        }
    else:
        return {
            (NounType.INTEGER, StorageType.WORD): a,
            (NounType.REAL, StorageType.FLOAT): b,
            (NounType.LIST, StorageType.WORD_ARRAY): c,
            (NounType.LIST, StorageType.FLOAT_ARRAY): d,
            (NounType.LIST, StorageType.MIXED_ARRAY): e,
            (NounType.DICTIONARY, StorageType.MIXED_ARRAY): dictionary,
        }

def match_dispatch_dictionary_string(a, b, c, d, e, f, g):
    return {
        (NounType.INTEGER, StorageType.WORD): a,
        (NounType.REAL, StorageType.FLOAT): b,
        (NounType.LIST, StorageType.WORD_ARRAY): c,
        (NounType.LIST, StorageType.FLOAT_ARRAY): d,
        (NounType.LIST, StorageType.MIXED_ARRAY): e,
        (NounType.DICTIONARY, StorageType.MIXED_ARRAY): f,
        (NounType.STRING, StorageType.WORD_ARRAY): g,
    }

def expand_dispatch_character_string(f):
    return {
        (NounType.INTEGER, StorageType.WORD): f,
        (NounType.REAL, StorageType.FLOAT): f,
        (NounType.LIST, StorageType.WORD_ARRAY): f,
        (NounType.LIST, StorageType.FLOAT_ARRAY): f,
        (NounType.LIST, StorageType.MIXED_ARRAY): f,
        (NounType.CHARACTER, StorageType.WORD): f,
        (NounType.STRING, StorageType.WORD_ARRAY): f,
    }
