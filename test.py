from storage import *
from testify import TestCase, assert_equal, assert_not_equal, assert_isinstance
from squeeze import squeeze, expand

# Examples from the book "An Introduction to Array Programming in Klong" by Nils
class BookTests(TestCase):
    pass

class Pythonic(TestCase):
    def test_eq(self):
        assert_equal(Integer(1), Integer(1))
        assert_not_equal(Integer(1), Integer(2))

        assert_not_equal(Integer(1), Float(1))
        assert_not_equal(Integer(1), Float(2))

        assert_not_equal(Integer(1), IntegerArray([1]))
        assert_not_equal(Integer(1), FloatArray([1]))
        assert_not_equal(Integer(1), MixedArray([Integer(1)]))

        assert_equal(Float(1), Float(1))
        assert_not_equal(Float(1), Float(2))

        assert_not_equal(Float(1), Integer(1))
        assert_not_equal(Float(1), Integer(2))

        assert_not_equal(Float(1), IntegerArray([1]))
        assert_not_equal(Float(1), FloatArray([1]))
        assert_not_equal(Float(1), MixedArray([Integer(1)]))

        assert_equal(IntegerArray([1]), IntegerArray([1]))
        assert_not_equal(IntegerArray([1]), IntegerArray([2]))

        assert_not_equal(IntegerArray([1]), FloatArray([1]))
        assert_not_equal(IntegerArray([1]), FloatArray([2]))

        assert_equal(FloatArray([1]), FloatArray([1]))
        assert_not_equal(FloatArray([1]), FloatArray([2]))

        assert_not_equal(FloatArray([1]), MixedArray([Integer(1)]))
        assert_not_equal(FloatArray([1]), MixedArray([Float(2)]))

        assert_not_equal(FloatArray([1]), Integer(1))
        assert_not_equal(FloatArray([1]), Float(1))

        assert_equal(MixedArray([Integer(1)]), MixedArray([Integer(1)]))
        assert_not_equal(MixedArray([Integer(1)]), MixedArray([Integer(2)]))

        assert_not_equal(MixedArray([Integer(1)]), IntegerArray([1]))
        assert_not_equal(MixedArray([Integer(1)]), IntegerArray([2]))

        assert_not_equal(MixedArray([Integer(1)]), FloatArray([1]))
        assert_not_equal(MixedArray([Integer(1)]), FloatArray([2]))

        assert_not_equal(MixedArray([Integer(1)]), Integer(1))
        assert_not_equal(MixedArray([Integer(1)]), Float(1))

class AddTests(TestCase):
    def test_add_integer_integer(self):
        assert_equal(Integer(1).plus(Integer(2)), Integer(3))
        assert_equal(Integer(-1).plus(Integer(-1)), Integer(-2))
        assert_equal(Integer(0).plus(Integer(0)), Integer(0))

    def test_add_integer_float(self):
        assert_equal(Integer(1).plus(Float(2)), Float(3))
        assert_equal(Integer(-1).plus(Float(-1)), Float(-2))
        assert_equal(Integer(0).plus(Float(0)), Float(0))

    def test_add_integer_integer_array(self):
        assert_equal(Integer(1).plus(IntegerArray([2, 3])), IntegerArray([3, 4]))
        assert_equal(Integer(-1).plus(IntegerArray([-1, 0])), IntegerArray([-2, -1]))
        assert_equal(Integer(0).plus(IntegerArray([0, 1])), IntegerArray([0, 1]))

    def test_add_integer_float_array(self):
        assert_equal(Integer(1).plus(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Integer(-1).plus(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Integer(0).plus(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_add_integer_mixed_array(self):
        assert_equal(Integer(1).plus(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(3), Float(4)]))
        assert_equal(Integer(-1).plus(MixedArray([Integer(-1), Float(0)])), MixedArray([Integer(-2), Float(-1)]))
        assert_equal(Integer(0).plus(MixedArray([Integer(0), Float(1)])), MixedArray([Integer(0), Float(1)]))

    def test_add_float_integer(self):
        assert_equal(Float(1).plus(Integer(2)), Float(3))
        assert_equal(Float(-1).plus(Integer(-1)), Float(-2))
        assert_equal(Float(0).plus(Integer(0)), Float(0))

    def test_add_float_float(self):
        assert_equal(Float(1).plus(Float(2)), Float(3))
        assert_equal(Float(-1).plus(Float(-1)), Float(-2))
        assert_equal(Float(0).plus(Float(0)), Float(0))

    def test_add_float_integer_array(self):
        assert_equal(Float(1).plus(IntegerArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).plus(IntegerArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).plus(IntegerArray([0, 1])), FloatArray([0, 1]))

    def test_add_float_float_array(self):
        assert_equal(Float(1).plus(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).plus(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).plus(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_add_float_mixed_array(self):
        assert_equal(Float(1).plus(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(4)]))
        assert_equal(Float(-1).plus(MixedArray([Integer(-1), Float(0)])), MixedArray([Float(-2), Float(-1)]))
        assert_equal(Float(0).plus(MixedArray([Integer(0), Float(1)])), MixedArray([Float(0), Float(1)]))

    def test_add_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).plus(Integer(1)), IntegerArray([3, 4]))
        assert_equal(IntegerArray([-1, 0]).plus(Integer(-1)), IntegerArray([-2, -1]))
        assert_equal(IntegerArray([0, 1]).plus(Integer(0)), IntegerArray([0, 1]))

    def test_add_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).plus(Float(1)), FloatArray([3, 4]))
        assert_equal(IntegerArray([-1, 0]).plus(Float(-1)), FloatArray([-2, -1]))
        assert_equal(IntegerArray([0, 1]).plus(Float(0)), FloatArray([0, 1]))

    def test_add_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 5]), IntegerArray([5, 6])]))
        assert_equal(IntegerArray([-1, 0]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 2]), IntegerArray([2, 3])]))
        assert_equal(IntegerArray([0, 1]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([2, 3]), IntegerArray([3, 4])]))

    def test_add_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).plus(FloatArray([2, 3])), MixedArray([FloatArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(IntegerArray([-1, 0]).plus(FloatArray([2, 3])), MixedArray([FloatArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(IntegerArray([0, 1]).plus(FloatArray([2, 3])), MixedArray([FloatArray([2, 3]), FloatArray([3, 4])]))

    def test_add_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(5)]), MixedArray([Integer(5), Float(6)])]))
        assert_equal(IntegerArray([-1, 0]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2)]), MixedArray([Integer(2), Float(3)])]))
        assert_equal(IntegerArray([0, 1]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2), Float(3)]), MixedArray([Integer(3), Float(4)])]))

    def test_add_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).plus(Integer(2)), MixedArray([Integer(4), Float(5)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).plus(Integer(2)), MixedArray([Integer(1), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).plus(Integer(2)), MixedArray([Integer(2), Float(3)]))

    def test_add_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).plus(Float(2)), MixedArray([Float(4), Float(5)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).plus(Float(2)), MixedArray([Float(1), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).plus(Float(2)), MixedArray([Float(2), Float(3)]))

    def test_add_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).plus(IntegerArray([2, 3])), MixedArray([IntegerArray([2, 3]), FloatArray([3, 4])]))

    def test_add_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).plus(FloatArray([2, 3])), MixedArray([FloatArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).plus(FloatArray([2, 3])), MixedArray([FloatArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).plus(FloatArray([2, 3])), MixedArray([FloatArray([2, 3]), FloatArray([3, 4])]))

    def test_add_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(5)]), MixedArray([Float(5), Float(6)])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2)]), MixedArray([Float(2), Float(3)])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).plus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2), Float(3)]), MixedArray([Float(3), Float(4)])]))

class SubtractTests(TestCase):
    def test_subtract_integer_integer(self):
        assert_equal(Integer(1).minus(Integer(2)), Integer(-1))
        assert_equal(Integer(-1).minus(Integer(-1)), Integer(0))
        assert_equal(Integer(0).minus(Integer(0)), Integer(0))

    def test_subtract_integer_float(self):
        assert_equal(Integer(1).minus(Float(2)), Float(-1))
        assert_equal(Integer(-1).minus(Float(-1)), Float(0))
        assert_equal(Integer(0).minus(Float(0)), Float(0))

    def test_subtract_integer_integer_array(self):
        assert_equal(Integer(1).minus(IntegerArray([2, 3])), IntegerArray([-1, -2]))
        assert_equal(Integer(-1).minus(IntegerArray([-1, 0])), IntegerArray([0, -1]))
        assert_equal(Integer(0).minus(IntegerArray([0, 1])), IntegerArray([0, -1]))

    def test_subtract_integer_float_array(self):
        assert_equal(Integer(1).minus(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Integer(-1).minus(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Integer(0).minus(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_integer_mixed_array(self):
        assert_equal(Integer(1).minus(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(-1), Float(-2)]))
        assert_equal(Integer(-1).minus(MixedArray([Integer(-1), Float(0)])), MixedArray([Integer(0), Float(-1)]))
        assert_equal(Integer(0).minus(MixedArray([Integer(0), Float(1)])), MixedArray([Integer(0), Float(-1)]))

    def test_subtract_float_integer(self):
        assert_equal(Float(1).minus(Integer(-1)), Float(2))
        assert_equal(Float(-1).minus(Integer(0)), Float(-1))
        assert_equal(Float(0).minus(Integer(0)), Float(0))

    def test_subtract_float_float(self):
        assert_equal(Float(1).minus(Float(2)), Float(-1))
        assert_equal(Float(-1).minus(Float(-1)), Float(0))
        assert_equal(Float(0).minus(Float(0)), Float(0))

    def test_subtract_float_integer_array(self):
        assert_equal(Float(1).minus(IntegerArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).minus(IntegerArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).minus(IntegerArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_float_float_array(self):
        assert_equal(Float(1).minus(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).minus(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).minus(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_float_mixed_array(self):
        assert_equal(Float(1).minus(MixedArray([Integer(2), Float(3)])), MixedArray([Float(-1), Float(-2)]))
        assert_equal(Float(-1).minus(MixedArray([Integer(-1), Float(0)])), MixedArray([Float(0), Float(-1)]))
        assert_equal(Float(0).minus(MixedArray([Integer(0), Float(1)])), MixedArray([Float(0), Float(-1)]))

    def test_subtract_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).minus(Integer(1)), IntegerArray([1, 2]))
        assert_equal(IntegerArray([-1, 0]).minus(Integer(-1)), IntegerArray([0, 1]))
        assert_equal(IntegerArray([0, 1]).minus(Integer(0)), IntegerArray([0, 1]))

    def test_subtract_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).minus(Float(1)), FloatArray([1, 2]))
        assert_equal(IntegerArray([-1, 0]).minus(Float(-1)), FloatArray([0, 1]))
        assert_equal(IntegerArray([0, 1]).minus(Float(0)), FloatArray([0, 1]))

    def test_subtract_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([0, -1]), IntegerArray([1, 0])]))
        assert_equal(IntegerArray([-1, 0]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([-3, -4]), IntegerArray([-2, -3])]))
        assert_equal(IntegerArray([0, 1]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([-2, -3]), IntegerArray([-1, -2])]))

    def test_subtract_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).minus(FloatArray([2, 3])), MixedArray([FloatArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(IntegerArray([-1, 0]).minus(FloatArray([2, 3])), MixedArray([FloatArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(IntegerArray([0, 1]).minus(FloatArray([2, 3])), MixedArray([FloatArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(0), Float(-1)]), MixedArray([Integer(1), Float(0)])]))
        assert_equal(IntegerArray([-1, 0]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-3), Float(-4)]), MixedArray([Integer(-2), Float(-3)])]))
        assert_equal(IntegerArray([0, 1]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-2), Float(-3)]), MixedArray([Integer(-1), Float(-2)])]))

    def test_subtract_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).minus(Integer(2)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).minus(Integer(2)), MixedArray([Integer(-3), Float(-2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).minus(Integer(2)), MixedArray([Integer(-2), Float(-1)]))

    def test_subtract_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).minus(Float(2)), MixedArray([Float(0), Float(1)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).minus(Float(2)), MixedArray([Float(-3), Float(-2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).minus(Float(2)), MixedArray([Float(-2), Float(-1)]))

    def test_subtract_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).minus(IntegerArray([2, 3])), MixedArray([IntegerArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).minus(FloatArray([2, 3])), MixedArray([FloatArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).minus(FloatArray([2, 3])), MixedArray([FloatArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).minus(FloatArray([2, 3])), MixedArray([FloatArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(0), Float(-1)]), MixedArray([Float(1), Float(0)])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-3), Float(-4)]), MixedArray([Float(-2), Float(-3)])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).minus(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-2), Float(-3)]), MixedArray([Float(-1), Float(-2)])]))

class TimesTests(TestCase):
    def test_times_integer_integer(self):
        assert_equal(Integer(1).times(Integer(2)), Integer(2))

    def test_times_integer_float(self):
        assert_equal(Integer(1).times(Float(2)), Float(2))

    def test_times_integer_integer_array(self):
        assert_equal(Integer(1).times(IntegerArray([2, 3])), IntegerArray([2, 3]))

    def test_times_integer_float_array(self):
        assert_equal(Integer(1).times(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_times_integer_mixed_array(self):
        assert_equal(Integer(1).times(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3)]))

    def test_times_float_integer(self):
        assert_equal(Float(1).times(Integer(-1)), Float(-1))

    def test_times_float_float(self):
        assert_equal(Float(1).times(Float(2)), Float(2))

    def test_times_float_integer_array(self):
        assert_equal(Float(1).times(IntegerArray([2, 3])), FloatArray([2, 3]))

    def test_times_float_float_array(self):
        assert_equal(Float(1).times(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_times_float_mixed_array(self):
        assert_equal(Float(1).times(MixedArray([Integer(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_times_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).times(Integer(1)), IntegerArray([2, 3]))

    def test_times_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).times(Float(1)), FloatArray([2, 3]))

    def test_times_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).times(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 6]), IntegerArray([6, 9])]))

    def test_times_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).times(FloatArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_times_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).times(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(6)]), MixedArray([Integer(6), Float(9)])]))

    def test_times_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).times(Integer(1)), FloatArray([2, 3]))

    def test_times_float_array_float(self):
        assert_equal(FloatArray([2, 3]).times(Float(1)), FloatArray([2, 3]))

    def test_times_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).times(IntegerArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_times_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).times(FloatArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_times_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).times(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(6)]), MixedArray([Float(6), Float(9)])]))

    def test_times_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).times(Integer(2)), MixedArray([Integer(4), Float(6)]))

    def test_times_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).times(Float(2)), MixedArray([Float(4), Float(6)]))

    def test_times_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).times(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 6]), FloatArray([6, 9])]))

    def test_times_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).times(FloatArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_times_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).times(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(6)]), MixedArray([Float(6), Float(9)])]))

class PowerTests(TestCase):
    def test_power_integer_integer(self):
        assert_equal(Integer(2).power(Integer(2)), Float(4))

    def test_power_integer_float(self):
        assert_equal(Integer(2).power(Float(2)), Float(4))

    def test_power_integer_integer_array(self):
        assert_equal(Integer(2).power(IntegerArray([2, 3])), FloatArray([4, 8]))

    def test_power_integer_float_array(self):
        assert_equal(Integer(2).power(FloatArray([2, 3])), FloatArray([4, 8]))

    def test_power_integer_mixed_array(self):
        assert_equal(Integer(2).power(MixedArray([Integer(2), Float(3)])), MixedArray([Float(4), Float(8)]))

    def test_power_float_integer(self):
        assert_equal(Float(2).power(Integer(2)), Float(4))

    def test_power_float_float(self):
        assert_equal(Float(2).power(Float(2)), Float(4))

    def test_power_float_integer_array(self):
        assert_equal(Float(2).power(IntegerArray([2, 3])), FloatArray([4, 8]))

    def test_power_float_float_array(self):
        assert_equal(Float(2).power(FloatArray([2, 3])), FloatArray([4, 8]))

    def test_power_float_mixed_array(self):
        assert_equal(Float(2).power(MixedArray([Integer(2), Float(3)])), MixedArray([Float(4), Float(8)]))

    def test_power_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).power(Integer(3)), FloatArray([8, 27]))

    def test_power_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).power(Float(1)), FloatArray([2, 3]))

    def test_power_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).power(IntegerArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).power(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

    def test_power_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).power(Integer(3)), FloatArray([8, 27]))

    def test_power_float_array_float(self):
        assert_equal(FloatArray([2, 3]).power(Float(1)), FloatArray([2, 3]))

    def test_power_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).power(IntegerArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).power(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

    def test_power_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).power(Integer(2)), MixedArray([Float(4), Float(9)]))

    def test_power_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).power(Float(2)), MixedArray([Float(4), Float(9)]))

    def test_power_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).power(IntegerArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).power(FloatArray([2, 3])), MixedArray([FloatArray([4, 8]), FloatArray([9, 27])]))

    def test_power_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).power(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Float(4), Float(8)]), MixedArray([Float(9), Float(27)])]))

class DivideTests(TestCase):
    def test_divide_integer_integer(self):
        assert_equal(Integer(1).divide(Integer(2)), Integer(0))
        assert_equal(Integer(1).divide(Integer(0)).type, StorageType.ERROR)

    def test_divide_integer_float(self):
        assert_equal(Integer(1).divide(Float(2)), Float(0.5))
        assert_equal(Integer(1).divide(Float(0)).type, StorageType.ERROR)

    def test_divide_integer_integer_array(self):
        assert_equal(Integer(1).divide(IntegerArray([2, 3])), IntegerArray([0, 0]))
        assert_equal(Integer(1).divide(IntegerArray([0, 3])).type, StorageType.ERROR)

    def test_divide_integer_float_array(self):
        assert_equal(Integer(1).divide(FloatArray([2, 3])), FloatArray([1.0/2.0, 1.0/3.0]))
        assert_equal(Integer(1).divide(FloatArray([0, 3])).type, StorageType.ERROR)

    def test_divide_integer_mixed_array(self):
        assert_equal(Integer(1).divide(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(0), Float(1.0/3.0)]))
        assert_equal(Integer(1).divide(MixedArray([Integer(0), Float(3)])).type, StorageType.ERROR)

    def test_divide_float_integer(self):
        assert_equal(Float(1).divide(Integer(-1)), Float(-1))
        assert_equal(Float(1).divide(Integer(0)).type, StorageType.ERROR)

    def test_divide_float_float(self):
        assert_equal(Float(1).divide(Float(2)), Float(0.5))
        assert_equal(Float(1).divide(Float(0)).type, StorageType.ERROR)

    def test_divide_float_integer_array(self):
        assert_equal(Float(1).divide(IntegerArray([2, 3])), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_divide_float_float_array(self):
        assert_equal(Float(1).divide(FloatArray([2, 3])), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_divide_float_mixed_array(self):
        assert_equal(Float(1).divide(MixedArray([Integer(2), Float(3)])), MixedArray([Float(1.0/2.0), Float(1.0/3.0)]))

    def test_divide_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).divide(Integer(1)), IntegerArray([2, 3]))

    def test_divide_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).divide(Float(1)), FloatArray([2, 3]))

    def test_divide_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).divide(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 0]), IntegerArray([1, 1])]))

    def test_divide_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).divide(FloatArray([2, 3])), MixedArray([FloatArray([1, 2.0/3.0]), FloatArray([3.0/2.0, 1.0])]))

    def test_divide_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).divide(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2.0/3.0)]), MixedArray([Integer(1), Float(1)])]))

    def test_divide_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).divide(Integer(2)), MixedArray([Integer(1), Float(3.0/2.0)]))

    def test_divide_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).divide(Float(2)), MixedArray([Float(1), Float(3.0/2.0)]))

    def test_divide_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).divide(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 0]), FloatArray([3.0/2.0, 1.0])]))

    def test_divide_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).divide(FloatArray([2, 3])), MixedArray([FloatArray([1, 2.0/3.0]), FloatArray([3.0/2.0, 1.0])]))

    def test_divide_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).divide(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2.0/3.0)]), MixedArray([Float(3.0/2.0), Float(1.0)])]))

class NegateTests(TestCase):
    def test_negate_integer(self):
        assert_equal(Integer(1).negate(), Integer(-1))

    def test_negate_float(self):
        assert_equal(Float(1).negate(), Float(-1))

    def test_negate_integer_array(self):
        assert_equal(IntegerArray([2, 3]).negate(), IntegerArray([-2, -3]))

    def test_negate_float_array(self):
        assert_equal(FloatArray([2, 3]).negate(), FloatArray([-2, -3]))

    def test_negate_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).negate(), MixedArray([Integer(-2), Float(-3)]))

class AtomTests(TestCase):
    def test_atom_integer(self):
        assert_equal(Integer(1).atom(), Integer(1))

    def test_atom_float(self):
        assert_equal(Float(1).atom(), Integer(1))

    def test_atom_integer_array(self):
        assert_equal(IntegerArray([2, 3]).atom(), Integer(0))

    def test_atom_float_array(self):
        assert_equal(FloatArray([2, 3]).atom(), Integer(0))

    def test_atom_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).atom(), Integer(0))

class ReciprocalTests(TestCase):
    def test_reciprocal_integer(self):
        assert_equal(Integer(2).reciprocal(), Float(1.0/2.0))

    def test_reciprocal_float(self):
        assert_equal(Float(2).reciprocal(), Float(1.0/2.0))

    def test_reciprocal_integer_array(self):
        assert_equal(IntegerArray([2, 3]).reciprocal(), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_reciprocal_float_array(self):
        assert_equal(FloatArray([2, 3]).reciprocal(), FloatArray([1.0/2.0, 1.0/3.0]))

    def test_reciprocal_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).reciprocal(), MixedArray([Float(1.0/2.0), Float(1.0/3.0)]))

class EnumerateTests(TestCase):
    def test_enumerate(self):
        assert_equal(Integer(5).enumerate(), IntegerArray([1, 2, 3, 4, 5]))

class ComplementationTests(TestCase):
    def test_complementation_integer(self):
        assert_equal(Integer(5).complementation(), Integer(-4))

    def test_complementation_float(self):
        assert_equal(Float(5).complementation(), Float(-4))

    def test_complementation_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).complementation(), IntegerArray([1, 0, -1]))

    def test_complementation_float_array(self):
        assert_equal(FloatArray([0, 1, 2]).complementation(), FloatArray([1, 0, -1]))

    def test_complementation_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(2)]).complementation(), MixedArray([Integer(1), Float(0), Integer(-1)]))

class FloorTests(TestCase):
    def test_floor_integer(self):
        assert_equal(Integer(5).floor(), Integer(5))

    def test_floor_float(self):
        assert_equal(Float(5.5).floor(), Integer(5))

    def test_floor_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).floor(), IntegerArray([0, 1, 2]))

    def test_floor_float_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).floor(), IntegerArray([0, 1, 2]))

    def test_floor_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(2)]).floor(), MixedArray([Integer(0), Integer(1), Integer(2)]))

class CountTests(TestCase):
    def test_count_integer(self):
        assert_equal(Integer(5).count(), Integer(5))
        assert_equal(Integer(-5).count(), Integer(5))

    def test_count_float(self):
        assert_equal(Float(5.5).count(), Float(5.5))
        assert_equal(Float(-5.5).count(), Float(5.5))

    def test_count_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).count(), Integer(3))

    def test_count_float_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).count(), Integer(3))

    def test_count_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(2)]).count(), Integer(3))

class ReverseTests(TestCase):
    def test_reverse_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).reverse(), IntegerArray([2, 1, 0]))

    def test_reverse_float_array(self):
        assert_equal(FloatArray([0, 1, 2]).reverse(), FloatArray([2, 1, 0]))

    def test_reverse_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(2)]).reverse(), MixedArray([Integer(2), Float(1), Integer(0)]))

class FirstTests(TestCase):
    def test_first_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).first(), Integer(0))

    def test_first_float_array(self):
        assert_equal(FloatArray([0, 1, 2]).first(), Float(0))

    def test_first_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(2)]).first(), Integer(0))

class ShapeTests(TestCase):
    def test_shape_integer(self):
        assert_equal(Integer(5).shape(), Integer(0))

    def test_shape_float(self):
        assert_equal(Float(5.5).shape(), Integer(0))

    def test_shape_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).shape(), IntegerArray([3]))

    def test_shape_float_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).shape(), IntegerArray([3]))

    def test_shape_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).shape(), IntegerArray([3]))
        assert_equal(MixedArray([IntegerArray([0]), FloatArray([1]), MixedArray([Integer(0)])]).shape(), IntegerArray([3, 1]))

class RankTests(TestCase):
    def test_shape_integer(self):
        assert_equal(Integer(5).shape().count(), Integer(0))

    def test_shape_float(self):
        assert_equal(Float(5.5).shape().count(), Integer(0))

    def test_shape_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).shape().count(), Integer(1))

    def test_shape_float_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).shape().count(), Integer(1))

    def test_shape_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).shape().count(), Integer(1))
        assert_equal(MixedArray([IntegerArray([0]), FloatArray([1]), MixedArray([Integer(0)])]).shape().count(), Integer(2))

class EncloseTests(TestCase):
    def test_enclose_integer(self):
        assert_equal(Integer(5).enclose(), IntegerArray([5]))

    def test_enclose_float(self):
        assert_equal(Float(5.5).enclose(), FloatArray([5.5]))

    def test_enclose_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).enclose(), MixedArray([IntegerArray([0, 1, 2])]))

    def test_enclose_float_array(self):
        assert_equal(FloatArray([0, 1, 2]).enclose(), MixedArray([FloatArray([0, 1, 2])]))

    def test_enclose_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).enclose(), MixedArray([MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])])]))

class UniqueTests(TestCase):
    def test_unique_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).unique(), IntegerArray([0, 1, 2]))

    def test_unique_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).unique(), FloatArray([0, 1, 2]))

    def test_unique_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).unique(), MixedArray([Integer(0), Float(1), Float(2)]))

class TakeTests(TestCase):
    def test_take_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(2)), IntegerArray([0, 1]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(-2)), IntegerArray([0, 2]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(0)), IntegerArray([]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(9)), IntegerArray([0, 1, 0, 2, 0, 1, 0, 2, 0]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(6)), IntegerArray([0, 1, 0, 2, 0, 1]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Integer(-6)), IntegerArray([0, 2, 0, 1, 0, 2]))
        assert_isinstance(IntegerArray([]).take(Integer(1)), Error)

        assert_equal(IntegerArray([0, 1, 0, 2]).take(Float(0.0)), IntegerArray([]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Float(0.5)), IntegerArray([0, 1]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Float(1.0)), IntegerArray([0, 1, 0, 2]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Float(2.0)), IntegerArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(Float(-2.0)), IntegerArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(IntegerArray([]).take(Float(0.5)), IntegerArray([]))
        assert_equal(IntegerArray([]).take(Float(1)), IntegerArray([]))

        assert_equal(IntegerArray([0, 1, 0, 2]).take(IntegerArray([])), IntegerArray([]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(IntegerArray([1])), MixedArray([IntegerArray([0])]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(IntegerArray([1, 2])), MixedArray([IntegerArray([0]), IntegerArray([0, 1])]))
        assert_isinstance(IntegerArray([]).take(IntegerArray([1, 2])), Error)

        assert_equal(IntegerArray([0, 1, 0, 2]).take(FloatArray([])), IntegerArray([]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(FloatArray([0.25])), MixedArray([IntegerArray([0])]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(FloatArray([0.25, 0.5])), MixedArray([IntegerArray([0]), IntegerArray([0, 1])]))
        assert_equal(IntegerArray([]).take(FloatArray([1, 2])), MixedArray([IntegerArray([]), IntegerArray([])]))

        assert_equal(IntegerArray([0, 1, 0, 2]).take(MixedArray([])), IntegerArray([]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(MixedArray([Integer(1)])), MixedArray([IntegerArray([0])]))
        assert_equal(IntegerArray([0, 1, 0, 2]).take(MixedArray([Integer(1), Float(0.5)])), MixedArray([IntegerArray([0]), IntegerArray([0, 1])]))
        assert_equal(IntegerArray([]).take(MixedArray([Float(1), Float(2)])), MixedArray([IntegerArray([]), IntegerArray([])]))
        assert_isinstance(IntegerArray([]).take(MixedArray([Integer(1), Float(2)])), Error)

    def test_take_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(2)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(-2)), FloatArray([0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(0)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(9)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2, 0]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(6)), FloatArray([0, 1, 0, 2, 0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(-6)), FloatArray([0, 2, 0, 1, 0, 2]))
        assert_isinstance(FloatArray([]).take(Integer(1)), Error)

        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(0.0)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(0.5)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(1.0)), FloatArray([0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(2.0)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Float(-2.0)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2]))
        assert_equal(FloatArray([]).take(Float(0.5)), FloatArray([]))
        assert_equal(FloatArray([]).take(Float(1)), FloatArray([]))

        assert_equal(FloatArray([0, 1, 0, 2]).take(IntegerArray([])), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(IntegerArray([1])), MixedArray([FloatArray([0])]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(IntegerArray([1, 2])), MixedArray([FloatArray([0]), FloatArray([0, 1])]))
        assert_isinstance(FloatArray([]).take(IntegerArray([1, 2])), Error)
        assert_isinstance(FloatArray([]).take(MixedArray([Integer(1), Float(2)])), Error)

    def test_take_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(2)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(-2)), MixedArray([Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(0)), MixedArray([]))
        assert_equal(MixedArray([Float(0), Float(1), Float(0), Float(2)]).take(Integer(9)), MixedArray([Float(0), Float(1), Float(0), Float(2), Float(0), Float(1), Float(0), Float(2), Float(0)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(6)), MixedArray([Integer(0), Float(1), Integer(0), Float(2), Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(-6)), MixedArray([Integer(0), Float(2), Integer(0), Float(1), Integer(0), Float(2)]))
        assert_isinstance(MixedArray([]).take(Integer(1)), Error)

        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Float(0.0)), MixedArray([]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Float(0.5)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Float(1.0)), MixedArray([Integer(0), Float(1), Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Float(2.0)), MixedArray([Integer(0), Float(1), Integer(0), Float(2), Integer(0), Float(1), Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Float(-2.0)), MixedArray([Integer(0), Float(1), Integer(0), Float(2), Integer(0), Float(1), Integer(0), Float(2)]))
        assert_equal(MixedArray([]).take(Float(0.5)), MixedArray([]))
        assert_equal(MixedArray([]).take(Float(1)), MixedArray([]))

        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(IntegerArray([])), MixedArray([]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(IntegerArray([1])), MixedArray([MixedArray([Integer(0)])]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(IntegerArray([1, 2])), MixedArray([MixedArray([Integer(0)]), MixedArray([Integer(0), Float(1)])]))
        assert_isinstance(MixedArray([]).take(IntegerArray([1, 2])), Error)
        assert_isinstance(MixedArray([]).take(MixedArray([Integer(1), Float(2)])), Error)

class DropTests(TestCase):
    def test_drop_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).drop(Integer(2)), IntegerArray([0, 2]))
        assert_equal(IntegerArray([0, 1, 0, 2]).drop(Integer(-2)), IntegerArray([0, 1]))
        assert_equal(IntegerArray([0, 1, 0, 2]).drop(Integer(0)), IntegerArray([0, 1, 0, 2]))
        assert_equal(IntegerArray([0, 1, 0, 2]).drop(Integer(100)), IntegerArray([]))

    def test_drop_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Integer(2)), FloatArray([0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Integer(-2)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Integer(0)), FloatArray([0, 1, 0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).drop(Integer(100)), FloatArray([]))

    def test_drop_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).drop(Integer(2)), MixedArray([Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).drop(Integer(-2)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).drop(Integer(0)), MixedArray([Integer(0), Float(1), Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).drop(Integer(100)), MixedArray([]))

class JoinTests(TestCase):
    def test_join_integer_integer(self):
        assert_equal(Integer(1).join(Integer(2)), IntegerArray([1, 2]))

    def test_join_integer_float(self):
        assert_equal(Integer(1).join(Float(2)), MixedArray([Integer(1), Float(2)]))

    def test_join_integer_integer_array(self):
        assert_equal(Integer(1).join(IntegerArray([2, 3])), IntegerArray([1, 2, 3]))

    def test_join_integer_float_array(self):
        assert_equal(Integer(1).join(FloatArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_integer_mixed_array(self):
        assert_equal(Integer(1).join(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(1), Integer(2), Float(3)]))

    def test_join_float_integer(self):
        assert_equal(Float(1).join(Integer(-1)), MixedArray([Float(1), Integer(-1)]))

    def test_join_float_float(self):
        assert_equal(Float(1).join(Float(2)), FloatArray([1, 2]))

    def test_join_float_integer_array(self):
        assert_equal(Float(1).join(IntegerArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_float_float_array(self):
        assert_equal(Float(1).join(FloatArray([2, 3])), FloatArray([1, 2, 3]))

    def test_join_float_mixed_array(self):
        assert_equal(Float(1).join(MixedArray([Integer(2), Float(3)])), MixedArray([Float(1), Integer(2), Float(3)]))

    def test_join_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).join(Integer(1)), IntegerArray([2, 3, 1]))

    def test_join_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).join(Float(1)), FloatArray([2, 3, 1]))

    def test_join_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).join(IntegerArray([2, 3])), IntegerArray([2, 3, 2, 3]))

    def test_join_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).join(FloatArray([2, 3])), FloatArray([2, 3, 2, 3]))

    def test_join_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).join(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Integer(3), Integer(2), Float(3)]))

    def test_join_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).join(Integer(2)), MixedArray([Integer(2), Float(3), Integer(2)]))

    def test_join_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).join(Float(2)), MixedArray([Integer(2), Float(3), Float(2)]))

    def test_join_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).join(IntegerArray([2, 3])), MixedArray([Integer(2), Float(3), Integer(2), Integer(3)]))

    def test_join_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).join(FloatArray([2, 3])), MixedArray([Integer(2), Float(3), Float(2), Float(3)]))

    def test_join_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).join(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3), Integer(2), Float(3)]))

class RotateTests(TestCase):
    def test_rotate_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).rotate(Integer(1)), IntegerArray([1, 2, 0]))
        assert_equal(IntegerArray([0, 1, 2]).rotate(Integer(-1)), IntegerArray([2, 0, 1]))

    def test_rotate_float_array(self):
        assert_equal(FloatArray([0, 1, 2]).rotate(Integer(1)), FloatArray([1, 2, 0]))
        assert_equal(FloatArray([0, 1, 2]).rotate(Integer(-1)), FloatArray([2, 0, 1]))

    def test_rotate_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).rotate(Integer(1)), MixedArray([Float(1), IntegerArray([1, 2, 3]), Integer(0)]))
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).rotate(Integer(-1)), MixedArray([IntegerArray([1, 2, 3]), Integer(0), Float(1)]))

class SplitTests(TestCase):
    def test_split_integer_integer_array(self):
        assert_equal(Integer(1).split(IntegerArray([2, 3])), MixedArray([IntegerArray([2]), IntegerArray([3])]))

    def test_split_integer_float_array(self):
        assert_equal(Integer(1).split(FloatArray([2, 3])), MixedArray([FloatArray([2]), FloatArray([3])]))

    def test_split_integer_mixed_array(self):
        assert_equal(Integer(1).split(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)])]))

    def test_split_float_integer_array(self):
        assert_equal(Float(0.5).split(IntegerArray([2, 3])), MixedArray([IntegerArray([2]), IntegerArray([3])]))

    def test_split_float_float_array(self):
        assert_equal(Float(0.5).split(FloatArray([2, 3])), MixedArray([FloatArray([2]), FloatArray([3])]))

    def test_split_float_mixed_array(self):
        assert_equal(Float(0.5).split(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)])]))

    def test_split_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).split(Integer(1)), MixedArray([IntegerArray([2]), IntegerArray([3])]))

    def test_split_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).split(Float(0.5)), MixedArray([IntegerArray([2]), IntegerArray([3])]))

    def test_split_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3, 4]).split(IntegerArray([1, 1])), MixedArray([IntegerArray([2]), IntegerArray([3]), IntegerArray([4])]))

    def test_split_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3, 4]).split(FloatArray([0.5, 0.5])),  MixedArray([IntegerArray([2]), IntegerArray([3]), IntegerArray([4])]))

    def test_split_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3, 4]).split(MixedArray([Integer(1), Float(0.5)])),  MixedArray([IntegerArray([2]), IntegerArray([3]), IntegerArray([4])]))

    def test_split_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3), Integer(2)]).split(Integer(1)), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3), Integer(2)])]))

    def test_split_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).split(Float(0.5)), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)])]))

    def test_split_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3), Integer(1)]).split(IntegerArray([1, 1])), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)]), MixedArray([Integer(1)])]))

    def test_split_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3), Integer(1)]).split(FloatArray([0.5, 0.5])), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)]), MixedArray([Integer(1)])]))

    def test_split_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3), Integer(1)]).split(MixedArray([Integer(1), Float(0.5)])),  MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3)]), MixedArray([Integer(1)])]))

class FindTests(TestCase):
    def test_find_integer_integer_array(self):
        assert_equal(Integer(2).find(IntegerArray([1, 2, 3])), IntegerArray([0, 1, 0]))

    def test_find_integer_float_array(self):
        assert_equal(Integer(2).find(FloatArray([1, 2, 3])), IntegerArray([0, 1, 0]))

    def test_find_integer_mixed_array(self):
        assert_equal(Integer(2).find(MixedArray([Integer(1), Integer(2), Float(3)])), IntegerArray([0, 1, 0]))

    def test_find_float_integer_array(self):
        assert_equal(Float(2).find(IntegerArray([1, 2, 3])), IntegerArray([0, 1, 0]))

    def test_find_float_float_array(self):
        assert_equal(Float(2).find(FloatArray([1, 2, 3])), IntegerArray([0, 1, 0]))

    def test_find_float_mixed_array(self):
        assert_equal(Float(3).find(MixedArray([Integer(1), Integer(2), Float(3)])), IntegerArray([0, 0, 1]))

    def test_find_integer_array_integer(self):
        assert_equal(IntegerArray([1, 2, 3]).find(Integer(2)), IntegerArray([0, 1, 0]))

    def test_find_integer_array_float(self):
        assert_equal(IntegerArray([1, 2, 3]).find(Float(2)), IntegerArray([0, 1, 0]))

    def test_find_integer_array_integer_array(self):
        assert_equal(IntegerArray([1, 2, 3]).find(IntegerArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_integer_array_float_array(self):
        assert_equal(IntegerArray([1, 2, 3]).find(FloatArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_integer_array_mixed_array(self):
        assert_equal(IntegerArray([1, 2, 3]).find(MixedArray([Integer(2), Integer(3)])), IntegerArray([0, 1, 0]))

    def test_find_float_array_integer(self):
        assert_equal(FloatArray([1, 2, 3]).find(Integer(2)), IntegerArray([0, 1, 0]))

    def test_find_float_array_float(self):
        assert_equal(FloatArray([1, 2, 3]).find(Float(2)), IntegerArray([0, 1, 0]))

    def test_find_float_array_integer_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(IntegerArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_float_array_float_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(FloatArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_float_array_mixed_array(self):
        assert_equal(FloatArray([1, 2, 3]).find(MixedArray([Float(2), Float(3)])), IntegerArray([0, 1, 0]))

    def test_find_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(1), Integer(2), Integer(3)]).find(Integer(2)), IntegerArray([0, 1, 0]))

    def test_find_mixed_array_float(self):
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).find(Float(2)), IntegerArray([0, 1, 0]))

    def test_find_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(1), Integer(2), Integer(3)]).find(IntegerArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_mixed_array_float_array(self):
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).find(FloatArray([2, 3])), IntegerArray([0, 1, 0]))

    def test_find_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(1), Integer(2), Float(3)]).find(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 1, 0]))

class RemainderTests(TestCase):
    def test_remainder_integer_integer(self):
        assert_equal(Integer(10).remainder(Integer(2)), Integer(0))

    def test_remainder_integer_integer_array(self):
        assert_equal(Integer(10).remainder(IntegerArray([2, 3])), IntegerArray([0, 1]))

    def test_remainder_integer_mixed_array(self):
        assert_equal(Integer(10).remainder(MixedArray([Integer(2), Integer(3)])), MixedArray([Integer(0), Integer(1)]))

    def test_remainder_integer_array_integer(self):
        assert_equal(IntegerArray([10, 9]).remainder(Integer(2)), IntegerArray([0, 1]))

    def test_remainder_integer_array_integer_array(self):
        assert_equal(IntegerArray([10, 9]).remainder(IntegerArray([2, 3])), MixedArray([IntegerArray([0, 1]), IntegerArray([1, 0])]))

    def test_remainder_integer_array_mixed_array(self):
        assert_equal(IntegerArray([10, 9]).remainder(MixedArray([Integer(2), Integer(3)])), MixedArray([MixedArray([Integer(0), Integer(1)]), MixedArray([Integer(1), Integer(0)])]))

    def test_remainder_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(10), Integer(9)]).remainder(Integer(2)), MixedArray([Integer(0), Integer(1)]))

    def test_remainder_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(10), Integer(9)]).remainder(IntegerArray([2, 3])), MixedArray([IntegerArray([0, 1]), IntegerArray([1, 0])]))

    def test_remainder_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(10), Integer(9)]).remainder(MixedArray([Integer(2), Integer(3)])), MixedArray([MixedArray([Integer(0), Integer(1)]), MixedArray([Integer(1), Integer(0)])]))

class MatchTests(TestCase):
    def test_match_integer_integer(self):
        assert_equal(Integer(10).match(Integer(10)), Integer(1))

    def test_match_integer_float(self):
        assert_equal(Integer(10).match(Float(10)), Integer(1))

    def test_match_integer_integer_array(self):
        assert_equal(Integer(10).match(IntegerArray([2, 3])), Integer(0))

    def test_match_integer_float_array(self):
        assert_equal(Integer(10).match(FloatArray([2, 3])), Integer(0))

    def test_match_integer_mixed_array(self):
        assert_equal(Integer(10).match(MixedArray([Integer(2), Integer(3)])), Integer(0))

    def test_match_integer_array_integer(self):
        assert_equal(IntegerArray([1, 2, 3]).match(Integer(2)), Integer(0))

    def test_match_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).match(IntegerArray([2, 3])), Integer(1))

    def test_match_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).match(MixedArray([Integer(2), Integer(3)])), Integer(1))

    def test_match_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).match(Integer(2)), Integer(0))

    def test_match_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).match(IntegerArray([1, 2, 3])), Integer(1))

    def test_match_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).match(MixedArray([Float(1), Integer(2), Float(3)])), Integer(1))

class MaxTests(TestCase):
    def test_max_integer_integer(self):
        assert_equal(Integer(1).max(Integer(2)), Integer(2))

    def test_max_integer_float(self):
        assert_equal(Integer(1).max(Float(2)), Float(2))

    def test_max_integer_integer_array(self):
        assert_equal(Integer(1).max(IntegerArray([2, 3])), IntegerArray([2, 3]))

    def test_max_integer_float_array(self):
        assert_equal(Integer(1).max(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_max_integer_mixed_array(self):
        assert_equal(Integer(1).max(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3)]))

    def test_max_float_integer(self):
        assert_equal(Float(1).max(Integer(-1)), Float(1))

    def test_max_float_float(self):
        assert_equal(Float(1).max(Float(2)), Float(2))

    def test_max_float_integer_array(self):
        assert_equal(Float(1).max(IntegerArray([2, 3])), FloatArray([2, 3]))

    def test_max_float_float_array(self):
        assert_equal(Float(1).max(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_max_float_mixed_array(self):
        assert_equal(Float(1).max(MixedArray([Integer(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_max_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).max(Integer(1)), IntegerArray([2, 3]))

    def test_max_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).max(Float(1)), FloatArray([2, 3]))

    def test_max_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).max(IntegerArray([2, 3])), IntegerArray([3, 3]))

    def test_max_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).max(FloatArray([2, 3])), FloatArray([3, 3]))

    def test_max_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).max(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(3)]))

    def test_max_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).max(Integer(1)), FloatArray([2, 3]))

    def test_max_float_array_float(self):
        assert_equal(FloatArray([2, 3]).max(Float(1)), FloatArray([2, 3]))

    def test_max_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).max(IntegerArray([2, 3])), FloatArray([3, 3]))

    def test_max_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).max(FloatArray([2, 3])), FloatArray([3, 3]))

    def test_max_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).max(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(Integer(3)), MixedArray([Integer(3), Float(3)]))

    def test_max_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(Float(3)), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(IntegerArray([2, 3])), MixedArray([Integer(3), Float(3)]))

    def test_max_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(FloatArray([2, 3])), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(3)]))

class MinTests(TestCase):
    def test_min_integer_integer(self):
        assert_equal(Integer(1).min(Integer(2)), Integer(1))
        assert_equal(Integer(4).min(Integer(1)), Integer(1))

    def test_min_integer_float(self):
        assert_equal(Integer(1).min(Float(2)), Float(1))
        assert_equal(Integer(2).min(Float(1)), Float(1))

    def test_min_integer_integer_array(self):
        assert_equal(Integer(1).min(IntegerArray([2, 3])), IntegerArray([1, 1]))
        assert_equal(Integer(4).min(IntegerArray([2, 3])), IntegerArray([2, 3]))

    def test_min_integer_float_array(self):
        assert_equal(Integer(1).min(FloatArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Integer(4).min(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_min_integer_mixed_array(self):
        assert_equal(Integer(1).min(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(1), Float(1)]))
        assert_equal(Integer(4).min(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3)]))

    def test_min_float_integer(self):
        assert_equal(Float(1).min(Integer(-1)), Float(-1))
        assert_equal(Float(1).min(Integer(4)), Float(1))

    def test_min_float_float(self):
        assert_equal(Float(1).min(Float(2)), Float(1))
        assert_equal(Float(2).min(Float(1)), Float(1))

    def test_min_float_integer_array(self):
        assert_equal(Float(1).min(IntegerArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Float(4).min(IntegerArray([2, 3])), FloatArray([2, 3]))

    def test_min_float_float_array(self):
        assert_equal(Float(1).min(FloatArray([2, 3])), FloatArray([1, 1]))
        assert_equal(Float(4).min(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_min_float_mixed_array(self):
        assert_equal(Float(1).min(MixedArray([Integer(2), Float(3)])), MixedArray([Float(1), Float(1)]))
        assert_equal(Float(4).min(MixedArray([Integer(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_min_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).min(Integer(1)), IntegerArray([1, 1]))
        assert_equal(IntegerArray([2, 3]).min(Integer(4)), IntegerArray([2, 3]))

    def test_min_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).min(Float(1)), FloatArray([1, 1]))
        assert_equal(IntegerArray([2, 3]).min(Float(4)), FloatArray([2, 3]))

    def test_min_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).min(IntegerArray([1, 1])), IntegerArray([1, 1]))
        assert_equal(IntegerArray([2, 3]).min(IntegerArray([4, 4])), IntegerArray([2, 3]))
        assert_isinstance(IntegerArray([2, 3]).min(IntegerArray([4, 4, 4])), Error)

    def test_min_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).min(FloatArray([1, 1])), FloatArray([1, 1]))
        assert_equal(IntegerArray([2, 3]).min(FloatArray([4, 4])), FloatArray([2, 3]))
        assert_isinstance(IntegerArray([2, 3]).min(FloatArray([4, 4, 4])), Error)

    def test_min_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).min(MixedArray([Integer(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(IntegerArray([2, 3]).min(MixedArray([Integer(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_isinstance(IntegerArray([2, 3]).min(MixedArray([Integer(4), Integer(4), Integer(4)])), Error)

    def test_min_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).min(Integer(1)), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(Integer(4)), FloatArray([2, 3]))

    def test_min_float_array_float(self):
        assert_equal(FloatArray([2, 3]).min(Float(1)), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(Float(4)), FloatArray([2, 3]))

    def test_min_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).min(IntegerArray([1, 1])), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(IntegerArray([4, 4])), FloatArray([2, 3]))
        assert_isinstance(FloatArray([2, 3]).min(IntegerArray([4, 4, 4])), Error)

    def test_min_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).min(FloatArray([1, 1])), FloatArray([1, 1]))
        assert_equal(FloatArray([2, 3]).min(FloatArray([4, 4])), FloatArray([2, 3]))
        assert_isinstance(FloatArray([2, 3]).min(FloatArray([4, 4, 4])), Error)

    def test_min_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).min(MixedArray([Integer(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(FloatArray([2, 3]).min(MixedArray([Integer(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_isinstance(FloatArray([2, 3]).min(MixedArray([Integer(4), Integer(4), Integer(4)])), Error)

    def test_min_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Integer(1)), MixedArray([Integer(1), Float(1)]))
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Integer(4)), MixedArray([Integer(2), Float(3)]))

    def test_min_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Float(1)), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Float(4)), MixedArray([Float(2), Float(3)]))

    def test_min_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(IntegerArray([1, 1])), MixedArray([Integer(1), Float(1)]))
        assert_equal(MixedArray([Integer(2), Float(3)]).min(IntegerArray([4, 4])), MixedArray([Integer(2), Float(3)]))
        assert_isinstance(MixedArray([Integer(2), Integer(3)]).min(IntegerArray([4, 4, 4])), Error)

    def test_min_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(FloatArray([1, 1])), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Integer(2), Float(3)]).min(FloatArray([4, 4])), MixedArray([Float(2), Float(3)]))
        assert_isinstance(MixedArray([Integer(2), Integer(3)]).min(FloatArray([4, 4, 4])), Error)

    def test_min_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(MixedArray([Integer(1), Float(1)])), MixedArray([Float(1), Float(1)]))
        assert_equal(MixedArray([Integer(2), Float(3)]).min(MixedArray([Integer(4), Float(4)])), MixedArray([Float(2), Float(3)]))
        assert_isinstance(MixedArray([Integer(2), Integer(3)]).min(MixedArray([Integer(4), Integer(4), Integer(4)])), Error)

class LessTests(TestCase):
    def test_less_integer_integer(self):
        assert_equal(Integer(1).less(Integer(2)), Integer(1))

    def test_less_integer_float(self):
        assert_equal(Integer(1).less(Float(2)), Integer(1))

    def test_less_integer_integer_array(self):
        assert_equal(Integer(1).less(IntegerArray([2, 3])), Integer(1))

    def test_less_integer_float_array(self):
        assert_equal(Integer(1).less(FloatArray([2, 3])), Integer(1))

    def test_less_integer_mixed_array(self):
        assert_equal(Integer(1).less(MixedArray([Integer(2), Float(3)])), Integer(1))

    def test_less_float_integer(self):
        assert_equal(Float(1).less(Integer(-1)), Integer(0))

    def test_less_float_float(self):
        assert_equal(Float(1).less(Float(2)), Integer(1))

    def test_less_float_integer_array(self):
        assert_equal(Float(1).less(IntegerArray([2, 3])), Integer(1))

    def test_less_float_float_array(self):
        assert_equal(Float(1).less(FloatArray([2, 3])), Integer(1))
    def test_less_float_mixed_array(self):
        assert_equal(Float(1).less(MixedArray([Integer(2), Float(3)])), Integer(1))

    def test_less_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).less(Integer(1)), IntegerArray([0, 0]))

    def test_less_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).less(Float(1)), IntegerArray([0, 0]))

    def test_less_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).less(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_less_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).less(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_less_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).less(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 0]))

    def test_less_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).less(Integer(1)), IntegerArray([0, 0]))

    def test_less_float_array_float(self):
        assert_equal(FloatArray([2, 3]).less(Float(1)), IntegerArray([0, 0]))

    def test_less_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).less(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_less_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).less(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_less_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).less(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 0]))

    def test_less_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).less(Integer(3)), IntegerArray([1, 0]))

    def test_less_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).less(Float(3)), IntegerArray([1, 0]))

    def test_less_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).less(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_less_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).less(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_less_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).less(MixedArray([Integer(2), Float(2)])), IntegerArray([0, 0]))

class MoreTests(TestCase):
    def test_more_integer_integer(self):
        assert_equal(Integer(1).more(Integer(2)), Integer(0))

    def test_more_integer_float(self):
        assert_equal(Integer(1).more(Float(2)), Integer(0))

    def test_more_integer_integer_array(self):
        assert_equal(Integer(1).more(IntegerArray([2, 3])), Integer(0))

    def test_more_integer_float_array(self):
        assert_equal(Integer(1).more(FloatArray([2, 3])), Integer(0))

    def test_more_integer_mixed_array(self):
        assert_equal(Integer(1).more(MixedArray([Integer(2), Float(3)])), Integer(0))

    def test_more_float_integer(self):
        assert_equal(Float(1).more(Integer(-1)), Integer(1))

    def test_more_float_float(self):
        assert_equal(Float(1).more(Float(2)), Integer(0))

    def test_more_float_integer_array(self):
        assert_equal(Float(1).more(IntegerArray([2, 3])), Integer(0))

    def test_more_float_float_array(self):
        assert_equal(Float(1).more(FloatArray([2, 3])), Integer(0))

    def test_more_float_mixed_array(self):
        assert_equal(Float(1).more(MixedArray([Integer(2), Float(3)])), Integer(0))

    def test_more_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).more(Integer(1)), IntegerArray([1, 1]))

    def test_more_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).more(Float(1)), IntegerArray([1, 1]))

    def test_more_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).more(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_more_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).more(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_more_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).more(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 0]))

    def test_more_float_array_integer(self):
        assert_equal(FloatArray([2, 3]).more(Integer(1)), IntegerArray([1, 1]))

    def test_more_float_array_float(self):
        assert_equal(FloatArray([2, 3]).more(Float(1)), IntegerArray([1, 1]))

    def test_more_float_array_integer_array(self):
        assert_equal(FloatArray([2, 3]).more(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_more_float_array_float_array(self):
        assert_equal(FloatArray([2, 3]).more(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_more_float_array_mixed_array(self):
        assert_equal(FloatArray([2, 3]).more(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 0]))

    def test_more_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).more(Integer(3)), IntegerArray([0, 0]))

    def test_more_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).more(Float(3)), IntegerArray([0, 0]))

    def test_more_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).more(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_more_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).more(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_more_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).more(MixedArray([Integer(2), Float(2)])), IntegerArray([0, 1]))

class EqualTests(TestCase):
    def test_equal_integer_integer(self):
        assert_equal(Integer(1).equal(Integer(2)), Integer(0))

    def test_equal_integer_float(self):
        assert_equal(Integer(1).equal(Float(2)), Integer(0))

    def test_equal_integer_integer_array(self):
        assert_equal(Integer(1).equal(IntegerArray([2, 3])), Integer(0))

    def test_equal_integer_float_array(self):
        assert_equal(Integer(1).equal(FloatArray([2, 3])), Integer(0))

    def test_equal_integer_mixed_array(self):
        assert_equal(Integer(1).equal(MixedArray([Integer(2), Float(3)])), Integer(0))

    def test_equal_float_integer(self):
        assert_equal(Float(1).equal(Integer(-1)), Integer(0))

    def test_equal_float_float(self):
        assert_equal(Float(1).equal(Float(2)), Integer(0))

    def test_equal_float_integer_array(self):
        assert_equal(Float(1).equal(IntegerArray([2, 3])), Integer(0))

    def test_equal_float_float_array(self):
        assert_equal(Float(1).equal(FloatArray([2, 3])), Integer(0))
    def test_equal_float_mixed_array(self):
        assert_equal(Float(1).equal(MixedArray([Integer(2), Float(3)])), Integer(0))

    def test_equal_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).equal(Integer(1)), IntegerArray([0, 0]))

    def test_equal_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).equal(Float(1)), IntegerArray([0, 0]))

    def test_equal_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).equal(IntegerArray([2, 3])), IntegerArray([1, 1]))

    def test_equal_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).equal(FloatArray([2, 3])), IntegerArray([1, 1]))

    def test_equal_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).equal(MixedArray([Integer(2), Float(3)])), IntegerArray([1, 1]))

    def test_equal_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).equal(Integer(3)), IntegerArray([0, 1]))

    def test_equal_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).equal(Float(3)), IntegerArray([0, 1]))

    def test_equal_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).equal(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_equal_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).equal(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_equal_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).equal(MixedArray([Integer(2), Float(2)])), IntegerArray([1, 0]))

class IndexTests(TestCase):
    def test_index_integer_integer_array(self):
        assert_equal(Integer(1).index(IntegerArray([2, 3])), Integer(2))

    def test_index_integer_float_array(self):
        assert_equal(Integer(1).index(FloatArray([2, 3])), Float(2))

    def test_index_integer_mixed_array(self):
        assert_equal(Integer(1).index(MixedArray([Integer(2), Float(3)])), Integer(2))

    def test_index_float_integer_array(self):
        assert_equal(Float(0.5).index(IntegerArray([2, 3])), Integer(2))

    def test_index_float_float_array(self):
        assert_equal(Float(0.5).index(FloatArray([2, 3])), Float(2))

    def test_index_float_mixed_array(self):
        assert_equal(Float(0.5).index(MixedArray([Integer(2), Float(3)])), Integer(2))

    def test_index_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).index(Integer(1)), Integer(2))

    def test_index_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).index(Float(0.5)), Integer(2))

    def test_index_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).index(IntegerArray([1, 2])), IntegerArray([2, 3]))

    def test_index_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).index(FloatArray([0.5, 1.0])), IntegerArray([2, 3]))

    def test_index_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).index(MixedArray([Integer(1), Float(1.0)])), IntegerArray([2, 3]))

    def test_index_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).index(Integer(1)), Integer(2))

    def test_index_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).index(Float(0.5)), Integer(2))

    def test_index_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).index(IntegerArray([1, 2])), MixedArray([Integer(2), Float(3)]))

    def test_index_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).index(FloatArray([0.5, 1.0])), MixedArray([Integer(2), Float(3)]))

    def test_index_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).index(MixedArray([Integer(1), Float(1.0)])), MixedArray([Integer(2), Float(3)]))

class CutTests(TestCase):
    def test_cut_integer_integer_array(self):
        assert_equal(Integer(1).cut(IntegerArray([2, 3])), IntegerArray([3]))

    def test_cut_integer_float_array(self):
        assert_equal(Integer(1).cut(FloatArray([2, 3])), FloatArray([3]))

    def test_cut_integer_mixed_array(self):
        assert_equal(Integer(1).cut(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3)]))

    def test_cut_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).cut(Integer(1)), IntegerArray([3]))

    def test_cut_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).cut(IntegerArray([1, 2])), MixedArray([IntegerArray([2])]))

    def test_cut_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).cut(MixedArray([Integer(1), Integer(2)])), MixedArray([IntegerArray([3])]))

    def test_cut_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).cut(Integer(1)), MixedArray([Float(3)]))

    def test_cut_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).cut(IntegerArray([1, 2])), MixedArray([MixedArray([]), MixedArray([Integer(2)]), MixedArray([Float(3)])]))

    def test_cut_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).cut(MixedArray([Integer(1), Integer(2)])), MixedArray([MixedArray([]), MixedArray([Integer(2)]), MixedArray([Float(3)])]))

class GradeUpTests(TestCase):
    def test_gradeUp_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).gradeUp(), IntegerArray([1, 3, 2, 4]))

    def test_gradeUp_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).gradeUp(), IntegerArray([1, 3, 2, 4]))

    def test_gradeUp_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).gradeUp(), IntegerArray([1, 3, 2, 4]))

class GradeDownTests(TestCase):
    def test_gradeDown_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).gradeDown(), IntegerArray([4, 2, 3, 1]))

    def test_gradeDown_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).gradeDown(), IntegerArray([4, 2, 3, 1]))

    def test_gradeDown_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).gradeDown(), IntegerArray([4, 2, 3, 1]))

class ReplicatedTests(TestCase):
    def test_replicate_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).replicate(IntegerArray([0, 1, 2, 3])), IntegerArray([1, 0, 0, 2, 2, 2]))

    def test_replicate_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).replicate(IntegerArray([0, 1, 2, 3])), FloatArray([1, 0, 0, 2, 2, 2]))

    def test_replicate_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).replicate(IntegerArray([0, 1, 2, 3])), MixedArray([Float(1), Integer(0), Integer(0), Float(2), Float(2), Float(2)]))

class TransposeTests(TestCase):
    def test_transpose_mixed_array(self):
        assert_equal(MixedArray([IntegerArray([1, 2]), IntegerArray([3, 4])]).transpose(), MixedArray([IntegerArray([1, 3]), IntegerArray([2, 4])]))

class GroupTests(TestCase):
    def test_group_integer_array(self):
        assert_equal(IntegerArray([0, 1, 0, 2]).group(), Dictionary(IntegerArray([0, 1, 2]), MixedArray([IntegerArray([1, 3]), IntegerArray([2]), IntegerArray([4])])))

    def test_group_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).group(), Dictionary(IntegerArray([0, 1, 2]), MixedArray([IntegerArray([1, 3]), IntegerArray([2]), IntegerArray([4])])))

    def test_group_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).group(), Dictionary(MixedArray([Integer(0), Float(1), Float(2)]), MixedArray([IntegerArray([1, 3]), IntegerArray([2]), IntegerArray([4])])))

class DictionaryTests(TestCase):
    def test_dictionary_get(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).get(Integer(1)), Integer(4))

    def test_dictionary_put(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).put(Integer(1), Integer(6)), Dictionary(IntegerArray([1, 2, 3]), IntegerArray([6, 5, 6])))

    def test_dictionary_contains(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).contains(Integer(1)), Integer(1))
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).contains(Integer(7)), Integer(0))

    def test_dictionary_remove(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).remove(Integer(1)), Dictionary(IntegerArray([2, 3]), IntegerArray([5, 6])))

    def test_dictionary_keys(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).keys(), IntegerArray([1, 2, 3]))

    def test_dictionary_values(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).values(), IntegerArray([4, 5, 6]))

    def test_dictionary_items(self):
        assert_equal(Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])).items(), MixedArray([IntegerArray([1, 4]), IntegerArray([2, 5]), IntegerArray([3, 6])]))

    def test_amend_integer_integer(self):
        assert_equal(Integer(1).amend(Integer(4)), Dictionary(IntegerArray([1]), IntegerArray([4])))

    def test_amend_integer_float(self):
        assert_equal(Integer(1).amend(Float(4)), Dictionary(IntegerArray([1]), FloatArray([4])))

    def test_amend_float_integer(self):
        assert_equal(Float(1).amend(Integer(4)), Dictionary(FloatArray([1]), IntegerArray([4])))

    def test_amend_float_float(self):
        assert_equal(Float(1).amend(Float(4)), Dictionary(FloatArray([1]), FloatArray([4])))

    def test_amend_integer_array_integer_array(self):
        assert_equal(IntegerArray([1, 2, 3]).amend(IntegerArray([4, 5, 6])), Dictionary(IntegerArray([1, 2, 3]), IntegerArray([4, 5, 6])))

    def test_amend_integer_array_float_array(self):
        assert_equal(IntegerArray([1, 2, 3]).amend(FloatArray([4, 5, 6])), Dictionary(IntegerArray([1, 2, 3]), FloatArray([4, 5, 6])))

    def test_amend_integer_array_mixed_array(self):
        assert_equal(IntegerArray([1, 2, 3]).amend(MixedArray([Integer(4), Float(5), Integer(6)])), Dictionary(IntegerArray([1, 2, 3]), MixedArray([Integer(4), Float(5), Integer(6)])))

    def test_amend_float_array_integer_array(self):
        assert_equal(FloatArray([1, 2, 3]).amend(IntegerArray([4, 5, 6])), Dictionary(FloatArray([1, 2, 3]), IntegerArray([4, 5, 6])))

    def test_amend_float_array_float_array(self):
        assert_equal(FloatArray([1, 2, 3]).amend(FloatArray([4, 5, 6])), Dictionary(FloatArray([1, 2, 3]), FloatArray([4, 5, 6])))

    def test_amend_float_array_mixed_array(self):
        assert_equal(FloatArray([1, 2, 3]).amend(MixedArray([Integer(4), Float(5), Integer(6)])), Dictionary(FloatArray([1, 2, 3]), MixedArray([Integer(4), Float(5), Integer(6)])))

    def test_amend_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).amend(IntegerArray([4, 5, 6])), Dictionary(MixedArray([Integer(1), Float(2), Integer(3)]), IntegerArray([4, 5, 6])))

    def test_amend_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).amend(FloatArray([4, 5, 6])), Dictionary(MixedArray([Integer(1), Float(2), Integer(3)]), FloatArray([4, 5, 6])))

    def test_amend_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).amend(MixedArray([Integer(4), Float(5), Integer(6)])), Dictionary(MixedArray([Integer(1), Float(2), Integer(3)]), MixedArray([Integer(4), Float(5), Integer(6)])))

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
    def test_serialization_to_bytes_integer(self):
        assert_equal(Integer(0).to_bytes(), b"\x01\x02\x00\x00")
        assert_equal(Integer(1).to_bytes(), b"\x01\x03\x00\x01\x01")
        assert_equal(Integer(256).to_bytes(), b"\x01\x04\x00\x02\x01\x00")
        assert_equal(Integer(-256).to_bytes(), b"\x01\x04\x00\xfe\xff\x00")

    def test_serialization_to_bytes_float(self):
        assert_equal(Float(0).to_bytes(),b'\x01\x05\x01\x00\x00\x00\x00')
        assert_equal(Float(1).to_bytes(),b'\x01\x05\x01\x00\x00\x80?')
        assert_equal(Float(256).to_bytes(), b'\x01\x05\x01\x00\x00\x80C')
        assert_equal(Float(-256).to_bytes(), b'\x01\x05\x01\x00\x00\x80\xc3')

    def test_serialization_from_bytes_integer(self):
        assert_equal(Storage.from_bytes(Integer(0).to_bytes()), (Integer(0), b''))
        assert_equal(Storage.from_bytes(Integer(1).to_bytes()), (Integer(1), b''))
        assert_equal(Storage.from_bytes(Integer(256).to_bytes()), (Integer(256), b''))
        assert_equal(Storage.from_bytes(Integer(-256).to_bytes()), (Integer(-256), b''))

    def test_serialization_from_bytes_float(self):
        assert_equal(Storage.from_bytes(Float(0).to_bytes()), (Float(0), b''))
        assert_equal(Storage.from_bytes(Float(1).to_bytes()), (Float(1), b''))
        assert_equal(Storage.from_bytes(Float(256).to_bytes()), (Float(256), b''))
        assert_equal(Storage.from_bytes(Float(-256).to_bytes()), (Float(-256), b''))

    def test_serialization_to_bytes_integer_array(self):
        assert_equal(IntegerArray([]).to_bytes(), b'\x01\x01\x02')
        assert_equal(IntegerArray([1]).to_bytes(), b'\x01\x03\x02\x01\x01')
        assert_equal(IntegerArray([1, 2, 3]).to_bytes(), b'\x01\x07\x02\x01\x01\x01\x02\x01\x03')
        assert_equal(IntegerArray([1, 2, 3, 4]).to_bytes(), b'\x01\t\x02\x01\x01\x01\x02\x01\x03\x01\x04')

    def test_serialization_from_bytes_integer_array(self):
        assert_equal(Storage.from_bytes(IntegerArray([]).to_bytes()), (IntegerArray([]), b''))
        assert_equal(Storage.from_bytes(IntegerArray([1]).to_bytes()), (IntegerArray([1]), b''))
        assert_equal(Storage.from_bytes(IntegerArray([1, 2, 3]).to_bytes()), (IntegerArray([1, 2, 3]), b''))
        assert_equal(Storage.from_bytes(IntegerArray([1, 2, 3, 4]).to_bytes()), (IntegerArray([1, 2, 3, 4]), b''))

    def test_serialization_to_bytes_float_array(self):
        assert_equal(FloatArray([]).to_bytes(),  b'\x01\x01\x03')
        assert_equal(FloatArray([1]).to_bytes(), b'\x01\x05\x03\x00\x00\x80?')
        assert_equal(FloatArray([1, 2, 3]).to_bytes(), b'\x01\r\x03\x00\x00\x80?\x00\x00\x00@\x00\x00@@')
        assert_equal(FloatArray([1, 2, 3, 4]).to_bytes(),  b'\x01\x11\x03\x00\x00\x80?\x00\x00\x00@\x00\x00@@\x00\x00\x80@')

    def test_serialization_from_bytes_float_array(self):
        assert_equal(Storage.from_bytes(FloatArray([]).to_bytes()), (FloatArray([]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1]).to_bytes()), (FloatArray([1]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1, 2, 3]).to_bytes()), (FloatArray([1, 2, 3]), b''))
        assert_equal(Storage.from_bytes(FloatArray([1, 2, 3, 4]).to_bytes()), (FloatArray([1, 2, 3, 4]), b''))

    def test_serialization_to_bytes_mixed_array(self):
        assert_equal(MixedArray([]).to_bytes(),b'\x01\x01\x04')
        assert_equal(MixedArray([Integer(1)]).to_bytes(),b'\x01\x06\x04\x01\x03\x00\x01\x01')
        assert_equal(MixedArray([Integer(1), Float(2), IntegerArray([3])]).to_bytes(),b'\x01\x12\x04\x01\x03\x00\x01\x01\x01\x05\x01\x00\x00\x00@\x01\x03\x02\x01\x03')
        assert_equal(MixedArray([IntegerArray([1, 2]), FloatArray([3]), MixedArray([Integer(4)])]).to_bytes(),  b'\x01\x17\x04\x01\x05\x02\x01\x01\x01\x02\x01\x05\x03\x00\x00@@\x01\x06\x04\x01\x03\x00\x01\x04')

    def test_serialization_from_bytes_mixed_array(self):
        assert_equal(Storage.from_bytes(MixedArray([]).to_bytes()),  (MixedArray([]), b''))
        assert_equal(Storage.from_bytes(MixedArray([Integer(1)]).to_bytes()), (MixedArray([Integer(1)]), b''))
        assert_equal(Storage.from_bytes(MixedArray([Integer(1), Float(2), IntegerArray([3])]).to_bytes()), (MixedArray([Integer(1), Float(2), IntegerArray([3])]), b''))
        assert_equal(Storage.from_bytes(MixedArray([IntegerArray([1, 2]), FloatArray([3]), MixedArray([Integer(4)])]).to_bytes()),  (MixedArray([IntegerArray([1, 2]), FloatArray([3]), MixedArray([Integer(4)])]), b''))

class AdverbTests(TestCase):
    def test_each(self):
        assert_equal(IntegerArray([1, 2, 3]).each(Integer(StorageMonads.negate.value)), MixedArray([Integer(-1), Integer(-2), Integer(-3)]))
        assert_equal(FloatArray([1, 2, 3]).each(Integer(StorageMonads.negate.value)), MixedArray([Float(-1), Float(-2), Float(-3)]))
        assert_equal(MixedArray([Integer(1), Integer(2), Integer(3)]).each(Integer(StorageMonads.negate.value)), MixedArray([Integer(-1), Integer(-2), Integer(-3)]))

    def test_each2(self):
        assert_equal(IntegerArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), Integer(4)), MixedArray([Integer(5), Integer(6), Integer(7)]))
        assert_equal(IntegerArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(IntegerArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([Integer(5), Integer(7), Integer(9)]))
        assert_equal(IntegerArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(IntegerArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Integer(5), Integer(7), Integer(9)]))

        assert_equal(FloatArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), Integer(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([Integer(5), Integer(7), Integer(9)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(FloatArray([1, 2, 3]).each2(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Integer(5), Integer(7), Integer(9)]))

        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).each2(Integer(StorageDyads.plus.value), Integer(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Float(1), Float(2), Float(3)]).each2(Integer(StorageDyads.plus.value), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).each2(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([Integer(5), Float(7), Integer(9)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).each2(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(7), Float(9)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).each2(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Integer(5), Float(7), Integer(9)]))

    def test_eachLeft(self):
        assert_equal(Integer(1).eachLeft(Integer(StorageDyads.plus.value), Integer(4)), Integer(5))
        assert_equal(Integer(1).eachLeft(Integer(StorageDyads.plus.value), Float(4)), Float(5))
        assert_equal(Integer(1).eachLeft(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), IntegerArray([5, 6, 7]))
        assert_equal(Integer(1).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Integer(1).eachLeft(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Integer(5), Integer(6), Integer(7)]))

        assert_equal(Float(1).eachLeft(Integer(StorageDyads.plus.value), Integer(4)), Float(5))
        assert_equal(Float(1).eachLeft(Integer(StorageDyads.plus.value), Float(4)), Float(5))
        assert_equal(Float(1).eachLeft(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(Float(1).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(Float(1).eachLeft(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(IntegerArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([IntegerArray([5, 6, 7]), IntegerArray([6, 7, 8]), IntegerArray([7, 8, 9])]))
        assert_equal(IntegerArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(IntegerArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(FloatArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), Integer(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachLeft(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachLeft(Integer(StorageDyads.plus.value), Integer(4)), MixedArray([Integer(5), Float(6), Integer(7)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachLeft(Integer(StorageDyads.plus.value), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachLeft(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([MixedArray([Integer(5), Float(6), Integer(7)]), MixedArray([Integer(6), Float(7), Integer(8)]), MixedArray([Integer(7), Float(8), Integer(9)])]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachLeft(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([MixedArray([Float(5), Float(6), Float(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Float(7), Float(8), Float(9)])]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachLeft(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([MixedArray([Integer(5), Float(6), Integer(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Integer(7), Float(8), Integer(9)])]))

    def test_eachRight(self):
        assert_equal(Integer(1).eachRight(Integer(StorageDyads.plus.value), Integer(4)), Integer(5))
        assert_equal(Integer(1).eachRight(Integer(StorageDyads.plus.value), Float(4)), Float(5))
        assert_equal(Integer(1).eachRight(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), IntegerArray([5, 6, 7]))
        assert_equal(Integer(1).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Integer(1).eachRight(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Integer(5), Integer(6), Integer(7)]))

        assert_equal(Float(1).eachRight(Integer(StorageDyads.plus.value), Integer(4)), Float(5))
        assert_equal(Float(1).eachRight(Integer(StorageDyads.plus.value), Float(4)), Float(5))
        assert_equal(Float(1).eachRight(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).eachRight(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Integer(5), Integer(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(IntegerArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([IntegerArray([5, 6, 7]), IntegerArray([6, 7, 8]), IntegerArray([7, 8, 9])]))
        assert_equal(IntegerArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(IntegerArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(FloatArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), Integer(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), Float(4)), FloatArray([5, 6, 7]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))
        assert_equal(FloatArray([1, 2, 3]).eachRight(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([FloatArray([5, 6, 7]), FloatArray([6, 7, 8]), FloatArray([7, 8, 9])]))

        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachRight(Integer(StorageDyads.plus.value), Integer(4)), MixedArray([Integer(5), Float(6), Integer(7)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachRight(Integer(StorageDyads.plus.value), Float(4)), MixedArray([Float(5), Float(6), Float(7)]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachRight(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), MixedArray([MixedArray([Integer(5), Float(6), Integer(7)]), MixedArray([Integer(6), Float(7), Integer(8)]), MixedArray([Integer(7), Float(8), Integer(9)])]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachRight(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), MixedArray([MixedArray([Float(5), Float(6), Float(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Float(7), Float(8), Float(9)])]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).eachRight(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([MixedArray([Integer(5), Float(6), Integer(7)]), MixedArray([Float(6), Float(7), Float(8)]), MixedArray([Integer(7), Float(8), Integer(9)])]))

    def test_eachPair(self):
        assert_equal(IntegerArray([4, 5, 6]).eachPair(Integer(StorageDyads.plus.value)), MixedArray([Integer(9), Integer(11)]))
        assert_equal(FloatArray([4, 5, 6]).eachPair(Integer(StorageDyads.plus.value)), MixedArray([Float(9), Float(11)]))
        assert_equal(MixedArray([Integer(4), Integer(5), Integer(6)]).eachPair(Integer(StorageDyads.plus.value)), MixedArray([Integer(9), Integer(11)]))

    def test_over(self):
        assert_equal(Integer(4).over(Integer(StorageDyads.plus.value)), Integer(4))
        assert_equal(Float(4).over(Integer(StorageDyads.plus.value)), Float(4))

        assert_equal(IntegerArray([]).over(Integer(StorageDyads.plus.value)), IntegerArray([]))
        assert_equal(IntegerArray([4]).over(Integer(StorageDyads.plus.value)), IntegerArray([4]))
        assert_equal(IntegerArray([4, 5, 6]).over(Integer(StorageDyads.plus.value)), Integer(15))

        assert_equal(FloatArray([]).over(Integer(StorageDyads.plus.value)), FloatArray([]))
        assert_equal(FloatArray([4]).over(Integer(StorageDyads.plus.value)), FloatArray([4]))
        assert_equal(FloatArray([4, 5, 6]).over(Integer(StorageDyads.plus.value)), Float(15))

        assert_equal(MixedArray([]).over(Integer(StorageDyads.plus.value)), MixedArray([]))
        assert_equal(MixedArray([Integer(4)]).over(Integer(StorageDyads.plus.value)), MixedArray([Integer(4)]))
        assert_equal(MixedArray([Integer(4), Integer(5), Integer(6)]).over(Integer(StorageDyads.plus.value)), Integer(15))

    def test_overNeutral(self):
        assert_equal(Integer(1).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Integer(2))
        assert_equal(Integer(1).overNeutral(Integer(StorageDyads.plus.value), Float(1)), Float(2))
        assert_equal(Integer(1).overNeutral(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), IntegerArray([5, 6, 7]))
        assert_equal(Integer(1).overNeutral(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Integer(1).overNeutral(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([Integer(5), Float(6), Integer(7)]))

        assert_equal(Float(1).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Float(2))
        assert_equal(Float(1).overNeutral(Integer(StorageDyads.plus.value), Float(1)), Float(2))
        assert_equal(Float(1).overNeutral(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).overNeutral(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([5, 6, 7]))
        assert_equal(Float(1).overNeutral(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([Float(5), Float(6), Float(7)]))

        assert_equal(IntegerArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Integer(4))
        assert_equal(IntegerArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), Float(1)), Float(4))
        assert_equal(IntegerArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), IntegerArray([7, 8, 9]))
        assert_equal(IntegerArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(IntegerArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([Integer(7), Float(8), Integer(9)]))
        assert_isinstance(IntegerArray([]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Error)

        assert_equal(FloatArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Float(4))
        assert_equal(FloatArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), Float(1)), Float(4))
        assert_equal(FloatArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(FloatArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(FloatArray([1, 2]).overNeutral(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([Float(7), Float(8), Float(9)]))
        assert_isinstance(FloatArray([]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Error)

        assert_equal(MixedArray([Integer(1), Float(2)]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Float(4))
        assert_equal(MixedArray([Integer(1), Float(2)]).overNeutral(Integer(StorageDyads.plus.value), Float(1)), Float(4))
        assert_equal(MixedArray([Integer(1), Float(2)]).overNeutral(Integer(StorageDyads.plus.value), IntegerArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(MixedArray([Integer(1), Float(2)]).overNeutral(Integer(StorageDyads.plus.value), FloatArray([4, 5, 6])), FloatArray([7, 8, 9]))
        assert_equal(MixedArray([Integer(1), Float(2)]).overNeutral(Integer(StorageDyads.plus.value), MixedArray([Integer(4), Float(5), Integer(6)])), MixedArray([Float(7), Float(8), Float(9)]))
        assert_isinstance(MixedArray([]).overNeutral(Integer(StorageDyads.plus.value), Integer(1)), Error)

    def test_converge(self):
        assert_equal(IntegerArray([1, 2, 3]).converge(Integer(StorageMonads.shape.value)), IntegerArray([1]))

    def test_whileOne(self):
        assert_equal(Integer(0).whileOne(Integer(StorageMonads.atom.value), Integer(StorageMonads.enclose.value)), IntegerArray([0]))

    def test_iterate(self):
        assert_equal(IntegerArray([1, 2, 3]).iterate(Integer(StorageMonads.shape.value), Integer(2)), IntegerArray([1]))
        assert_equal(FloatArray([1, 2, 3]).iterate(Integer(StorageMonads.shape.value), Integer(2)), IntegerArray([1]))
        assert_equal(MixedArray([Integer(1), Float(2), Integer(3)]).iterate(Integer(StorageMonads.shape.value), Integer(2)), IntegerArray([1]))

    def test_scanOver(self):
        assert_equal(IntegerArray([1, 2, 3]).scanOver(Integer(StorageDyads.plus.value)), MixedArray([Integer(1), Integer(3), Integer(6)]))

    def test_scanOverNeutral(self):
        assert_equal(IntegerArray([1, 2, 3]).scanConverging(Integer(StorageMonads.shape.value)), MixedArray([IntegerArray([1, 2, 3]), IntegerArray([3]), IntegerArray([1])]))

    def test_scanWhileOne(self):
        assert_equal(Integer(0).scanWhileOne(Integer(StorageMonads.atom.value), Integer(StorageMonads.enclose.value)), MixedArray([Integer(0), IntegerArray([0])]))

    def test_scanIterating(self):
        assert_equal(IntegerArray([1, 2, 3]).scanIterating(Integer(StorageMonads.shape.value), Integer(2)), MixedArray([IntegerArray([1, 2, 3]), IntegerArray([3]), IntegerArray([1])]))

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
