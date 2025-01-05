from storage import *
from nouns import *
from testify import TestCase, assert_not_equal, assert_equal
from squeeze import squeeze, expand

# Examples from the book "An Introduction to Array Programming in Klong" by Nils
class BookTests(TestCase):
    pass

class Pythonic(TestCase):
    def test_eq(self):
        assert_equal(Word(1), Word(1))
        assert_not_equal(Word(1), Word(2))

        assert_not_equal(Word(1), Float(1))
        assert_not_equal(Word(1), Float(2))

        assert_not_equal(Word(1), WordArray([1]))
        assert_not_equal(Word(1), FloatArray([1]))
        assert_not_equal(Word(1), MixedArray([Word(1)]))

        assert_equal(Float(1), Float(1))
        assert_not_equal(Float(1), Float(2))

        assert_not_equal(Float(1), Word(1))
        assert_not_equal(Float(1), Word(2))

        assert_not_equal(Float(1), WordArray([1]))
        assert_not_equal(Float(1), FloatArray([1]))
        assert_not_equal(Float(1), MixedArray([Word(1)]))

        assert_equal(WordArray([1]), WordArray([1]))
        assert_not_equal(WordArray([1]), WordArray([2]))

        assert_not_equal(WordArray([1]), FloatArray([1]))
        assert_not_equal(WordArray([1]), FloatArray([2]))

        assert_equal(FloatArray([1]), FloatArray([1]))
        assert_not_equal(FloatArray([1]), FloatArray([2]))

        assert_not_equal(FloatArray([1]), MixedArray([Word(1)]))
        assert_not_equal(FloatArray([1]), MixedArray([Float(2)]))

        assert_not_equal(FloatArray([1]), Word(1))
        assert_not_equal(FloatArray([1]), Float(1))

        assert_equal(MixedArray([Word(1)]), MixedArray([Word(1)]))
        assert_not_equal(MixedArray([Word(1)]), MixedArray([Word(2)]))

        assert_not_equal(MixedArray([Word(1)]), WordArray([1]))
        assert_not_equal(MixedArray([Word(1)]), WordArray([2]))

        assert_not_equal(MixedArray([Word(1)]), FloatArray([1]))
        assert_not_equal(MixedArray([Word(1)]), FloatArray([2]))

        assert_not_equal(MixedArray([Word(1)]), Word(1))
        assert_not_equal(MixedArray([Word(1)]), Float(1))

# Monads
class AtomTests(TestCase):
    # integer atom -> integer(1)
    # real atom -> integer(1)
    # list <i size equal 0> atom -> integer(1)
    # list <i size {equal 0} not> atom -> integer(0)
    # list atom -> integer(0)
    # char atom -> integer(1)

    def test_atom_word(self):
        assert_equal(Word(1).atom(), Word(1))

    def test_atom_float(self):
        assert_equal(Float(1).atom(), Word(1))

    def test_atom_word_array(self):
        assert_equal(WordArray([2, 3]).atom(), Word(0))

    def test_atom_real_array(self):
        assert_equal(FloatArray([2, 3]).atom(), Word(0))

    def test_atom_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).atom(), Word(0))

    def test_atom_integer(self):
        assert_equal(Integer.new(1).atom(), Integer.true())

    def test_atom_real(self):
        assert_equal(Real.new(1).atom(), Integer.true())

    def test_atom_list(self):
        assert_equal(List.new([2, 3]).atom(), Integer.false())
        assert_equal(List.new([2.0, 3.0]).atom(), Integer.false())
        assert_equal(List.new([2, 3.0]).atom(), Integer.false())

class PlusTests(TestCase):
    def test_plus_errors(self):
        assert_equal(Word(0).plus(Error.test_error()).o, NounType.ERROR)
        assert_equal(Float(0).plus(Error.test_error()).o, NounType.ERROR)
        assert_equal(WordArray([0]).plus(Error.test_error()).o, NounType.ERROR)
        assert_equal(FloatArray([0]).plus(Error.test_error()).o, NounType.ERROR)
        assert_equal(MixedArray([Word(0)]).plus(Error.test_error()).o, NounType.ERROR)

    def test_plus_word_word(self):
        assert_equal(Word(1).plus(Word(2)), Word(3))
        assert_equal(Word(-1).plus(Word(-1)), Word(-2))
        assert_equal(Word(0).plus(Word(0)), Word(0))

    def test_plus_word_real(self):
        assert_equal(Word(1).plus(Float(2)), Float(3))
        assert_equal(Word(-1).plus(Float(-1)), Float(-2))
        assert_equal(Word(0).plus(Float(0)), Float(0))

    def test_plus_word_word_array(self):
        assert_equal(Word(1).plus(WordArray([2, 3])), WordArray([3, 4]))
        assert_equal(Word(-1).plus(WordArray([-1, 0])), WordArray([-2, -1]))
        assert_equal(Word(0).plus(WordArray([0, 1])), WordArray([0, 1]))

    def test_plus_word_real_array(self):
        assert_equal(Word(1).plus(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Word(-1).plus(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Word(0).plus(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_plus_word_mixed_array(self):
        assert_equal(Word(1).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(3), Float(4)]))
        assert_equal(Word(-1).plus(MixedArray([Word(-1), Float(0)])), MixedArray([Word(-2), Float(-1)]))
        assert_equal(Word(0).plus(MixedArray([Word(0), Float(1)])), MixedArray([Word(0), Float(1)]))

    def test_plus_real_word(self):
        assert_equal(Float(1).plus(Word(2)), Float(3))
        assert_equal(Float(-1).plus(Word(-1)), Float(-2))
        assert_equal(Float(0).plus(Word(0)), Float(0))

    def test_plus_real_real(self):
        assert_equal(Float(1).plus(Float(2)), Float(3))
        assert_equal(Float(-1).plus(Float(-1)), Float(-2))
        assert_equal(Float(0).plus(Float(0)), Float(0))

    def test_plus_real_word_array(self):
        assert_equal(Float(1).plus(WordArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).plus(WordArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).plus(WordArray([0, 1])), FloatArray([0, 1]))

    def test_plus_real_real_array(self):
        assert_equal(Float(1).plus(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).plus(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).plus(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_plus_real_mixed_array(self):
        assert_equal(Float(1).plus(MixedArray([Word(2), Float(3)])), MixedArray([Float(3), Float(4)]))
        assert_equal(Float(-1).plus(MixedArray([Word(-1), Float(0)])), MixedArray([Float(-2), Float(-1)]))
        assert_equal(Float(0).plus(MixedArray([Word(0), Float(1)])), MixedArray([Float(0), Float(1)]))

    def test_plus_word_array_word(self):
        assert_equal(WordArray([2, 3]).plus(Word(1)), WordArray([3, 4]))
        assert_equal(WordArray([-1, 0]).plus(Word(-1)), WordArray([-2, -1]))
        assert_equal(WordArray([0, 1]).plus(Word(0)), WordArray([0, 1]))

    def test_plus_word_array_real(self):
        assert_equal(WordArray([2, 3]).plus(Float(1)), FloatArray([3, 4]))
        assert_equal(WordArray([-1, 0]).plus(Float(-1)), FloatArray([-2, -1]))
        assert_equal(WordArray([0, 1]).plus(Float(0)), FloatArray([0, 1]))

    def test_plus_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).plus(WordArray([2, 3])), FloatArray([4, 6]))
        assert_equal(WordArray([-1, 0]).plus(WordArray([2, 3])), FloatArray([1, 3]))
        assert_equal(WordArray([0, 1]).plus(WordArray([2, 3])), FloatArray([2, 4]))

    def test_plus_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).plus(FloatArray([2, 3])), FloatArray([4, 6]))
        assert_equal(WordArray([-1, 0]).plus(FloatArray([2, 3])),FloatArray([1, 3]))
        assert_equal(WordArray([0, 1]).plus(FloatArray([2, 3])), FloatArray([2, 4]))

    def test_plus_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(4), Float(6)]))
        assert_equal(WordArray([-1, 0]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(1), Float(3)]))
        assert_equal(WordArray([0, 1]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(4)]))

    def test_plus_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).plus(Word(2)), MixedArray([Word(4), Float(5)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).plus(Word(2)), MixedArray([Word(1), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1)]).plus(Word(2)), MixedArray([Word(2), Float(3)]))

    def test_plus_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).plus(Float(2)), MixedArray([Float(4), Float(5)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).plus(Float(2)), MixedArray([Float(1), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1)]).plus(Float(2)), MixedArray([Float(2), Float(3)]))

    def test_plus_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).plus(WordArray([2, 3])), MixedArray([Word(4), Float(6)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).plus(WordArray([2, 3])), MixedArray([Word(1), Float(3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).plus(WordArray([2, 3])), MixedArray([Word(2), Float(4)]))

    def test_plus_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).plus(FloatArray([2, 3])), MixedArray([Float(4), Float(6)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).plus(FloatArray([2, 3])), MixedArray([Float(1), Float(3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).plus(FloatArray([2, 3])), MixedArray([Float(2), Float(4)]))

    def test_plus_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(4), Float(6)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(1), Float(3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).plus(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(4)]))

class MinusTests(TestCase):
    def test_minus_errors(self):
        assert_equal(Word(0).minus(Error.test_error()).o, NounType.ERROR)
        assert_equal(Float(0).minus(Error.test_error()).o, NounType.ERROR)
        assert_equal(WordArray([0]).minus(Error.test_error()).o, NounType.ERROR)
        assert_equal(FloatArray([0]).minus(Error.test_error()).o, NounType.ERROR)
        assert_equal(MixedArray([Word(0)]).minus(Error.test_error()).o, NounType.ERROR)

    def test_minus_word_word(self):
        assert_equal(Word(1).minus(Word(2)), Word(-1))
        assert_equal(Word(-1).minus(Word(-1)), Word(0))
        assert_equal(Word(0).minus(Word(0)), Word(0))

    def test_minus_word_real(self):
        assert_equal(Word(1).minus(Float(2)), Float(-1))
        assert_equal(Word(-1).minus(Float(-1)), Float(0))
        assert_equal(Word(0).minus(Float(0)), Float(0))

    def test_minus_word_word_array(self):
        assert_equal(Word(1).minus(WordArray([2, 3])), WordArray([-1, -2]))
        assert_equal(Word(-1).minus(WordArray([-1, 0])), WordArray([0, -1]))
        assert_equal(Word(0).minus(WordArray([0, 1])), WordArray([0, -1]))

    def test_minus_word_real_array(self):
        assert_equal(Word(1).minus(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Word(-1).minus(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Word(0).minus(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_minus_word_mixed_array(self):
        assert_equal(Word(1).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(-1), Float(-2)]))
        assert_equal(Word(-1).minus(MixedArray([Word(-1), Float(0)])), MixedArray([Word(0), Float(-1)]))
        assert_equal(Word(0).minus(MixedArray([Word(0), Float(1)])), MixedArray([Word(0), Float(-1)]))

    def test_minus_real_word(self):
        assert_equal(Float(1).minus(Word(-1)), Float(2))
        assert_equal(Float(-1).minus(Word(0)), Float(-1))
        assert_equal(Float(0).minus(Word(0)), Float(0))

    def test_minus_real_real(self):
        assert_equal(Float(1).minus(Float(2)), Float(-1))
        assert_equal(Float(-1).minus(Float(-1)), Float(0))
        assert_equal(Float(0).minus(Float(0)), Float(0))

    def test_minus_real_word_array(self):
        assert_equal(Float(1).minus(WordArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).minus(WordArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).minus(WordArray([0, 1])), FloatArray([0, -1]))

    def test_minus_real_real_array(self):
        assert_equal(Float(1).minus(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).minus(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).minus(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_minus_real_mixed_array(self):
        assert_equal(Float(1).minus(MixedArray([Word(2), Float(3)])), MixedArray([Float(-1), Float(-2)]))
        assert_equal(Float(-1).minus(MixedArray([Word(-1), Float(0)])), MixedArray([Float(0), Float(-1)]))
        assert_equal(Float(0).minus(MixedArray([Word(0), Float(1)])), MixedArray([Float(0), Float(-1)]))

    def test_minus_word_array_word(self):
        assert_equal(WordArray([2, 3]).minus(Word(1)), WordArray([1, 2]))
        assert_equal(WordArray([-1, 0]).minus(Word(-1)), WordArray([0, 1]))
        assert_equal(WordArray([0, 1]).minus(Word(0)), WordArray([0, 1]))

    def test_minus_word_array_real(self):
        assert_equal(WordArray([2, 3]).minus(Float(1)), FloatArray([1, 2]))
        assert_equal(WordArray([-1, 0]).minus(Float(-1)), FloatArray([0, 1]))
        assert_equal(WordArray([0, 1]).minus(Float(0)), FloatArray([0, 1]))

    def test_minus_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).minus(WordArray([2, 3])), WordArray([0, 0]))
        assert_equal(WordArray([-1, 0]).minus(WordArray([2, 3])), WordArray([-3, -3]))
        assert_equal(WordArray([0, 1]).minus(WordArray([2, 3])), WordArray([-2, -2]))

    def test_minus_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).minus(FloatArray([2, 3])), FloatArray([0, 0]))
        assert_equal(WordArray([-1, 0]).minus(FloatArray([2, 3])), FloatArray([-3, -3]))
        assert_equal(WordArray([0, 1]).minus(FloatArray([2, 3])), FloatArray([-2, -2]))

    def test_minus_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(0), Float(0)]))
        assert_equal(WordArray([-1, 0]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(-3), Float(-3)]))
        assert_equal(WordArray([0, 1]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(-2), Float(-2)]))

    def test_minus_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).minus(Word(2)), MixedArray([Word(0), Float(1)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).minus(Word(2)), MixedArray([Word(-3), Float(-2)]))
        assert_equal(MixedArray([Word(0), Float(1)]).minus(Word(2)), MixedArray([Word(-2), Float(-1)]))

    def test_minus_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).minus(Float(2)), MixedArray([Float(0), Float(1)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).minus(Float(2)), MixedArray([Float(-3), Float(-2)]))
        assert_equal(MixedArray([Word(0), Float(1)]).minus(Float(2)), MixedArray([Float(-2), Float(-1)]))

    def test_minus_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).minus(WordArray([2, 3])), MixedArray([Word(0), Float(0)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).minus(WordArray([2, 3])), MixedArray([Word(-3), Float(-3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).minus(WordArray([2, 3])), MixedArray([Word(-2), Float(-2)]))

    def test_minus_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).minus(FloatArray([2, 3])), MixedArray([Float(0), Float(0)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).minus(FloatArray([2, 3])), MixedArray([Float(-3), Float(-3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).minus(FloatArray([2, 3])), MixedArray([Float(-2), Float(-2)]))

    def test_minus_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(0), Float(0)]))
        assert_equal(MixedArray([Word(-1), Float(0)]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(-3), Float(-3)]))
        assert_equal(MixedArray([Word(0), Float(1)]).minus(MixedArray([Word(2), Float(3)])), MixedArray([Word(-2), Float(-2)]))

class TimesTests(TestCase):
    def test_times_errors(self):
        assert_equal(Word(0).times(Error.test_error()).o, NounType.ERROR)
        assert_equal(Float(0).times(Error.test_error()).o, NounType.ERROR)
        assert_equal(WordArray([0]).times(Error.test_error()).o, NounType.ERROR)
        assert_equal(FloatArray([0]).times(Error.test_error()).o, NounType.ERROR)
        assert_equal(MixedArray([Word(0)]).times(Error.test_error()).o, NounType.ERROR)

    def test_times_word_word(self):
        assert_equal(Word(1).times(Word(2)), Word(2))

    def test_times_word_real(self):
        assert_equal(Word(1).times(Float(2)), Float(2))

    def test_times_word_word_array(self):
        assert_equal(Word(1).times(WordArray([2, 3])), WordArray([2, 3]))

    def test_times_word_real_array(self):
        assert_equal(Word(1).times(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_times_word_mixed_array(self):
        assert_equal(Word(1).times(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(3)]))

    def test_times_real_word(self):
        assert_equal(Float(1).times(Word(-1)), Float(-1))

    def test_times_real_real(self):
        assert_equal(Float(1).times(Float(2)), Float(2))

    def test_times_real_word_array(self):
        assert_equal(Float(1).times(WordArray([2, 3])), FloatArray([2, 3]))

    def test_times_real_real_array(self):
        assert_equal(Float(1).times(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_times_real_mixed_array(self):
        assert_equal(Float(1).times(MixedArray([Word(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_times_word_array_word(self):
        assert_equal(WordArray([2, 3]).times(Word(1)), WordArray([2, 3]))

    def test_times_word_array_real(self):
        assert_equal(WordArray([2, 3]).times(Float(1)), FloatArray([2, 3]))

    def test_times_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).times(WordArray([2, 3])), WordArray([4, 9]))

    def test_times_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).times(FloatArray([2, 3])), FloatArray([4, 9]))

    def test_times_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).times(MixedArray([Word(2), Float(3)])), MixedArray([Word(4), Float(9)]))

    def test_times_real_array_word(self):
        assert_equal(FloatArray([2, 3]).times(Word(1)), FloatArray([2, 3]))

    def test_times_real_array_real(self):
        assert_equal(FloatArray([2, 3]).times(Float(1)), FloatArray([2, 3]))

    def test_times_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).times(WordArray([2, 3])), FloatArray([4, 9]))

    def test_times_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).times(FloatArray([2, 3])), FloatArray([4, 9]))

    def test_times_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).times(MixedArray([Word(2), Float(3)])), MixedArray([Float(4), Float(9)]))

    def test_times_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).times(Word(2)), MixedArray([Word(4), Float(6)]))

    def test_times_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).times(Float(2)), MixedArray([Float(4), Float(6)]))

    def test_times_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).times(WordArray([2, 3])), MixedArray([Word(4), Float(9)]))

    def test_times_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).times(FloatArray([2, 3])), MixedArray([Float(4), Float(9)]))

    def test_times_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).times(MixedArray([Word(2), Float(3)])), MixedArray([Word(4), Float(9)]))

class PowerTests(TestCase):
    def test_power_word_word(self):
        assert_equal(Word(2).power(Word(2)), Float(4))

    def test_power_word_real(self):
        assert_equal(Word(2).power(Float(2)), Float(4))

    def test_power_word_word_array(self):
        assert_equal(Word(2).power(WordArray([2, 3])), FloatArray([4, 8]))

    def test_power_word_real_array(self):
        assert_equal(Word(2).power(FloatArray([2, 3])), FloatArray([4, 8]))

    def test_power_word_mixed_array(self):
        assert_equal(Word(2).power(MixedArray([Word(2), Float(3)])), MixedArray([Float(4), Float(8)]))

    def test_power_real_word(self):
        assert_equal(Float(2).power(Word(2)), Float(4))

    def test_power_real_real(self):
        assert_equal(Float(2).power(Float(2)), Float(4))

    def test_power_real_word_array(self):
        assert_equal(Float(2).power(WordArray([2, 3])), FloatArray([4, 8]))

    def test_power_real_real_array(self):
        assert_equal(Float(2).power(FloatArray([2, 3])), FloatArray([4, 8]))

    def test_power_real_mixed_array(self):
        assert_equal(Float(2).power(MixedArray([Word(2), Float(3)])), MixedArray([Float(4), Float(8)]))

    def test_power_word_array_word(self):
        assert_equal(WordArray([2, 3]).power(Word(3)), FloatArray([8, 27]))

    def test_power_word_array_real(self):
        assert_equal(WordArray([2, 3]).power(Float(1)), FloatArray([2, 3]))

    def test_power_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).power(WordArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).power(MixedArray([Word(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

    def test_power_real_array_word(self):
        assert_equal(FloatArray([2, 3]).power(Word(3)), FloatArray([8, 27]))

    def test_power_real_array_real(self):
        assert_equal(FloatArray([2, 3]).power(Float(1)), FloatArray([2, 3]))

    def test_power_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).power(WordArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).power(MixedArray([Word(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

    def test_power_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).power(Word(2)), MixedArray([Float(4), Float(9)]))

    def test_power_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).power(Float(2)), MixedArray([Float(4), Float(9)]))

    def test_power_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).power(WordArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).power(MixedArray([Word(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

class DivideTests(TestCase):
    def test_divide_errors(self):
        assert_equal(Word(0).divide(Error.test_error()).o, NounType.ERROR)
        assert_equal(Float(0).divide(Error.test_error()).o, NounType.ERROR)
        assert_equal(WordArray([0]).divide(Error.test_error()).o, NounType.ERROR)
        assert_equal(FloatArray([0]).divide(Error.test_error()).o, NounType.ERROR)
        assert_equal(MixedArray([Word(0)]).divide(Error.test_error()).o, NounType.ERROR)

    def test_divide_word_word(self):
        assert_equal(Word(1).divide(Word(2)), Float(1.0 / 2.0))
        assert_equal(Word(1).divide(Word(0)).o, NounType.ERROR)

    def test_divide_word_real(self):
        assert_equal(Word(1).divide(Float(2)), Float(0.5))
        assert_equal(Word(1).divide(Float(0)).o, NounType.ERROR)

    def test_divide_word_word_array(self):
        assert_equal(Word(1).divide(WordArray([2, 3])), FloatArray([1.0 / 2.0, 1.0 / 3.0]))
        assert_equal(Word(1).divide(WordArray([0, 3])).o, NounType.ERROR)

    def test_divide_word_real_array(self):
        assert_equal(Word(1).divide(FloatArray([2, 3])), FloatArray([1.0 / 2.0, 1.0 / 3.0]))
        assert_equal(Word(1).divide(FloatArray([0, 3])).o, NounType.ERROR)

    def test_divide_word_mixed_array(self):
        assert_equal(Word(1).divide(MixedArray([Word(2), Float(3)])), MixedArray([Float(1.0 / 2.0), Float(1.0 / 3.0)]))
        assert_equal(Word(1).divide(MixedArray([Word(0), Float(3)])).o, NounType.ERROR)

    def test_divide_real_word(self):
        assert_equal(Float(1).divide(Word(-1)), Float(-1))
        assert_equal(Float(1).divide(Word(0)).o, NounType.ERROR)

    def test_divide_real_real(self):
        assert_equal(Float(1).divide(Float(2)), Float(0.5))
        assert_equal(Float(1).divide(Float(0)).o, NounType.ERROR)

    def test_divide_real_word_array(self):
        assert_equal(Float(1).divide(WordArray([2, 3])), FloatArray([1.0 / 2.0, 1.0 / 3.0]))

    def test_divide_real_real_array(self):
        assert_equal(Float(1).divide(FloatArray([2, 3])), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_divide_real_mixed_array(self):
        assert_equal(Float(1).divide(MixedArray([Word(2), Float(3)])), MixedArray([Float(1.0 / 2.0), Float(1.0 / 3.0)]))

    def test_divide_word_array_word(self):
        assert_equal(WordArray([2, 3]).divide(Word(1)), WordArray([2, 3]))

    def test_divide_word_array_real(self):
        assert_equal(WordArray([2, 3]).divide(Float(1)), FloatArray([2, 3]))

    def test_divide_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).divide(WordArray([2, 3])), FloatArray([1, 1]))

    def test_divide_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).divide(FloatArray([2, 3])), FloatArray([1, 1]))

    def test_divide_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).divide(MixedArray([Word(2), Float(3)])), MixedArray([Float(1), Float(1)]))

    def test_divide_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).divide(Word(2)), MixedArray([Float(1), Float(3.0 / 2.0)]))

    def test_divide_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).divide(Float(2)), MixedArray([Float(1), Float(3.0 / 2.0)]))

    def test_divide_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).divide(WordArray([2, 3])), MixedArray([Float(1), Float(1)]))

    def test_divide_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).divide(FloatArray([2, 3])), MixedArray([Float(1), Float(1)]))

    def test_divide_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).divide(MixedArray([Word(2), Float(3)])), MixedArray([Float(1), Float(1)]))

class NegateTests(TestCase):
    def test_negate_word(self):
        assert_equal(Word(1).negate(), Word(-1))

    def test_negate_real(self):
        assert_equal(Float(1).negate(), Float(-1))

    def test_negate_word_array(self):
        assert_equal(WordArray([2, 3]).negate(), WordArray([-2, -3]))

    def test_negate_real_array(self):
        assert_equal(FloatArray([2, 3]).negate(), FloatArray([-2, -3]))

    def test_negate_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).negate(), MixedArray([Word(-2), Float(-3)]))


class ReciprocalTests(TestCase):
    def test_reciprocal_word(self):
        assert_equal(Word(2).reciprocal(), Float(1.0 / 2.0))

    def test_reciprocal_real(self):
        assert_equal(Float(2).reciprocal(), Float(1.0/2.0))

    def test_reciprocal_word_array(self):
        assert_equal(WordArray([2, 3]).reciprocal(), FloatArray([1.0 / 2.0, 1.0 / 3.0]))

    def test_reciprocal_real_array(self):
        assert_equal(FloatArray([2, 3]).reciprocal(), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_reciprocal_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).reciprocal(), MixedArray([Float(1.0 / 2.0), Float(1.0 / 3.0)]))

class EnumerateTests(TestCase):
    def test_enumerate(self):
        assert_equal(Word(5).enumerate(), WordArray([1, 2, 3, 4, 5]))

class ComplementationTests(TestCase):
    def test_complementation_word(self):
        assert_equal(Word(5).complementation(), Word(-4))

    def test_complementation_real(self):
        assert_equal(Float(5).complementation(), Float(-4))

    def test_complementation_word_array(self):
        assert_equal(WordArray([0, 1, 2]).complementation(), WordArray([1, 0, -1]))

    def test_complementation_real_array(self):
        assert_equal(FloatArray([0, 1, 2]).complementation(), FloatArray([1, 0, -1]))

    def test_complementation_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(2)]).complementation(), MixedArray([Word(1), Float(0), Word(-1)]))

class FloorTests(TestCase):
    def test_floor_word(self):
        assert_equal(Word(5).floor(), Word(5))

    def test_floor_real(self):
        assert_equal(Float(5.5).floor(), Word(5))

    def test_floor_word_array(self):
        assert_equal(WordArray([0, 1, 2]).floor(), WordArray([0, 1, 2]))

    def test_floor_real_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).floor(), WordArray([0, 1, 2]))

    def test_floor_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(2)]).floor(), MixedArray([Word(0), Word(1), Word(2)]))

# class CountTests(TestCase):
#     def test_size_word(self):
#         assert_equal(Word(5).size(), Word(5))
#         assert_equal(Word(-5).size(), Word(5))
#
#     def test_size_real(self):
#         assert_equal(Float(5.5).size(), Float(5.5))
#         assert_equal(Float(-5.5).size(), Float(5.5))
#
#     def test_size_word_array(self):
#         assert_equal(WordArray([0, 1, 2]).size(), Word(3))
#
#     def test_size_real_array(self):
#         assert_equal(FloatArray([0.1, 1.5, 2.9]).size(), Word(3))
#
#     def test_size_mixed_array(self):
#         assert_equal(MixedArray([Word(0), Float(1), Word(2)]).size(), Word(3))

class ReverseTests(TestCase):
    def test_reverse_word_array(self):
        assert_equal(WordArray([0, 1, 2]).reverse(), WordArray([2, 1, 0]))

    def test_reverse_real_array(self):
        assert_equal(FloatArray([0, 1, 2]).reverse(), FloatArray([2, 1, 0]))

    def test_reverse_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(2)]).reverse(), MixedArray([Word(2), Float(1), Word(0)]))

class FirstTests(TestCase):
    def test_first_word_array(self):
        assert_equal(WordArray([0, 1, 2]).first(), Word(0))

    def test_first_real_array(self):
        assert_equal(FloatArray([0, 1, 2]).first(), Float(0))

    def test_first_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(2)]).first(), Word(0))

class ShapeTests(TestCase):
    def test_shape_word(self):
        assert_equal(Word(5).shape(), Word(0))

    def test_shape_real(self):
        assert_equal(Float(5.5).shape(), Word(0))

    def test_shape_word_array(self):
        assert_equal(WordArray([0, 1, 2]).shape(), WordArray([3]))

    def test_shape_real_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).shape(), WordArray([3]))

    def test_shape_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).shape(), WordArray([3]))
        assert_equal(MixedArray([WordArray([0]), FloatArray([1]), MixedArray([Word(0)])]).shape(), WordArray([3, 1]))

class RankTests(TestCase):
    def test_shape_word(self):
        assert_equal(Word(5).shape().size(), Word(0))

    def test_shape_real(self):
        assert_equal(Float(5.5).shape().size(), Word(0))

    def test_shape_word_array(self):
        assert_equal(WordArray([0, 1, 2]).shape().size(), Word(1))

    def test_shape_real_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).shape().size(), Word(1))

    def test_shape_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).shape().size(), Word(1))
        assert_equal(MixedArray([WordArray([0]), FloatArray([1]), MixedArray([Word(0)])]).shape().size(), Word(2))

class EncloseTests(TestCase):
    def test_enclose_word(self):
        assert_equal(Word(5).enclose(), WordArray([5]))

    def test_enclose_real(self):
        assert_equal(Float(5.5).enclose(), FloatArray([5.5]))

    def test_enclose_word_array(self):
        assert_equal(WordArray([0, 1, 2]).enclose(), MixedArray([WordArray([0, 1, 2])]))

    def test_enclose_real_array(self):
        assert_equal(FloatArray([0, 1, 2]).enclose(), MixedArray([FloatArray([0, 1, 2])]))

    def test_enclose_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).enclose(), MixedArray([MixedArray([Word(0), Float(1), WordArray([1, 2, 3])])]))

class UniqueTests(TestCase):
    def test_unique_word_array(self):
        assert_equal(WordArray([0, 1, 0, 2]).unique(), WordArray([0, 1, 2]))

    def test_unique_real_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).unique(), FloatArray([0, 1, 2]))

    def test_unique_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).unique(), MixedArray([Word(0), Float(1), Float(2)]))

class TakeTests(TestCase):
    def test_take_word_array(self):
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(2)), WordArray([0, 1]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(-2)), WordArray([0, 2]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(0)), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(9)), WordArray([0, 1, 0, 2, 0, 1, 0, 2, 0]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(6)), WordArray([0, 1, 0, 2, 0, 1]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Word(-6)), WordArray([0, 2, 0, 1, 0, 2]))
        assert_equal(WordArray([]).take(Word(1)).o, NounType.ERROR)

        assert_equal(WordArray([0, 1, 0, 2]).take(Float(0.0)), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Float(0.5)), WordArray([0, 1]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Float(1.0)), WordArray([0, 1, 0, 2]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Float(2.0)), WordArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(WordArray([0, 1, 0, 2]).take(Float(-2.0)), WordArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(WordArray([]).take(Float(0.5)), WordArray([]))
        assert_equal(WordArray([]).take(Float(1)), WordArray([]))

        assert_equal(WordArray([0, 1, 0, 2]).take(WordArray([])), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).take(WordArray([1])), MixedArray([WordArray([0])]))
        assert_equal(WordArray([0, 1, 0, 2]).take(WordArray([1, 2])), MixedArray([WordArray([0]), WordArray([0, 1])]))
        assert_equal(WordArray([]).take(WordArray([1, 2])), WordArray([]))

        assert_equal(WordArray([0, 1, 0, 2]).take(FloatArray([])), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).take(FloatArray([0.25])), MixedArray([WordArray([0])]))
        assert_equal(WordArray([0, 1, 0, 2]).take(FloatArray([0.25, 0.5])), MixedArray([WordArray([0]), WordArray([0, 1])]))
        assert_equal(WordArray([]).take(FloatArray([1, 2])), WordArray([]))

        assert_equal(WordArray([0, 1, 0, 2]).take(MixedArray([])), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).take(MixedArray([Word(1)])), MixedArray([WordArray([0])]))
        assert_equal(WordArray([0, 1, 0, 2]).take(MixedArray([Word(1), Float(0.5)])), MixedArray([WordArray([0]), WordArray([0, 1])]))
        assert_equal(WordArray([]).take(MixedArray([Float(1), Float(2)])), WordArray([]))
        assert_equal(WordArray([]).take(MixedArray([Word(1), Float(2)])), WordArray([]))

    def test_take_real_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(2)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(-2)), FloatArray([0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(0)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(9)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2, 0]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(6)), FloatArray([0, 1, 0, 2, 0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Word(-6)), FloatArray([0, 2, 0, 1, 0, 2]))
        assert_equal(FloatArray([]).take(Word(1)).o, NounType.ERROR)

        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(0.0)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(0.5)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(1.0)), FloatArray([0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(2.0)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(-2.0)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(FloatArray([]).take(Float(0.5)), FloatArray([]))
        assert_equal(FloatArray([]).take(Float(1)), FloatArray([]))

        assert_equal(FloatArray([0, 1, 0, 2]).take(WordArray([])), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(WordArray([1])), MixedArray([FloatArray([0])]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(WordArray([1, 2])), MixedArray([FloatArray([0]), FloatArray([0, 1])]))
        assert_equal(FloatArray([]).take(WordArray([1, 2])), FloatArray([]))

        assert_equal(FloatArray([0, 1, 0, 2]).take(FloatArray([])), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(FloatArray([0.25])), MixedArray([FloatArray([0])]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(FloatArray([0.25, 0.5])), MixedArray([FloatArray([0]), FloatArray([0, 1])]))
        assert_equal(FloatArray([]).take(FloatArray([0.25, 0.5])), FloatArray([]))

        assert_equal(FloatArray([0, 1, 0, 2]).take(MixedArray([])), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(MixedArray([Float(0.25)])), MixedArray([FloatArray([0])]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(MixedArray([Float(0.25), Float(0.5)])), MixedArray([FloatArray([0]), FloatArray([0, 1])]))
        assert_equal(FloatArray([]).take(MixedArray([Float(0.25), Float(0.5)])), FloatArray([]))

        assert_equal(FloatArray([]).take(MixedArray([Word(1), Float(2)])), FloatArray([]))

    def test_take_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Word(2)), MixedArray([Word(0), Float(1)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Word(-2)), MixedArray([Word(0), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Word(0)), MixedArray([]))
        assert_equal(MixedArray([Float(0), Float(1), Float(0), Float(2)]).take(Word(9)), MixedArray([Float(0), Float(1), Float(0), Float(2), Float(0), Float(1), Float(0), Float(2), Float(0)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Word(6)), MixedArray([Word(0), Float(1), Word(0), Float(2), Word(0), Float(1)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Word(-6)), MixedArray([Word(0), Float(2), Word(0), Float(1), Word(0), Float(2)]))
        assert_equal(MixedArray([]).take(Word(1)), MixedArray([]))

        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Float(0.0)), MixedArray([]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Float(0.5)), MixedArray([Word(0), Float(1)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Float(1.0)), MixedArray([Word(0), Float(1), Word(0), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Float(2.0)), MixedArray([Word(0), Float(1), Word(0), Float(2), Word(0), Float(1), Word(0), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(Float(-2.0)), MixedArray([Word(0), Float(1), Word(0), Float(2), Word(0), Float(1), Word(0), Float(2)]))
        assert_equal(MixedArray([]).take(Float(0.5)), MixedArray([]))
        assert_equal(MixedArray([]).take(Float(1)), MixedArray([]))

        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(WordArray([])), MixedArray([]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(WordArray([1])), MixedArray([MixedArray([Word(0)])]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).take(WordArray([1, 2])), MixedArray([MixedArray([Word(0)]), MixedArray([Word(0), Float(1)])]))
        assert_equal(MixedArray([]).take(WordArray([1, 2])), MixedArray([]))
        assert_equal(MixedArray([]).take(MixedArray([Word(1), Float(2)])), MixedArray([]))

class DropTests(TestCase):
    def test_drop_word_array(self):
        assert_equal(WordArray([0, 1, 0, 2]).drop(Word(2)), WordArray([0, 2]))
        assert_equal(WordArray([0, 1, 0, 2]).drop(Word(-2)), WordArray([0, 1]))
        assert_equal(WordArray([0, 1, 0, 2]).drop(Word(0)), WordArray([0, 1, 0, 2]))
        assert_equal(WordArray([0, 1, 0, 2]).drop(Word(100)), WordArray([]))
        assert_equal(WordArray([]).drop(Word(100)), WordArray([]))
        assert_equal(WordArray([0, 1, 0, 2]).drop(Word(-100)), WordArray([]))
        assert_equal(WordArray([]).drop(Word(-100)), WordArray([]))

    def test_drop_real_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Word(2)), FloatArray([0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Word(-2)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Word(0)), FloatArray([0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Word(100)), FloatArray([]))
        assert_equal(FloatArray([]).drop(Word(100)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Word(-100)), FloatArray([]))
        assert_equal(FloatArray([]).drop(Word(-100)), FloatArray([]))

    def test_drop_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).drop(Word(2)), MixedArray([Word(0), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).drop(Word(-2)), MixedArray([Word(0), Float(1)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).drop(Word(0)), MixedArray([Word(0), Float(1), Word(0), Float(2)]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).drop(Word(100)), MixedArray([]))
        assert_equal(MixedArray([]).drop(Word(100)), MixedArray([]))
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).drop(Word(-100)), MixedArray([]))
        assert_equal(MixedArray([]).drop(Word(-100)), MixedArray([]))

    def test_drop_errors(self):
        assert_equal(Word(1).drop(Word(-1)).o, NounType.ERROR)
        assert_equal(Word(1).drop(Float(-1)).o, NounType.ERROR)

        assert_equal(Float(1).drop(Word(-1)).o, NounType.ERROR)
        assert_equal(Float(1).drop(Float(-1)).o, NounType.ERROR)

        assert_equal(WordArray([1, 2, 3]).drop(Float(-1)).o, NounType.ERROR)

        assert_equal(FloatArray([1, 2, 3]).drop(Float(-1)).o, NounType.ERROR)

        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).drop(Float(-1)).o, NounType.ERROR)

class JoinTests(TestCase):
    def test_join_word_word(self):
        assert_equal(Word(1).join(Word(2)), WordArray([1, 2]))

    def test_join_word_real(self):
        assert_equal(Word(1).join(Float(2)), MixedArray([Word(1), Float(2)]))

    def test_join_word_word_array(self):
        assert_equal(Word(1).join(WordArray([2, 3])), WordArray([1, 2, 3]))

    def test_join_word_real_array(self):
        assert_equal(Word(1).join(FloatArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_word_mixed_array(self):
        assert_equal(Word(1).join(MixedArray([Word(2), Float(3)])), MixedArray([Word(1), Word(2), Float(3)]))

    def test_join_real_word(self):
        assert_equal(Float(1).join(Word(-1)), MixedArray([Float(1), Word(-1)]))

    def test_join_real_real(self):
        assert_equal(Float(1).join(Float(2)), FloatArray([1, 2]))

    def test_join_real_word_array(self):
        assert_equal(Float(1).join(WordArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_real_real_array(self):
        assert_equal(Float(1).join(FloatArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_real_mixed_array(self):
        assert_equal(Float(1).join(MixedArray([Word(2), Float(3)])), MixedArray([Float(1), Word(2), Float(3)]))

    def test_join_word_array_word(self):
        assert_equal(WordArray([2, 3]).join(Word(1)), WordArray([2, 3, 1]))

    def test_join_word_array_real(self):
        assert_equal(WordArray([2, 3]).join(Float(1)), FloatArray([2, 3, 1]))

    def test_join_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).join(WordArray([2, 3])), WordArray([2, 3, 2, 3]))

    def test_join_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).join(FloatArray([2, 3])), FloatArray([2, 3, 2, 3]))

    def test_join_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).join(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Word(3), Word(2), Float(3)]))

    def test_join_real_array_word(self):
        assert_equal(FloatArray([2, 3]).join(Word(1)), FloatArray([2, 3, 1]))

    def test_join_real_array_real(self):
        assert_equal(FloatArray([2, 3]).join(Float(1)), FloatArray([2, 3, 1]))

    def test_join_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).join(WordArray([2, 3])), FloatArray([2, 3, 2, 3]))

    def test_join_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).join(FloatArray([2, 3])), FloatArray([2, 3, 2, 3]))

    def test_join_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).join(MixedArray([Word(2), Float(3)])), MixedArray([Float(2), Float(3), Word(2), Float(3)]))

    def test_join_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).join(Word(2)), MixedArray([Word(2), Float(3), Word(2)]))

    def test_join_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).join(Float(2)), MixedArray([Word(2), Float(3), Float(2)]))

    def test_join_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).join(WordArray([2, 3])), MixedArray([Word(2), Float(3), Word(2), Word(3)]))

    def test_join_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).join(FloatArray([2, 3])), MixedArray([Word(2), Float(3), Float(2), Float(3)]))

    def test_join_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).join(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(3), Word(2), Float(3)]))

class RotateTests(TestCase):
    def test_rotate_word_word_array(self):
        assert_equal(Word(1).rotate(WordArray([0, 1, 2])), WordArray([1, 2, 0]))
        assert_equal(Word(-1).rotate(WordArray([0, 1, 2])), WordArray([2, 0, 1]))
        assert_equal(Word(1).rotate(WordArray([])), WordArray([]))
        assert_equal(Word(0).rotate(WordArray([0, 1, 2])), WordArray([0, 1, 2]))

        assert_equal(Word(1).rotate(FloatArray([0, 1, 2])), FloatArray([1, 2, 0]))
        assert_equal(Word(-1).rotate(FloatArray([0, 1, 2])), FloatArray([2, 0, 1]))
        assert_equal(Word(1).rotate(FloatArray([])), FloatArray([]))
        assert_equal(Word(0).rotate(FloatArray([0, 1, 2])), FloatArray([0, 1, 2]))

        assert_equal(Word(1).rotate(MixedArray([Word(0), Float(1), Word(2)])), MixedArray([Float(1), Word(2), Word(0)]))
        assert_equal(Word(-1).rotate(MixedArray([Word(0), Float(1), Word(2)])), MixedArray([Word(2), Word(0), Float(1)]))
        assert_equal(Word(1).rotate(MixedArray([])), MixedArray([]))
        assert_equal(Word(0).rotate(MixedArray([Word(0), Float(1), Word(2)])), MixedArray([Word(0), Float(1), Word(2)]))

        assert_equal(Word(1).rotate(Word(1)).o, NounType.ERROR)

    def test_rotate_word_array(self):
        assert_equal(WordArray([0, 1, 2]).rotate(Word(1)), WordArray([1, 2, 0]))
        assert_equal(WordArray([0, 1, 2]).rotate(Word(4)), WordArray([1, 2, 0]))
        assert_equal(WordArray([0, 1, 2]).rotate(Word(-1)), WordArray([2, 0, 1]))
        assert_equal(WordArray([0, 1, 2]).rotate(Word(-4)), WordArray([2, 0, 1]))
        assert_equal(WordArray([]).rotate(Word(1)), WordArray([]))
        assert_equal(WordArray([0, 1, 2]).rotate(Word(0)), WordArray([0, 1, 2]))

    def test_rotate_real_array(self):
        assert_equal(FloatArray([0, 1, 2]).rotate(Word(1)), FloatArray([1, 2, 0]))
        assert_equal(FloatArray([0, 1, 2]).rotate(Word(4)), FloatArray([1, 2, 0]))
        assert_equal(FloatArray([0, 1, 2]).rotate(Word(-1)), FloatArray([2, 0, 1]))
        assert_equal(FloatArray([0, 1, 2]).rotate(Word(-4)), FloatArray([2, 0, 1]))
        assert_equal(FloatArray([]).rotate(Word(1)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 2]).rotate(Word(0)), FloatArray([0, 1, 2]))

    def test_rotate_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).rotate(Word(1)), MixedArray([Float(1), WordArray([1, 2, 3]), Word(0)]))
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).rotate(Word(4)), MixedArray([Float(1), WordArray([1, 2, 3]), Word(0)]))
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).rotate(Word(-1)), MixedArray([WordArray([1, 2, 3]), Word(0), Float(1)]))
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).rotate(Word(-4)), MixedArray([WordArray([1, 2, 3]), Word(0), Float(1)]))
        assert_equal(MixedArray([]).rotate(Word(1)), MixedArray([]))
        assert_equal(MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]).rotate(Word(0)), MixedArray([Word(0), Float(1), WordArray([1, 2, 3])]))

    def test_rotate_errors(self):
        assert_equal(Error.test_error().rotate(WordArray([1, 2, 3])).o, NounType.ERROR)
        assert_equal(Error.test_error().rotate(FloatArray([1, 2, 3])).o, NounType.ERROR)
        assert_equal(Error.test_error().rotate(MixedArray([Word(1), Float(2), Word(3)])).o, NounType.ERROR)

        assert_equal(WordArray([1, 2, 3]).rotate(Float(-1)).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).rotate(Float(-1)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), WordArray([3, 4, 5])]).rotate(Float(-1)).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).rotate(Error.test_error()).o, NounType.ERROR)

        assert_equal(WordArray([1, 2, 3]).rotate(WordArray([1])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).rotate(WordArray([1])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), WordArray([3, 4, 5])]).rotate(WordArray([1])).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).rotate(Error.test_error()).o, NounType.ERROR)

        assert_equal(WordArray([1, 2, 3]).rotate(FloatArray([1])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).rotate(FloatArray([1])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), WordArray([3, 4, 5])]).rotate(FloatArray([1])).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).rotate(Error.test_error()).o, NounType.ERROR)

        assert_equal(WordArray([1, 2, 3]).rotate(Error.test_error()).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).rotate(MixedArray([Word(1)])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), WordArray([3, 4, 5])]).rotate(MixedArray([Word(1)])).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).rotate(MixedArray([Word(1)])).o, NounType.ERROR)

class SplitTests(TestCase):
    def test_split_word_word_array(self):
        assert_equal(Word(1).split(WordArray([2, 3])), MixedArray([WordArray([2]), WordArray([3])]))

    def test_split_word_real_array(self):
        assert_equal(Word(1).split(FloatArray([2, 3])), MixedArray([FloatArray([2]), FloatArray([3])]))

    def test_split_word_mixed_array(self):
        assert_equal(Word(1).split(MixedArray([Word(2), Float(3)])), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)])]))

    def test_split_real_word_array(self):
        assert_equal(Float(0.5).split(WordArray([2, 3])), MixedArray([WordArray([2]), WordArray([3])]))

    def test_split_real_real_array(self):
        assert_equal(Float(0.5).split(FloatArray([2, 3])), MixedArray([FloatArray([2]), FloatArray([3])]))

    def test_split_real_mixed_array(self):
        assert_equal(Float(0.5).split(MixedArray([Word(2), Float(3)])), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)])]))

    def test_split_word_array_word(self):
        assert_equal(WordArray([2, 3]).split(Word(1)), MixedArray([WordArray([2]), WordArray([3])]))

    def test_split_word_array_real(self):
        assert_equal(WordArray([2, 3]).split(Float(0.5)), MixedArray([WordArray([2]), WordArray([3])]))
        assert_equal(WordArray([1]).split(Float(0)), WordArray([]))

    def test_split_word_array_word_array(self):
        assert_equal(WordArray([2, 3, 4]).split(WordArray([1, 1])), MixedArray([WordArray([2]), WordArray([3]), WordArray([4])]))
        assert_equal(WordArray([2, 3, 4]).split(WordArray([])), MixedArray([WordArray([2, 3, 4])]))

    def test_split_word_array_real_array(self):
        assert_equal(WordArray([2, 3, 4]).split(FloatArray([0.5, 0.5])), MixedArray([WordArray([2]), WordArray([3]), WordArray([4])]))
        assert_equal(WordArray([2, 3, 4]).split(FloatArray([])), MixedArray([WordArray([2, 3, 4])]))

    def test_split_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3, 4]).split(MixedArray([Word(1), Float(0.5)])), MixedArray([WordArray([2]), WordArray([3]), WordArray([4])]))
        assert_equal(WordArray([2, 3, 4]).split(MixedArray([])), MixedArray([WordArray([2, 3, 4])]))

    def test_split_real_array_word(self):
        assert_equal(FloatArray([2, 3]).split(Word(1)), MixedArray([FloatArray([2]), FloatArray([3])]))

    def test_split_real_array_real(self):
        assert_equal(FloatArray([2, 3]).split(Float(0.5)), MixedArray([FloatArray([2]), FloatArray([3])]))
        assert_equal(FloatArray([2, 3]).split(Float(0)), FloatArray([]))
        assert_equal(FloatArray([1]).split(Float(0)), FloatArray([]))

    def test_split_real_array_word_array(self):
        assert_equal(FloatArray([2, 3, 4]).split(WordArray([1, 1])), MixedArray([FloatArray([2]), FloatArray([3]), FloatArray([4])]))
        assert_equal(FloatArray([2, 3, 4]).split(WordArray([])), MixedArray([FloatArray([2, 3, 4])]))

    def test_split_real_array_real_array(self):
        assert_equal(FloatArray([2, 3, 4]).split(FloatArray([0.5, 0.5])),  MixedArray([FloatArray([2]), FloatArray([3]), FloatArray([4])]))
        assert_equal(FloatArray([2, 3, 4]).split(FloatArray([])),  FloatArray([]))

    def test_split_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3, 4]).split(MixedArray([Word(1), Float(0.5)])), MixedArray([FloatArray([2]), FloatArray([3]), FloatArray([4])]))
        assert_equal(FloatArray([2, 3, 4]).split(MixedArray([])),  FloatArray([]))

    def test_split_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3), Word(2)]).split(Word(1)), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3), Word(2)])]))

    def test_split_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).split(Float(0.5)), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)])]))
        assert_equal(MixedArray([Word(1)]).split(Float(0)), MixedArray([]))

    def test_split_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(WordArray([1, 1])), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)]), MixedArray([Word(1)])]))
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(WordArray([])), MixedArray([MixedArray([Word(2), Float(3), Word(1)])]))

    def test_split_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(FloatArray([0.5, 0.5])), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)]), MixedArray([Word(1)])]))
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(FloatArray([])), MixedArray([MixedArray([Word(2), Float(3), Word(1)])]))

    def test_split_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(MixedArray([Word(1), Float(0.5)])), MixedArray([MixedArray([Word(2)]), MixedArray([Float(3)]), MixedArray([Word(1)])]))
        assert_equal(MixedArray([Word(2), Float(3), Word(1)]).split(MixedArray([])), MixedArray([MixedArray([Word(2), Float(3), Word(1)])]))

    def test_split_errors(self):
        assert_equal(Word(1).split(Word(4)).o, NounType.ERROR)
        assert_equal(Word(1).split(Float(4)).o, NounType.ERROR)

        assert_equal(Float(1).split(Word(4)).o, NounType.ERROR)
        assert_equal(Float(1).split(Float(4)).o, NounType.ERROR)

        assert_equal(WordArray([]).split(Word(4)).o, NounType.ERROR)
        assert_equal(WordArray([1]).split(Word(0)).o, NounType.ERROR)
        assert_equal(WordArray([1]).split(Word(-1)).o, NounType.ERROR)
        assert_equal(WordArray([1]).split(Word(4)).o, NounType.ERROR)
        assert_equal(WordArray([1]).split(Float(-1)).o, NounType.ERROR)
        assert_equal(WordArray([1]).split(Float(2)).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).split(WordArray([1, 5])).o, NounType.ERROR)
        assert_equal(WordArray([1, 2]).split(WordArray([1, 1, 1])).o, NounType.ERROR)

        assert_equal(FloatArray([]).split(Word(4)).o, NounType.ERROR)
        assert_equal(FloatArray([1]).split(Word(0)).o, NounType.ERROR)
        assert_equal(FloatArray([1]).split(Word(-1)).o, NounType.ERROR)
        assert_equal(FloatArray([1]).split(Word(4)).o, NounType.ERROR)
        assert_equal(FloatArray([1]).split(Float(-1)).o, NounType.ERROR)
        assert_equal(FloatArray([1]).split(Float(2)).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).split(WordArray([1, 5])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2]).split(WordArray([1, 1, 1])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).split(FloatArray([1, 5])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2]).split(FloatArray([1, 1, 1])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).split(MixedArray([Word(1), Word(5)])).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2]).split(MixedArray([Word(1), Word(1), Word(1)])).o, NounType.ERROR)

        assert_equal(MixedArray([]).split(Word(4)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1)]).split(Word(0)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1)]).split(Word(-1)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1)]).split(Word(4)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1)]).split(Float(-1)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1)]).split(Float(2)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).split(WordArray([1, 5])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2)]).split(WordArray([1, 1, 1])).o, NounType.ERROR)

class FindTests(TestCase):
    def test_find_word_word(self):
        assert_equal(Word(2).find(Word(1)).o, NounType.ERROR)

    def test_find_word_real(self):
        assert_equal(Float(2).find(Word(1)).o, NounType.ERROR)

    def test_find_word_word_array(self):
        assert_equal(Word(2).find(WordArray([1, 2, 3])), WordArray([0, 1, 0]))

    def test_find_word_real_array(self):
        assert_equal(Word(2).find(FloatArray([1, 2, 3])), WordArray([0, 1, 0]))

    def test_find_word_mixed_array(self):
        assert_equal(Word(2).find(MixedArray([Word(1), Word(2), Float(3)])), WordArray([0, 1, 0]))

    def test_find_real_word_array(self):
        assert_equal(Float(2).find(WordArray([1, 2, 3])), WordArray([0, 1, 0]))

    def test_find_real_real_array(self):
        assert_equal(Float(2).find(FloatArray([1, 2, 3])), WordArray([0, 1, 0]))

    def test_find_real_mixed_array(self):
        assert_equal(Float(3).find(MixedArray([Word(1), Word(2), Float(3)])), WordArray([0, 0, 1]))

    def test_find_word_array_word(self):
        assert_equal(WordArray([1, 2, 3]).find(Word(2)), WordArray([0, 1, 0]))

    def test_find_word_array_real(self):
        assert_equal(WordArray([1, 2, 3]).find(Float(2)), WordArray([0, 1, 0]))

    def test_find_word_array_word_array(self):
        assert_equal(WordArray([1, 2, 3]).find(WordArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_word_array_real_array(self):
        assert_equal(WordArray([1, 2, 3]).find(FloatArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_word_array_mixed_array(self):
        assert_equal(WordArray([1, 2, 3]).find(MixedArray([Word(2), Word(3)])), WordArray([0, 1, 0]))

    def test_find_real_array_word(self):
        assert_equal(FloatArray([1, 2, 3]).find(Word(2)), WordArray([0, 1, 0]))

    def test_find_real_array_real(self):
        assert_equal(FloatArray([1, 2, 3]).find(Float(2)), WordArray([0, 1, 0]))

    def test_find_real_array_word_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(WordArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_real_array_real_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(FloatArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_real_array_mixed_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(MixedArray([Float(2), Float(3)])), WordArray([0, 1, 0]))

    def test_find_mixed_array_word(self):
        assert_equal(MixedArray([Word(1), Word(2), Word(3)]).find(Word(2)), WordArray([0, 1, 0]))

    def test_find_mixed_array_real(self):
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).find(Float(2)), WordArray([0, 1, 0]))

    def test_find_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(1), Word(2), Word(3)]).find(WordArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_mixed_array_real_array(self):
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).find(FloatArray([2, 3])), WordArray([0, 1, 0]))

    def test_find_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(1), Word(2), Float(3)]).find(MixedArray([Word(2), Float(3)])), WordArray([0, 1, 0]))

class RemainderTests(TestCase):
    def test_remainder_word_word(self):
        assert_equal(Word(10).remainder(Word(2)), Word(0))

    def test_remainder_word_word_array(self):
        assert_equal(Word(10).remainder(WordArray([2, 3])), WordArray([0, 1]))

    def test_remainder_word_mixed_array(self):
        assert_equal(Word(10).remainder(MixedArray([Word(2), Word(3)])), MixedArray([Word(0), Word(1)]))

    def test_remainder_word_array_word(self):
        assert_equal(WordArray([10, 9]).remainder(Word(2)), WordArray([0, 1]))

    def test_remainder_word_array_word_array(self):
        assert_equal(WordArray([10, 9]).remainder(WordArray([2, 3])), MixedArray([WordArray([0, 1]), WordArray([1, 0])]))

    def test_remainder_word_array_mixed_array(self):
        assert_equal(WordArray([10, 9]).remainder(MixedArray([Word(2), Word(3)])), MixedArray([MixedArray([Word(0), Word(1)]), MixedArray([Word(1), Word(0)])]))

    def test_remainder_mixed_array_word(self):
        assert_equal(MixedArray([Word(10), Word(9)]).remainder(Word(2)), MixedArray([Word(0), Word(1)]))

    def test_remainder_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(10), Word(9)]).remainder(WordArray([2, 3])), MixedArray([WordArray([0, 1]), WordArray([1, 0])]))

    def test_remainder_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(10), Word(9)]).remainder(MixedArray([Word(2), Word(3)])), MixedArray([MixedArray([Word(0), Word(1)]), MixedArray([Word(1), Word(0)])]))

    def test_remainder_errors(self):
        assert_equal(Word(10).remainder(FloatArray([2, 3])).o, NounType.ERROR)
        assert_equal(Float(10).remainder(FloatArray([2, 3])).o, NounType.ERROR)
        assert_equal(WordArray([10]).remainder(FloatArray([2, 3])).o, NounType.ERROR)
        assert_equal(FloatArray([10]).remainder(FloatArray([2, 3])).o, NounType.ERROR)
        assert_equal(MixedArray(Word(10)).remainder(FloatArray([2, 3])).o, NounType.ERROR)

class MatchTests(TestCase):
    def test_match_word_word(self):
        assert_equal(Word(10).match(Word(10)), Word(1))

    def test_match_word_real(self):
        assert_equal(Word(10).match(Float(10)), Word(1))

    def test_match_word_word_array(self):
        assert_equal(Word(10).match(WordArray([2, 3])), Word(0))

    def test_match_word_real_array(self):
        assert_equal(Word(10).match(FloatArray([2, 3])), Word(0))

    def test_match_word_mixed_array(self):
        assert_equal(Word(10).match(MixedArray([Word(2), Word(3)])), Word(0))

    def test_match_real_word(self):
        assert_equal(Float(10).match(Word(10)), Word(1))

    def test_match_real_real(self):
        assert_equal(Float(10).match(Float(10)), Word(1))

    def test_match_real_word_array(self):
        assert_equal(Float(10).match(WordArray([2, 3])), Word(0))

    def test_match_real_real_array(self):
        assert_equal(Float(10).match(FloatArray([2, 3])), Word(0))

    def test_match_real_mixed_array(self):
        assert_equal(Float(10).match(MixedArray([Word(2), Word(3)])), Word(0))

    def test_match_word_array_word(self):
        assert_equal(WordArray([1, 2, 3]).match(Word(2)), Word(0))
        assert_equal(WordArray([]).match(WordArray([])), Word(1))
        assert_equal(WordArray([]).match(FloatArray([])), Word(1))
        assert_equal(WordArray([]).match(MixedArray([])), Word(1))
        assert_equal(WordArray([]).match(WordArray([1])), Word(0))
        assert_equal(WordArray([1]).match(WordArray([])), Word(0))
        assert_equal(WordArray([]).match(FloatArray([1])), Word(0))
        assert_equal(WordArray([1]).match(FloatArray([])), Word(0))
        assert_equal(WordArray([]).match(MixedArray([Word(1)])), Word(0))
        assert_equal(WordArray([1]).match(MixedArray([])), Word(0))

    def test_match_word_array_real(self):
        assert_equal(WordArray([2, 3]).match(Float(2)), Word(0))

    def test_match_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).match(WordArray([2, 3])), Word(1))

    def test_match_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).match(FloatArray([2, 3])), Word(1))

    def test_match_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).match(MixedArray([Word(2), Word(3)])), Word(1))

    def test_match_real_array_word(self):
        assert_equal(FloatArray([1, 2, 3]).match(Word(2)), Word(0))

    def test_match_real_array_real(self):
        assert_equal(FloatArray([1, 2, 3]).match(Float(2)), Word(0))

    def test_match_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).match(WordArray([2, 3])), Word(1))
        assert_equal(FloatArray([2, 3]).match(WordArray([4, 5])), Word(0))

    def test_match_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).match(FloatArray([2, 3])), Word(1))
        assert_equal(FloatArray([]).match(WordArray([])), Word(1))
        assert_equal(FloatArray([]).match(FloatArray([])), Word(1))
        assert_equal(FloatArray([]).match(MixedArray([])), Word(1))
        assert_equal(FloatArray([]).match(WordArray([1])), Word(0))
        assert_equal(FloatArray([1]).match(WordArray([])), Word(0))
        assert_equal(FloatArray([]).match(FloatArray([1])), Word(0))
        assert_equal(FloatArray([1]).match(FloatArray([])), Word(0))
        assert_equal(FloatArray([]).match(MixedArray([Word(1)])), Word(0))
        assert_equal(FloatArray([1]).match(MixedArray([])), Word(0))

    def test_match_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).match(MixedArray([Word(2), Word(3)])), Word(1))

    def test_match_mixed_array_word(self):
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).match(Word(2)), Word(0))

    def test_match_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).match(WordArray([1, 2, 3])), Word(1))

    def test_match_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).match(MixedArray([Float(1), Word(2), Float(3)])), Word(1))
        assert_equal(MixedArray([]).match(WordArray([])), Word(1))
        assert_equal(MixedArray([]).match(FloatArray([])), Word(1))
        assert_equal(MixedArray([]).match(MixedArray([])), Word(1))
        assert_equal(MixedArray([]).match(WordArray([1])), Word(0))
        assert_equal(MixedArray([1]).match(WordArray([])), Word(0))

class MaxTests(TestCase):
    def test_max_word_word(self):
        assert_equal(Word(1).max(Word(2)), Word(2))

    def test_max_word_real(self):
        assert_equal(Word(1).max(Float(2)), Float(2))

    def test_max_word_word_array(self):
        assert_equal(Word(1).max(WordArray([2, 3])), WordArray([2, 3]))

    def test_max_word_real_array(self):
        assert_equal(Word(1).max(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_max_word_mixed_array(self):
        assert_equal(Word(1).max(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(3)]))

    def test_max_real_word(self):
        assert_equal(Float(1).max(Word(-1)), Float(1))

    def test_max_real_real(self):
        assert_equal(Float(1).max(Float(2)), Float(2))

    def test_max_real_word_array(self):
        assert_equal(Float(1).max(WordArray([2, 3])), FloatArray([2, 3]))

    def test_max_real_real_array(self):
        assert_equal(Float(1).max(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_max_real_mixed_array(self):
        assert_equal(Float(1).max(MixedArray([Word(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_max_word_array_word(self):
        assert_equal(WordArray([2, 3]).max(Word(1)), WordArray([2, 3]))

    def test_max_word_array_real(self):
        assert_equal(WordArray([2, 3]).max(Float(1)), FloatArray([2, 3]))

    def test_max_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).max(WordArray([2, 3])), WordArray([3, 3]))

    def test_max_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).max(FloatArray([2, 3])), FloatArray([3, 3]))

    def test_max_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).max(MixedArray([Word(2), Float(3)])), MixedArray([Float(3), Float(3)]))

    def test_max_real_array_word(self):
        assert_equal(FloatArray([2, 3]).max(Word(1)), FloatArray([2, 3]))

    def test_max_real_array_real(self):
        assert_equal(FloatArray([2, 3]).max(Float(1)), FloatArray([2, 3]))

    def test_max_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).max(WordArray([2, 3])), FloatArray([3, 3]))

    def test_max_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).max(FloatArray([2, 3])), FloatArray([3, 3]))

    def test_max_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).max(MixedArray([Word(2), Float(3)])), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).max(Word(3)), MixedArray([Word(3), Float(3)]))

    def test_max_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).max(Float(3)), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).max(WordArray([2, 3])), MixedArray([Word(3), Float(3)]))

    def test_max_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).max(FloatArray([2, 3])), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).max(MixedArray([Word(2), Float(3)])), MixedArray([Float(3), Float(3)]))

class MinTests(TestCase):
    def test_min_word_word(self):
        assert_equal(Word(1).min(Word(2)), Word(1))
        assert_equal(Word(4).min(Word(1)), Word(1))

    def test_min_word_real(self):
        assert_equal(Word(1).min(Float(2)), Float(1))
        assert_equal(Word(2).min(Float(1)), Float(1))

    def test_min_word_word_array(self):
        assert_equal(Word(1).min(WordArray([2, 3])), WordArray([1, 1]))
        assert_equal(Word(4).min(WordArray([2, 3])), WordArray([2, 3]))

    def test_min_word_real_array(self):
        assert_equal(Word(1).min(FloatArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Word(4).min(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_min_word_mixed_array(self):
        assert_equal(Word(1).min(MixedArray([Word(2), Float(3)])), MixedArray([Word(1), Float(1)]))
        assert_equal(Word(4).min(MixedArray([Word(2), Float(3)])), MixedArray([Word(2), Float(3)]))

    def test_min_real_word(self):
        assert_equal(Float(1).min(Word(-1)), Float(-1))
        assert_equal(Float(1).min(Word(4)), Float(1))

    def test_min_real_real(self):
        assert_equal(Float(1).min(Float(2)), Float(1))
        assert_equal(Float(2).min(Float(1)), Float(1))

    def test_min_real_word_array(self):
        assert_equal(Float(1).min(WordArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Float(4).min(WordArray([2, 3])), FloatArray([2, 3]))

    def test_min_real_real_array(self):
        assert_equal(Float(1).min(FloatArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Float(4).min(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_min_real_mixed_array(self):
        assert_equal(Float(1).min(MixedArray([Word(2), Float(3)])), MixedArray([Float(1), Float(1)]))
        assert_equal(Float(4).min(MixedArray([Word(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_min_word_array_word(self):
        assert_equal(WordArray([2, 3]).min(Word(1)), WordArray([1, 1]))
        assert_equal(WordArray([2, 3]).min(Word(4)), WordArray([2, 3]))

    def test_min_word_array_real(self):
        assert_equal(WordArray([2, 3]).min(Float(1)), FloatArray([1, 1]))
        assert_equal(WordArray([2, 3]).min(Float(4)), FloatArray([2, 3]))

    def test_min_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).min(WordArray([1, 1])), WordArray([1, 1]))
        assert_equal(WordArray([2, 3]).min(WordArray([4, 4])), WordArray([2, 3]))
        assert_equal(WordArray([2, 3]).min(WordArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(WordArray([2, 3]).min(WordArray([])).o, NounType.ERROR)
        assert_equal(WordArray([]).min(WordArray([4, 4, 4])).o, NounType.ERROR)

    def test_min_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).min(FloatArray([1, 1])), FloatArray([1, 1]))
        assert_equal(WordArray([2, 3]).min(FloatArray([4, 4])), FloatArray([2, 3]))
        assert_equal(WordArray([2, 3]).min(FloatArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(WordArray([]).min(FloatArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(WordArray([2, 3]).min(FloatArray([])).o, NounType.ERROR)

    def test_min_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).min(MixedArray([Word(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(WordArray([2, 3]).min(MixedArray([Word(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_equal(WordArray([2, 3]).min(MixedArray([Word(4), Word(4), Word(4)])).o, NounType.ERROR)
        assert_equal(WordArray([2, 3]).min(MixedArray([])).o, NounType.ERROR)
        assert_equal(WordArray([]).min(MixedArray([Word(4), Word(4), Word(4)])).o, NounType.ERROR)

    def test_min_real_array_word(self):
        assert_equal(FloatArray([2, 3]).min(Word(1)), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(Word(4)), FloatArray([2, 3]))

    def test_min_real_array_real(self):
        assert_equal(FloatArray([2, 3]).min(Float(1)), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(Float(4)), FloatArray([2, 3]))

    def test_min_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).min(WordArray([1, 1])), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(WordArray([4, 4])), FloatArray([2, 3]))
        assert_equal(FloatArray([2, 3]).min(WordArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(FloatArray([2, 3]).min(WordArray([])).o, NounType.ERROR)
        assert_equal(WordArray([2, 3]).min(WordArray([])).o, NounType.ERROR)
        assert_equal(WordArray([]).min(WordArray([2, 3])).o, NounType.ERROR)

    def test_min_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).min(FloatArray([1, 1])), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(FloatArray([4, 4])), FloatArray([2, 3]))
        assert_equal(FloatArray([2, 3]).min(FloatArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(FloatArray([2, 3]).min(FloatArray([])).o, NounType.ERROR)
        assert_equal(FloatArray([]).min(FloatArray([2, 3])).o, NounType.ERROR)

    def test_min_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).min(MixedArray([Word(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(FloatArray([2, 3]).min(MixedArray([Word(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_equal(FloatArray([2, 3]).min(MixedArray([Word(4), Word(4), Word(4)])).o, NounType.ERROR)
        assert_equal(MixedArray([2, 3]).min(MixedArray([])).o, NounType.ERROR)
        assert_equal(MixedArray([]).min(MixedArray([2, 3])).o, NounType.ERROR)

    def test_min_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).min(Word(1)), MixedArray([Word(1), Float(1)]))
        assert_equal(MixedArray([Word(2), Float(3)]).min(Word(4)), MixedArray([Word(2), Float(3)]))

    def test_min_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).min(Float(1)), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Word(2), Float(3)]).min(Float(4)), MixedArray([Float(2), Float(3)]))

    def test_min_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).min(WordArray([1, 1])), MixedArray([Word(1), Float(1)]))
        assert_equal(MixedArray([Word(2), Float(3)]).min(WordArray([4, 4])), MixedArray([Word(2), Float(3)]))
        assert_equal(MixedArray([Word(2), Word(3)]).min(WordArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(2), Word(3)]).min(WordArray([])).o, NounType.ERROR)
        assert_equal(MixedArray([]).min(WordArray([4, 4, 4])).o, NounType.ERROR)

    def test_min_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).min(FloatArray([1, 1])), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Word(2), Float(3)]).min(FloatArray([4, 4])), MixedArray([Float(2), Float(3)]))
        assert_equal(MixedArray([Word(2), Word(3)]).min(FloatArray([4, 4, 4])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(2), Word(3)]).min(FloatArray([])).o, NounType.ERROR)
        assert_equal(MixedArray([]).min(FloatArray([4, 4, 4])).o, NounType.ERROR)

    def test_min_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).min(MixedArray([Word(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Word(2), Float(3)]).min(MixedArray([Word(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_equal(MixedArray([Word(2), Word(3)]).min(MixedArray([Word(4), Word(4), Word(4)])).o, NounType.ERROR)
        assert_equal(MixedArray([Word(2), Word(3)]).min(MixedArray([])).o, NounType.ERROR)
        assert_equal(MixedArray([]).min(MixedArray([Word(4), Word(4), Word(4)])).o, NounType.ERROR)

class LessTests(TestCase):
    def test_less_word_word(self):
        assert_equal(Word(1).less(Word(2)), Word(1))

    def test_less_word_real(self):
        assert_equal(Word(1).less(Float(2)), Word(1))

    def test_less_word_word_array(self):
        assert_equal(Word(1).less(WordArray([2, 3])), Word(1))

    def test_less_word_real_array(self):
        assert_equal(Word(1).less(FloatArray([2, 3])), Word(1))

    def test_less_word_mixed_array(self):
        assert_equal(Word(1).less(MixedArray([Word(2), Float(3)])), Word(1))

    def test_less_real_word(self):
        assert_equal(Float(1).less(Word(-1)), Word(0))

    def test_less_real_real(self):
        assert_equal(Float(1).less(Float(2)), Word(1))

    def test_less_real_word_array(self):
        assert_equal(Float(1).less(WordArray([2, 3])), Word(1))

    def test_less_real_real_array(self):
        assert_equal(Float(1).less(FloatArray([2, 3])), Word(1))
    def test_less_real_mixed_array(self):
        assert_equal(Float(1).less(MixedArray([Word(2), Float(3)])), Word(1))

    def test_less_word_array_word(self):
        assert_equal(WordArray([2, 3]).less(Word(1)), WordArray([0, 0]))

    def test_less_word_array_real(self):
        assert_equal(WordArray([2, 3]).less(Float(1)), WordArray([0, 0]))

    def test_less_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).less(WordArray([2, 3])), WordArray([0, 0]))

    def test_less_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).less(FloatArray([2, 3])), WordArray([0, 0]))

    def test_less_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).less(MixedArray([Word(2), Float(3)])), WordArray([0, 0]))

    def test_less_real_array_word(self):
        assert_equal(FloatArray([2, 3]).less(Word(1)), WordArray([0, 0]))

    def test_less_real_array_real(self):
        assert_equal(FloatArray([2, 3]).less(Float(1)), WordArray([0, 0]))

    def test_less_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).less(WordArray([2, 3])), WordArray([0, 0]))

    def test_less_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).less(FloatArray([2, 3])), WordArray([0, 0]))

    def test_less_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).less(MixedArray([Word(2), Float(3)])), WordArray([0, 0]))

    def test_less_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).less(Word(3)), WordArray([1, 0]))

    def test_less_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).less(Float(3)), WordArray([1, 0]))

    def test_less_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).less(WordArray([2, 3])), WordArray([0, 0]))

    def test_less_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).less(FloatArray([2, 3])), WordArray([0, 0]))

    def test_less_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).less(MixedArray([Word(2), Float(2)])), WordArray([0, 0]))

class MoreTests(TestCase):
    def test_more_word_word(self):
        assert_equal(Word(1).more(Word(2)), Word(0))

    def test_more_word_real(self):
        assert_equal(Word(1).more(Float(2)), Word(0))

    def test_more_word_word_array(self):
        assert_equal(Word(1).more(WordArray([2, 3])), Word(0))

    def test_more_word_real_array(self):
        assert_equal(Word(1).more(FloatArray([2, 3])), Word(0))

    def test_more_word_mixed_array(self):
        assert_equal(Word(1).more(MixedArray([Word(2), Float(3)])), Word(0))

    def test_more_real_word(self):
        assert_equal(Float(1).more(Word(-1)), Word(1))

    def test_more_real_real(self):
        assert_equal(Float(1).more(Float(2)), Word(0))

    def test_more_real_word_array(self):
        assert_equal(Float(1).more(WordArray([2, 3])), Word(0))

    def test_more_real_real_array(self):
        assert_equal(Float(1).more(FloatArray([2, 3])), Word(0))

    def test_more_real_mixed_array(self):
        assert_equal(Float(1).more(MixedArray([Word(2), Float(3)])), Word(0))

    def test_more_word_array_word(self):
        assert_equal(WordArray([2, 3]).more(Word(1)), WordArray([1, 1]))

    def test_more_word_array_real(self):
        assert_equal(WordArray([2, 3]).more(Float(1)), WordArray([1, 1]))

    def test_more_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).more(WordArray([2, 3])), WordArray([0, 0]))

    def test_more_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).more(FloatArray([2, 3])), WordArray([0, 0]))

    def test_more_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).more(MixedArray([Word(2), Float(3)])), WordArray([0, 0]))

    def test_more_real_array_word(self):
        assert_equal(FloatArray([2, 3]).more(Word(1)), WordArray([1, 1]))

    def test_more_real_array_real(self):
        assert_equal(FloatArray([2, 3]).more(Float(1)), WordArray([1, 1]))

    def test_more_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).more(WordArray([2, 3])), WordArray([0, 0]))

    def test_more_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).more(FloatArray([2, 3])), WordArray([0, 0]))

    def test_more_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).more(MixedArray([Word(2), Float(3)])), WordArray([0, 0]))

    def test_more_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).more(Word(3)), WordArray([0, 0]))

    def test_more_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).more(Float(3)), WordArray([0, 0]))

    def test_more_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).more(WordArray([2, 3])), WordArray([0, 0]))

    def test_more_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).more(FloatArray([2, 3])), WordArray([0, 0]))

    def test_more_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).more(MixedArray([Word(2), Float(2)])), WordArray([0, 1]))

class EqualTests(TestCase):
    def test_equal_word_word(self):
        assert_equal(Word(1).equal(Word(2)), Word(0))

    def test_equal_word_real(self):
        assert_equal(Word(1).equal(Float(2)), Word(0))

    def test_equal_word_word_array(self):
        assert_equal(Word(1).equal(WordArray([2, 3])), Word(0))

    def test_equal_word_real_array(self):
        assert_equal(Word(1).equal(FloatArray([2, 3])), Word(0))

    def test_equal_word_mixed_array(self):
        assert_equal(Word(1).equal(MixedArray([Word(2), Float(3)])), Word(0))

    def test_equal_real_word(self):
        assert_equal(Float(1).equal(Word(-1)), Word(0))

    def test_equal_real_real(self):
        assert_equal(Float(1).equal(Float(2)), Word(0))

    def test_equal_real_word_array(self):
        assert_equal(Float(1).equal(WordArray([2, 3])), Word(0))

    def test_equal_real_real_array(self):
        assert_equal(Float(1).equal(FloatArray([2, 3])), Word(0))
    def test_equal_real_mixed_array(self):
        assert_equal(Float(1).equal(MixedArray([Word(2), Float(3)])), Word(0))

    def test_equal_word_array_word(self):
        assert_equal(WordArray([2, 3]).equal(Word(1)), WordArray([0, 0]))

    def test_equal_word_array_real(self):
        assert_equal(WordArray([2, 3]).equal(Float(1)), WordArray([0, 0]))

    def test_equal_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).equal(WordArray([2, 3])), WordArray([1, 1]))

    def test_equal_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).equal(FloatArray([2, 3])), WordArray([1, 1]))

    def test_equal_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).equal(MixedArray([Word(2), Float(3)])), WordArray([1, 1]))

    def test_equal_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).equal(Word(3)), WordArray([0, 1]))

    def test_equal_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).equal(Float(3)), WordArray([0, 1]))

    def test_equal_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).equal(WordArray([2, 3])), WordArray([0, 0]))

    def test_equal_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).equal(FloatArray([2, 3])), WordArray([0, 0]))

    def test_equal_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).equal(MixedArray([Word(2), Float(2)])), WordArray([1, 0]))

class IndexTests(TestCase):
    def test_index_word_word_array(self):
        assert_equal(Word(1).index(WordArray([2, 3])), Word(2))

    def test_index_word_real_array(self):
        assert_equal(Word(1).index(FloatArray([2, 3])), Float(2))

    def test_index_word_mixed_array(self):
        assert_equal(Word(1).index(MixedArray([Word(2), Float(3)])), Word(2))

    def test_index_real_word_array(self):
        assert_equal(Float(0.5).index(WordArray([2, 3])), Word(2))

    def test_index_real_real_array(self):
        assert_equal(Float(0.5).index(FloatArray([2, 3])), Float(2))

    def test_index_real_mixed_array(self):
        assert_equal(Float(0.5).index(MixedArray([Word(2), Float(3)])), Word(2))

    def test_index_word_array_word(self):
        assert_equal(WordArray([2, 3]).index(Word(1)), Word(2))

    def test_index_word_array_real(self):
        assert_equal(WordArray([2, 3]).index(Float(0.5)), Word(2))

    def test_index_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).index(WordArray([1, 2])), WordArray([2, 3]))

    def test_index_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).index(FloatArray([0.5, 1.0])), WordArray([2, 3]))

    def test_index_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).index(MixedArray([Word(1), Float(1.0)])), WordArray([2, 3]))

    def test_index_real_array_word(self):
        assert_equal(FloatArray([2, 3]).index(Word(1)), Float(2))

    def test_index_real_array_real(self):
        assert_equal(FloatArray([2, 3]).index(Float(0.5)), Float(2))

    def test_index_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).index(WordArray([1, 2])), FloatArray([2, 3]))

    def test_index_real_array_real_array(self):
        assert_equal(FloatArray([2, 3]).index(FloatArray([0.5, 1.0])), FloatArray([2, 3]))

    def test_index_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).index(MixedArray([Word(1), Float(1.0)])), FloatArray([2, 3]))

    def test_index_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).index(Word(1)), Word(2))

    def test_index_mixed_array_real(self):
        assert_equal(MixedArray([Word(2), Float(3)]).index(Float(0.5)), Word(2))

    def test_index_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).index(WordArray([1, 2])), MixedArray([Word(2), Float(3)]))

    def test_index_mixed_array_real_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).index(FloatArray([0.5, 1.0])), MixedArray([Word(2), Float(3)]))

    def test_index_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).index(MixedArray([Word(1), Float(1)])), MixedArray([Word(2), Float(3)]))

class CutTests(TestCase):
    def test_cut_word_word_array(self):
        assert_equal(Word(1).cut(WordArray([2, 3])), WordArray([3]))

    def test_cut_word_real_array(self):
        assert_equal(Word(1).cut(FloatArray([2, 3])), FloatArray([3]))

    def test_cut_word_mixed_array(self):
        assert_equal(Word(1).cut(MixedArray([Word(2), Float(3)])), MixedArray([Float(3)]))

    def test_cut_word_array_word(self):
        assert_equal(WordArray([2, 3]).cut(Word(1)), WordArray([3]))

    def test_cut_word_array_word_array(self):
        assert_equal(WordArray([2, 3]).cut(WordArray([1, 2])), MixedArray([WordArray([2])]))
        assert_equal(WordArray([2, 3]).cut(WordArray([])), WordArray([2, 3]))
        assert_equal(WordArray([]).cut(WordArray([1, 2])), MixedArray([WordArray([])]))

    def test_cut_word_array_real_array(self):
        assert_equal(WordArray([2, 3]).cut(FloatArray([0.5, 1.0])), MixedArray([WordArray([2]), WordArray([3]), WordArray([])]))
        assert_equal(WordArray([2, 3]).cut(FloatArray([])), MixedArray([WordArray([2, 3])]))

    def test_cut_word_array_mixed_array(self):
        assert_equal(WordArray([2, 3]).cut(MixedArray([Word(1), Word(2)])), MixedArray([WordArray([3])]))
        assert_equal(WordArray([2, 3]).cut(MixedArray([])), WordArray([2, 3]))

    def test_cut_real_array_word(self):
        assert_equal(FloatArray([2, 3]).cut(Word(1)), FloatArray([3]))

    def test_cut_real_array_word_array(self):
        assert_equal(FloatArray([2, 3]).cut(WordArray([1, 2])), MixedArray([WordArray([]), WordArray([2]), WordArray([3])]))
        assert_equal(FloatArray([2, 3]).cut(WordArray([])), MixedArray([FloatArray([2, 3])]))

    def test_cut_real_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).cut(MixedArray([Word(1), Word(2)])), MixedArray([FloatArray([3])]))

    def test_cut_mixed_array_word(self):
        assert_equal(MixedArray([Word(2), Float(3)]).cut(Word(1)), MixedArray([Float(3)]))

    def test_cut_mixed_array_word_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).cut(WordArray([1, 2])), MixedArray([MixedArray([]), MixedArray([Word(2)]), MixedArray([Float(3)])]))
        assert_equal(MixedArray([Word(2), Float(3)]).cut(WordArray([])), MixedArray([MixedArray([Word(2), Float(3)])]))

    def test_cut_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Word(2), Float(3)]).cut(MixedArray([Word(1), Word(2)])), MixedArray([MixedArray([]), MixedArray([Word(2)]), MixedArray([Float(3)])]))

    def test_cut_errors(self):
        assert_equal(WordArray([1, 2, 3]).cut(Float(1)).o, NounType.ERROR)

class GradeUpTests(TestCase):
    def test_gradeUp_word_array(self):
        assert_equal(WordArray([0, 1, 0, 2]).gradeUp(), WordArray([1, 3, 2, 4]))

    def test_gradeUp_real_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).gradeUp(), WordArray([1, 3, 2, 4]))

    def test_gradeUp_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).gradeUp(), WordArray([1, 3, 2, 4]))

class GradeDownTests(TestCase):
    def test_gradeDown_word_array(self):
        assert_equal(WordArray([0, 1, 0, 2]).gradeDown(), WordArray([4, 2, 3, 1]))

    def test_gradeDown_real_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).gradeDown(), WordArray([4, 2, 3, 1]))

    def test_gradeDown_mixed_array(self):
        assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).gradeDown(), WordArray([4, 2, 3, 1]))

# class ReplicatedTests(TestCase):
#     def test_replicate_word_array(self):
#         assert_equal(WordArray([0, 1, 0, 2]).replicate(WordArray([0, 1, 2, 3])), WordArray([1, 0, 0, 2, 2, 2]))
#
#     def test_replicate_real_array(self):
#         assert_equal(FloatArray([0, 1, 0, 2]).replicate(WordArray([0, 1, 2, 3])), FloatArray([1, 0, 0, 2, 2, 2]))
#
#     def test_replicate_mixed_array(self):
#         assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).replicate(WordArray([0, 1, 2, 3])), MixedArray([Float(1), Word(0), Word(0), Float(2), Float(2), Float(2)]))

class TransposeTests(TestCase):
    def test_transpose_mixed_array(self):
        assert_equal(MixedArray([WordArray([1, 2]), WordArray([3, 4])]).transpose(), MixedArray([WordArray([1, 3]), WordArray([2, 4])]))

# class GroupTests(TestCase):
#     def test_group_word_array(self):
#         assert_equal(WordArray([0, 1, 0, 2]).group(), Dictionary(WordArray([0, 1, 2]), MixedArray([WordArray([1, 3]), WordArray([2]), WordArray([4])])))
#
#     def test_group_real_array(self):
#         assert_equal(FloatArray([0, 1, 0, 2]).group(), Dictionary(WordArray([0, 1, 2]), MixedArray([WordArray([1, 3]), WordArray([2]), WordArray([4])])))
#
#     def test_group_mixed_array(self):
#         assert_equal(MixedArray([Word(0), Float(1), Word(0), Float(2)]).group(), Dictionary(MixedArray([Word(0), Float(1), Float(2)]), MixedArray([WordArray([1, 3]), WordArray([2]), WordArray([4])])))

# class DictionaryTests(TestCase):
#     def test_dictionary_get(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).get(Word(1)), Word(4))
#
#     def test_dictionary_put(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).put(Word(1), Word(6)), Dictionary(WordArray([1, 2, 3]), WordArray([6, 5, 6])))
#
#     def test_dictionary_contains(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).contains(Word(1)), Word(1))
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).contains(Word(7)), Word(0))
#
#     def test_dictionary_remove(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).remove(Word(1)), Dictionary(WordArray([2, 3]), WordArray([5, 6])))
#
#     def test_dictionary_keys(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).keys(), WordArray([1, 2, 3]))
#
#     def test_dictionary_values(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).values(), WordArray([4, 5, 6]))
#
#     def test_dictionary_items(self):
#         assert_equal(Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])).items(), MixedArray([WordArray([1, 4]), WordArray([2, 5]), WordArray([3, 6])]))
#
#     def test_amend_word_word(self):
#         assert_equal(Word(1).amend(Word(4)), Dictionary(WordArray([1]), WordArray([4])))
#
#     def test_amend_word_real(self):
#         assert_equal(Word(1).amend(Float(4)), Dictionary(WordArray([1]), FloatArray([4])))
#
#     def test_amend_real_word(self):
#         assert_equal(Float(1).amend(Word(4)), Dictionary(FloatArray([1]), WordArray([4])))
#
#     def test_amend_real_real(self):
#         assert_equal(Float(1).amend(Float(4)), Dictionary(FloatArray([1]), FloatArray([4])))
#
#     def test_amend_word_array_word_array(self):
#         assert_equal(WordArray([1, 2, 3]).amend(WordArray([4, 5, 6])), Dictionary(WordArray([1, 2, 3]), WordArray([4, 5, 6])))
#
#     def test_amend_word_array_real_array(self):
#         assert_equal(WordArray([1, 2, 3]).amend(FloatArray([4, 5, 6])), Dictionary(WordArray([1, 2, 3]), FloatArray([4, 5, 6])))
#
#     def test_amend_word_array_mixed_array(self):
#         assert_equal(WordArray([1, 2, 3]).amend(MixedArray([Word(4), Float(5), Word(6)])), Dictionary(WordArray([1, 2, 3]), MixedArray([Word(4), Float(5), Word(6)])))
#
#     def test_amend_real_array_word_array(self):
#         assert_equal(FloatArray([1, 2, 3]).amend(WordArray([4, 5, 6])), Dictionary(FloatArray([1, 2, 3]), WordArray([4, 5, 6])))
#
#     def test_amend_real_array_real_array(self):
#         assert_equal(FloatArray([1, 2, 3]).amend(FloatArray([4, 5, 6])), Dictionary(FloatArray([1, 2, 3]), FloatArray([4, 5, 6])))
#
#     def test_amend_real_array_mixed_array(self):
#         assert_equal(FloatArray([1, 2, 3]).amend(MixedArray([Word(4), Float(5), Word(6)])), Dictionary(FloatArray([1, 2, 3]), MixedArray([Word(4), Float(5), Word(6)])))
#
#     def test_amend_mixed_array_word_array(self):
#         assert_equal(MixedArray([Word(1), Float(2), Word(3)]).amend(WordArray([4, 5, 6])), Dictionary(MixedArray([Word(1), Float(2), Word(3)]), WordArray([4, 5, 6])))
#
#     def test_amend_mixed_array_real_array(self):
#         assert_equal(MixedArray([Word(1), Float(2), Word(3)]).amend(FloatArray([4, 5, 6])), Dictionary(MixedArray([Word(1), Float(2), Word(3)]), FloatArray([4, 5, 6])))
#
#     def test_amend_mixed_array_mixed_array(self):
#         assert_equal(MixedArray([Word(1), Float(2), Word(3)]).amend(MixedArray([Word(4), Float(5), Word(6)])), Dictionary(MixedArray([Word(1), Float(2), Word(3)]), MixedArray([Word(4), Float(5), Word(6)])))

class SqueezeTests(TestCase):
    def test_squeeze(self):
        assert_equal(squeeze(0), b"\x00")
        assert_equal(squeeze(1), b"\x01\x01")
        assert_equal(squeeze(256), b"\x02\x01\x00")
        assert_equal(squeeze(-256), b"\xfe\xff\x00")

    def test_expand(self):
        assert_equal(expand(b"\x00"), (0, b''))
        assert_equal(expand(b"\x01\x01"), (1, b''))
        assert_equal(expand(b"\x02\x01\x00"), (256, b''))
        assert_equal(expand(b"\xfe\xff\x00"), (-256, b''))

class SerializationTests(TestCase):
    def test_serialization_to_bytes_word(self):
        assert_equal(Word(0).to_bytes(), b"\x01\x02\x00\x00")
        assert_equal(Word(1).to_bytes(), b"\x01\x03\x00\x01\x01")
        assert_equal(Word(256).to_bytes(), b"\x01\x04\x00\x02\x01\x00")
        assert_equal(Word(-256).to_bytes(), b"\x01\x04\x00\xfe\xff\x00")

    def test_serialization_to_bytes_real(self):
        assert_equal(Float(0).to_bytes(),b'\x01\x05\x01\x00\x00\x00\x00')
        assert_equal(Float(1).to_bytes(),b'\x01\x05\x01\x00\x00\x80?')
        assert_equal(Float(256).to_bytes(), b'\x01\x05\x01\x00\x00\x80C')
        assert_equal(Float(-256).to_bytes(), b'\x01\x05\x01\x00\x00\x80\xc3')

    def test_serialization_from_bytes_word(self):
        assert_equal(Storage.from_bytes(Word(0).to_bytes()), (Word(0), b''))
        assert_equal(Storage.from_bytes(Word(1).to_bytes()), (Word(1), b''))
        assert_equal(Storage.from_bytes(Word(256).to_bytes()), (Word(256), b''))
        assert_equal(Storage.from_bytes(Word(-256).to_bytes()), (Word(-256), b''))

    def test_serialization_from_bytes_real(self):
        assert_equal(Storage.from_bytes(Float(0).to_bytes()), (Float(0), b''))
        assert_equal(Storage.from_bytes(Float(1).to_bytes()), (Float(1), b''))
        assert_equal(Storage.from_bytes(Float(256).to_bytes()), (Float(256), b''))
        assert_equal(Storage.from_bytes(Float(-256).to_bytes()), (Float(-256), b''))

    def test_serialization_to_bytes_word_array(self):
        assert_equal(WordArray([]).to_bytes(), b'\x01\x01\x02')
        assert_equal(WordArray([1]).to_bytes(), b'\x01\x03\x02\x01\x01')
        assert_equal(WordArray([1, 2, 3]).to_bytes(), b'\x01\x07\x02\x01\x01\x01\x02\x01\x03')
        assert_equal(WordArray([1, 2, 3, 4]).to_bytes(), b'\x01\t\x02\x01\x01\x01\x02\x01\x03\x01\x04')

    def test_serialization_from_bytes_word_array(self):
        assert_equal(Storage.from_bytes(WordArray([]).to_bytes()), (WordArray([]), b''))
        assert_equal(Storage.from_bytes(WordArray([1]).to_bytes()), (WordArray([1]), b''))
        assert_equal(Storage.from_bytes(WordArray([1, 2, 3]).to_bytes()), (WordArray([1, 2, 3]), b''))
        assert_equal(Storage.from_bytes(WordArray([1, 2, 3, 4]).to_bytes()), (WordArray([1, 2, 3, 4]), b''))

    def test_serialization_to_bytes_real_array(self):
        assert_equal(FloatArray([]).to_bytes(),  b'\x01\x01\x03')
        assert_equal(FloatArray([1]).to_bytes(), b'\x01\x05\x03\x00\x00\x80?')
        assert_equal(FloatArray([1, 2, 3]).to_bytes(), b'\x01\r\x03\x00\x00\x80?\x00\x00\x00@\x00\x00@@')
        assert_equal(FloatArray([1, 2, 3, 4]).to_bytes(),  b'\x01\x11\x03\x00\x00\x80?\x00\x00\x00@\x00\x00@@\x00\x00\x80@')

    def test_serialization_from_bytes_real_array(self):
        assert_equal(Storage.from_bytes(FloatArray([]).to_bytes()), (FloatArray([]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1]).to_bytes()), (FloatArray([1]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1, 2, 3]).to_bytes()), (FloatArray([1, 2, 3]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1, 2, 3, 4]).to_bytes()), (FloatArray([1, 2, 3, 4]), b''))

    def test_serialization_to_bytes_mixed_array(self):
        assert_equal(MixedArray([]).to_bytes(),b'\x01\x01\x04')
        assert_equal(MixedArray([Word(1)]).to_bytes(), b'\x01\x06\x04\x01\x03\x00\x01\x01')
        assert_equal(MixedArray([Word(1), Float(2), WordArray([3])]).to_bytes(), b'\x01\x12\x04\x01\x03\x00\x01\x01\x01\x05\x01\x00\x00\x00@\x01\x03\x02\x01\x03')
        assert_equal(MixedArray([WordArray([1, 2]), FloatArray([3]), MixedArray([Word(4)])]).to_bytes(), b'\x01\x17\x04\x01\x05\x02\x01\x01\x01\x02\x01\x05\x03\x00\x00@@\x01\x06\x04\x01\x03\x00\x01\x04')

    def test_serialization_from_bytes_mixed_array(self):
        assert_equal(Storage.from_bytes(MixedArray([]).to_bytes()),  (MixedArray([]), b''))
        assert_equal(Storage.from_bytes(MixedArray([Word(1)]).to_bytes()), (MixedArray([Word(1)]), b''))
        assert_equal(Storage.from_bytes(MixedArray([Word(1), Float(2), WordArray([3])]).to_bytes()), (MixedArray([Word(1), Float(2), WordArray([3])]), b''))
        assert_equal(Storage.from_bytes(MixedArray([WordArray([1, 2]), FloatArray([3]), MixedArray([Word(4)])]).to_bytes()), (MixedArray([WordArray([1, 2]), FloatArray([3]), MixedArray([Word(4)])]), b''))

class AdverbTests(TestCase):
    def test_each(self):
        assert_equal(Word(1).each(Monads.negate.symbol()), Word(-1))
        assert_equal(Float(1).each(Monads.negate.symbol()), Float(-1))
        assert_equal(WordArray([1, 2, 3]).each(Monads.negate.symbol()), MixedArray([Word(-1), Word(-2), Word(-3)]))
        assert_equal(FloatArray([1, 2, 3]).each(Monads.negate.symbol()), MixedArray([Float(-1), Float(-2), Float(-3)]))
        assert_equal(MixedArray([Word(1), Word(2), Word(3)]).each(Monads.negate.symbol()), MixedArray([Word(-1), Word(-2), Word(-3)]))

    def test_each2(self):
        assert_equal(Word(1).each2(Dyads.plus.symbol(), Word(1)), Word(2))
        assert_equal(Float(1).each2(Dyads.plus.symbol(), Float(1)), Float(2))
        assert_equal(WordArray([1, 2, 3]).each2(Dyads.plus.symbol(), Word(4)), MixedArray([Word(5), Word(6), Word(7)]))
        assert_equal(WordArray([1, 2, 3]).each2(Dyads.plus.symbol(), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(WordArray([1, 2, 3]).each2(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([Word(5), Word(7), Word(9)]))
        assert_equal(WordArray([1, 2, 3]).each2(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(WordArray([1, 2, 3]).each2(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Word(5), Word(7), Word(9)]))

        assert_equal(FloatArray([1, 2, 3]).each2(Dyads.plus.symbol(), Word(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Dyads.plus.symbol(), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([Word(5), Word(7), Word(9)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Word(5), Word(7), Word(9)]))

        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).each2(Dyads.plus.symbol(), Word(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).each2(Dyads.plus.symbol(), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).each2(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([Word(5), Float(7), Word(9)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).each2(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).each2(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Word(5), Float(7), Word(9)]))

    def test_eachLeft(self):
        assert_equal(Word(1).eachLeft(Dyads.plus.symbol(), Word(4)), Word(5))
        assert_equal(Word(1).eachLeft(Dyads.plus.symbol(), Float(4)), Float(5))
        assert_equal(Word(1).eachLeft(Dyads.plus.symbol(), WordArray([4, 5, 6])), WordArray([5, 6, 7]))
        assert_equal(Word(1).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Word(1).eachLeft(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Word(5), Word(6), Word(7)]))

        assert_equal(Float(1).eachLeft(Dyads.plus.symbol(), Word(4)), Float(5))
        assert_equal(Float(1).eachLeft(Dyads.plus.symbol(), Float(4)), Float(5))
        assert_equal(Float(1).eachLeft(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(Float(1).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(Float(1).eachLeft(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), Word(4)), WordArray([5, 6, 7]))
        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([WordArray([5, 6, 7]), WordArray([6, 7, 8]), WordArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([WordArray([5, 6, 7]), FloatArray([6, 7, 8]), WordArray([7, 8, 9])]))

        assert_equal(FloatArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), Word(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachLeft(Dyads.plus.symbol(), Word(4)), MixedArray([Word(5), Float(6), Word(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachLeft(Dyads.plus.symbol(), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachLeft(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([MixedArray([Word(5), Float(6), Word(7)]), MixedArray([Word(6), Float(7), Word(8)]), MixedArray([Word(7), Float(8), Word(9)])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachLeft(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([MixedArray([Float(5), Float(6), Float(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Float(7), Float(8), Float(9)])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachLeft(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([MixedArray([Word(5), Float(6), Word(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Word(7), Float(8), Word(9)])]))

    def test_eachRight(self):
        assert_equal(Word(1).eachRight(Dyads.plus.symbol(), Word(4)), Word(5))
        assert_equal(Word(1).eachRight(Dyads.plus.symbol(), Float(4)), Float(5))
        assert_equal(Word(1).eachRight(Dyads.plus.symbol(), WordArray([4, 5, 6])), WordArray([5, 6, 7]))
        assert_equal(Word(1).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Word(1).eachRight(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Word(5), Word(6), Word(7)]))

        assert_equal(Float(1).eachRight(Dyads.plus.symbol(), Word(4)), Float(5))
        assert_equal(Float(1).eachRight(Dyads.plus.symbol(), Float(4)), Float(5))
        assert_equal(Float(1).eachRight(Dyads.plus.symbol(), WordArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).eachRight(Dyads.plus.symbol(), MixedArray([Word(4), Word(5), Word(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), Word(4)), WordArray([5, 6, 7]))
        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([WordArray([5, 6, 7]), WordArray([6, 7, 8]), WordArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(WordArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([WordArray([5, 6, 7]), FloatArray([6, 7, 8]), WordArray([7, 8, 9])]))

        assert_equal(FloatArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), Word(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachRight(Dyads.plus.symbol(), Word(4)), MixedArray([Word(5), Float(6), Word(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachRight(Dyads.plus.symbol(), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachRight(Dyads.plus.symbol(), WordArray([4, 5, 6])), MixedArray([MixedArray([Word(5), Float(6), Word(7)]), MixedArray([Word(6), Float(7), Word(8)]), MixedArray([Word(7), Float(8), Word(9)])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachRight(Dyads.plus.symbol(), FloatArray([4, 5, 6])), MixedArray([MixedArray([Float(5), Float(6), Float(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Float(7), Float(8), Float(9)])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).eachRight(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([MixedArray([Word(5), Float(6), Word(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Word(7), Float(8), Word(9)])]))

    def test_eachPair(self):
        assert_equal(WordArray([4, 5, 6]).eachPair(Dyads.plus.symbol()), MixedArray([Word(9), Word(11)]))
        assert_equal(FloatArray([4, 5, 6]).eachPair(Dyads.plus.symbol()), MixedArray([Float(9), Float(11)]))
        assert_equal(MixedArray([Word(4), Word(5), Word(6)]).eachPair(Dyads.plus.symbol()), MixedArray([Word(9), Word(11)]))

    def test_over(self):
        assert_equal(Word(4).over(Dyads.plus.symbol()), Word(4))
        assert_equal(Float(4).over(Dyads.plus.symbol()), Float(4))

        assert_equal(WordArray([]).over(Dyads.plus.symbol()), WordArray([]))
        assert_equal(WordArray([4]).over(Dyads.plus.symbol()), WordArray([4]))
        assert_equal(WordArray([4, 5, 6]).over(Dyads.plus.symbol()), Word(15))

        assert_equal(FloatArray([]).over(Dyads.plus.symbol()), FloatArray([]))
        assert_equal(FloatArray([4]).over(Dyads.plus.symbol()), FloatArray([4]))
        assert_equal(FloatArray([4, 5, 6]).over(Dyads.plus.symbol()), Float(15))

        assert_equal(MixedArray([]).over(Dyads.plus.symbol()), MixedArray([]))
        assert_equal(MixedArray([Word(4)]).over(Dyads.plus.symbol()), MixedArray([Word(4)]))
        assert_equal(MixedArray([Word(4), Word(5), Word(6)]).over(Dyads.plus.symbol()), Word(15))

    def test_overNeutral(self):
        assert_equal(Word(1).overNeutral(Dyads.plus.symbol(), Word(1)), Word(2))
        assert_equal(Word(1).overNeutral(Dyads.plus.symbol(), Float(1)), Float(2))
        assert_equal(Word(1).overNeutral(Dyads.plus.symbol(), WordArray([4, 5, 6])), WordArray([5, 6, 7]))
        assert_equal(Word(1).overNeutral(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Word(1).overNeutral(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([Word(5), Float(6), Word(7)]))

        assert_equal(Float(1).overNeutral(Dyads.plus.symbol(), Word(1)), Float(2))
        assert_equal(Float(1).overNeutral(Dyads.plus.symbol(), Float(1)), Float(2))
        assert_equal(Float(1).overNeutral(Dyads.plus.symbol(), WordArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).overNeutral(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).overNeutral(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(WordArray([1, 2]).overNeutral(Dyads.plus.symbol(), Word(1)), Word(4))
        assert_equal(WordArray([1, 2]).overNeutral(Dyads.plus.symbol(), Float(1)), Float(4))
        assert_equal(WordArray([1, 2]).overNeutral(Dyads.plus.symbol(), WordArray([4, 5, 6])), WordArray([7, 8, 9]))
        assert_equal(WordArray([1, 2]).overNeutral(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(WordArray([1, 2]).overNeutral(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([Word(7), Float(8), Word(9)]))
        assert_equal(WordArray([]).overNeutral(Dyads.plus.symbol(), Word(1)).o, NounType.ERROR)

        assert_equal(FloatArray([1, 2]).overNeutral(Dyads.plus.symbol(), Word(1)), Float(4))
        assert_equal(FloatArray([1, 2]).overNeutral(Dyads.plus.symbol(), Float(1)), Float(4))
        assert_equal(FloatArray([1, 2]).overNeutral(Dyads.plus.symbol(), WordArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(FloatArray([1, 2]).overNeutral(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(FloatArray([1, 2]).overNeutral(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([Float(7), Float(8), Float(9)]))
        assert_equal(FloatArray([]).overNeutral(Dyads.plus.symbol(), Word(1)).o, NounType.ERROR)

        assert_equal(MixedArray([Word(1), Float(2)]).overNeutral(Dyads.plus.symbol(), Word(1)), Float(4))
        assert_equal(MixedArray([Word(1), Float(2)]).overNeutral(Dyads.plus.symbol(), Float(1)), Float(4))
        assert_equal(MixedArray([Word(1), Float(2)]).overNeutral(Dyads.plus.symbol(), WordArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(MixedArray([Word(1), Float(2)]).overNeutral(Dyads.plus.symbol(), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(MixedArray([Word(1), Float(2)]).overNeutral(Dyads.plus.symbol(), MixedArray([Word(4), Float(5), Word(6)])), MixedArray([Float(7), Float(8), Float(9)]))
        assert_equal(MixedArray([]).overNeutral(Dyads.plus.symbol(), Word(1)).o, NounType.ERROR)

    def test_converge(self):
        assert_equal(WordArray([1, 2, 3]).converge(Monads.shape.symbol()), WordArray([1]))

    def test_whileOne(self):
        assert_equal(Word(0).whileOne(Monads.atom.symbol(), Monads.enclose.symbol()), WordArray([0]))

    def test_iterate(self):
        assert_equal(WordArray([1, 2, 3]).iterate(Monads.shape.symbol(), Word(2)), WordArray([1]))
        assert_equal(FloatArray([1, 2, 3]).iterate(Monads.shape.symbol(), Word(2)), WordArray([1]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).iterate(Monads.shape.symbol(), Word(2)), WordArray([1]))

        assert_equal(Word(2).iterate(Monads.shape.symbol(), WordArray([1, 2, 3])).o, NounType.ERROR)
        assert_equal(Word(-2).iterate(Monads.shape.symbol(), WordArray([1, 2, 3])).o, NounType.ERROR)
        assert_equal(Float(2).iterate(Monads.shape.symbol(), WordArray([1, 2, 3])).o, NounType.ERROR)

    def test_scanOver(self):
        assert_equal(Word(1).scanOver(Monads.shape.symbol()), WordArray([1]))

        assert_equal(WordArray([1, 2, 3]).scanOver(Dyads.plus.symbol()), MixedArray([Word(1), Word(3), Word(6)]))
        assert_equal(WordArray([]).scanOver(Dyads.plus.symbol()), WordArray([]))

        assert_equal(FloatArray([1, 2, 3]).scanOver(Dyads.plus.symbol()), MixedArray([Float(1), Float(3), Float(6)]))
        assert_equal(FloatArray([]).scanOver(Dyads.plus.symbol()), FloatArray([]))

        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanOver(Dyads.plus.symbol()), MixedArray([Word(1), Float(3), Float(6)]))
        assert_equal(MixedArray([]).scanOver(Dyads.plus.symbol()), MixedArray([]))

    def test_scanOverNeutral(self):
        assert_equal(Word(1).scanOverNeutral(Dyads.plus.symbol(), Word(1)), MixedArray([Word(1), Word(2)]))
        assert_equal(WordArray([1, 2, 3]).scanOverNeutral(Dyads.plus.symbol(), Word(1)), MixedArray([Word(1), Word(2), Word(4), Word(7)]))
        assert_equal(FloatArray([1, 2, 3]).scanOverNeutral(Dyads.plus.symbol(), Word(1)), MixedArray([Word(1), Float(2), Float(4), Float(7)]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanOverNeutral(Dyads.plus.symbol(), Word(1)), MixedArray([Word(1), Word(2), Float(4), Float(7)]))

    def test_scanConverging(self):
        assert_equal(WordArray([1, 2, 3]).scanConverging(Monads.shape.symbol()), MixedArray([WordArray([1, 2, 3]), WordArray([3]), WordArray([1])]))
        assert_equal(FloatArray([1, 2, 3]).scanConverging(Monads.shape.symbol()), MixedArray([FloatArray([1, 2, 3]), WordArray([3]), WordArray([1])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanConverging(Monads.shape.symbol()), MixedArray([MixedArray([Word(1), Float(2), Word(3)]), WordArray([3]), WordArray([1])]))

    def test_scanWhileOne(self):
        assert_equal(Word(0).scanWhileOne(Monads.atom.symbol(), Monads.enclose.symbol()), MixedArray([Word(0), WordArray([0])]))

    def test_scanIterating(self):
        assert_equal(WordArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Word(2)), MixedArray([WordArray([1, 2, 3]), WordArray([3]), WordArray([1])]))
        assert_equal(WordArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Word(-2)).o, NounType.ERROR)
        assert_equal(WordArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Float(2)).o, NounType.ERROR)

        assert_equal(FloatArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Word(2)), MixedArray([FloatArray([1, 2, 3]), WordArray([3]), WordArray([1])]))
        assert_equal(FloatArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Word(-2)).o, NounType.ERROR)
        assert_equal(FloatArray([1, 2, 3]).scanIterating(Monads.shape.symbol(), Float(2)).o, NounType.ERROR)

        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanIterating(Monads.shape.symbol(), Word(2)), MixedArray([MixedArray([Word(1), Float(2), Word(3)]), WordArray([3]), WordArray([1])]))
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanIterating(Monads.shape.symbol(), Word(-2)).o, NounType.ERROR)
        assert_equal(MixedArray([Word(1), Float(2), Word(3)]).scanIterating(Monads.shape.symbol(), Float(2)).o, NounType.ERROR)

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
