from character import Character, integer_word_char_impl, list_words_char_impl, list_mixed_char_impl
from dictionary import Dictionary
from error import Error
from integer import Integer
from iotaString import String
from iotaSymbol import Symbol
from list import List
import noun
from real import Real
import storage

# Apply hot patches. Doing it this way avoid circular imports.

noun.Noun.dispatch[(storage.NounType.INTEGER, storage.StorageType.WORD)][storage.Monads.char] = integer_word_char_impl
noun.Noun.dispatch[(storage.NounType.LIST, storage.StorageType.WORD_ARRAY)][storage.Monads.char] = list_words_char_impl
noun.Noun.dispatch[(storage.NounType.LIST, storage.StorageType.MIXED_ARRAY)][storage.Monads.char] = list_mixed_char_impl

__all__ = ["Character", "Dictionary", "Error", "Integer", "List", "Real", "String", "Symbol"]
