from storage import *
from testify import TestCase, assert_equal

class AddTests(TestCase):
    def test_add_integer_integer(self):
        assert_equal(Integer(1).add(Integer(2)), Integer(3))
        assert_equal(Integer(-1).add(Integer(-1)), Integer(-2))
        assert_equal(Integer(0).add(Integer(0)), Integer(0))

    def test_add_integer_float(self):
        assert_equal(Integer(1).add(Float(2)), Float(3))
        assert_equal(Integer(-1).add(Float(-1)), Float(-2))
        assert_equal(Integer(0).add(Float(0)), Float(0))

    def test_add_integer_integer_array(self):
        assert_equal(Integer(1).add(IntegerArray([2, 3])), IntegerArray([3, 4]))
        assert_equal(Integer(-1).add(IntegerArray([-1, 0])), IntegerArray([-2, -1]))
        assert_equal(Integer(0).add(IntegerArray([0, 1])), IntegerArray([0, 1]))

    def test_add_integer_float_array(self):
        assert_equal(Integer(1).add(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Integer(-1).add(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Integer(0).add(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_add_integer_mixed_array(self):
        assert_equal(Integer(1).add(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(3), Float(4)]))
        assert_equal(Integer(-1).add(MixedArray([Integer(-1), Float(0)])), MixedArray([Integer(-2), Float(-1)]))
        assert_equal(Integer(0).add(MixedArray([Integer(0), Float(1)])), MixedArray([Integer(0), Float(1)]))

    def test_add_float_integer(self):
        assert_equal(Float(1).add(Integer(2)), Float(3))
        assert_equal(Float(-1).add(Integer(-1)), Float(-2))
        assert_equal(Float(0).add(Integer(0)), Float(0))

    def test_add_float_float(self):
        assert_equal(Float(1).add(Float(2)), Float(3))
        assert_equal(Float(-1).add(Float(-1)), Float(-2))
        assert_equal(Float(0).add(Float(0)), Float(0))

    def test_add_float_integer_array(self):
        assert_equal(Float(1).add(IntegerArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).add(IntegerArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).add(IntegerArray([0, 1])), FloatArray([0, 1]))

    def test_add_float_float_array(self):
        assert_equal(Float(1).add(FloatArray([2, 3])), FloatArray([3, 4]))
        assert_equal(Float(-1).add(FloatArray([-1, 0])), FloatArray([-2, -1]))
        assert_equal(Float(0).add(FloatArray([0, 1])), FloatArray([0, 1]))

    def test_add_float_mixed_array(self):
        assert_equal(Float(1).add(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(4)]))
        assert_equal(Float(-1).add(MixedArray([Integer(-1), Float(0)])), MixedArray([Float(-2), Float(-1)]))
        assert_equal(Float(0).add(MixedArray([Integer(0), Float(1)])), MixedArray([Float(0), Float(1)]))

    def test_add_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).add(Integer(1)), IntegerArray([3, 4]))
        assert_equal(IntegerArray([-1, 0]).add(Integer(-1)), IntegerArray([-2, -1]))
        assert_equal(IntegerArray([0, 1]).add(Integer(0)), IntegerArray([0, 1]))

    def test_add_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).add(Float(1)), FloatArray([3, 4]))
        assert_equal(IntegerArray([-1, 0]).add(Float(-1)), FloatArray([-2, -1]))
        assert_equal(IntegerArray([0, 1]).add(Float(0)), FloatArray([0, 1]))

    def test_add_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 5]), IntegerArray([5, 6])]))
        assert_equal(IntegerArray([-1, 0]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 2]), IntegerArray([2, 3])]))
        assert_equal(IntegerArray([0, 1]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([2, 3]), IntegerArray([3, 4])]))

    def test_add_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).add(FloatArray([2, 3])), MixedArray([FloatArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(IntegerArray([-1, 0]).add(FloatArray([2, 3])), MixedArray([FloatArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(IntegerArray([0, 1]).add(FloatArray([2, 3])), MixedArray([FloatArray([2, 3]), FloatArray([3, 4])]))

    def test_add_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(5)]), MixedArray([Integer(5), Float(6)])]))
        assert_equal(IntegerArray([-1, 0]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2)]), MixedArray([Integer(2), Float(3)])]))
        assert_equal(IntegerArray([0, 1]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2), Float(3)]), MixedArray([Integer(3), Float(4)])]))

    def test_add_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).add(Integer(2)), MixedArray([Integer(4), Float(5)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).add(Integer(2)), MixedArray([Integer(1), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).add(Integer(2)), MixedArray([Integer(2), Float(3)]))

    def test_add_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).add(Float(2)), MixedArray([Float(4), Float(5)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).add(Float(2)), MixedArray([Float(1), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).add(Float(2)), MixedArray([Float(2), Float(3)]))

    def test_add_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).add(IntegerArray([2, 3])), MixedArray([IntegerArray([2, 3]), FloatArray([3, 4])]))

    def test_add_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).add(FloatArray([2, 3])), MixedArray([FloatArray([4, 5]), FloatArray([5, 6])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).add(FloatArray([2, 3])), MixedArray([FloatArray([1, 2]), FloatArray([2, 3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).add(FloatArray([2, 3])), MixedArray([FloatArray([2, 3]), FloatArray([3, 4])]))

    def test_add_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(5)]), MixedArray([Float(5), Float(6)])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(1), Float(2)]), MixedArray([Float(2), Float(3)])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).add(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(2), Float(3)]), MixedArray([Float(3), Float(4)])]))

class SubtractTests(TestCase):
    def test_subtract_integer_integer(self):
        assert_equal(Integer(1).subtract(Integer(2)), Integer(-1))
        assert_equal(Integer(-1).subtract(Integer(-1)), Integer(0))
        assert_equal(Integer(0).subtract(Integer(0)), Integer(0))

    def test_subtract_integer_float(self):
        assert_equal(Integer(1).subtract(Float(2)), Float(-1))
        assert_equal(Integer(-1).subtract(Float(-1)), Float(0))
        assert_equal(Integer(0).subtract(Float(0)), Float(0))

    def test_subtract_integer_integer_array(self):
        assert_equal(Integer(1).subtract(IntegerArray([2, 3])), IntegerArray([-1, -2]))
        assert_equal(Integer(-1).subtract(IntegerArray([-1, 0])), IntegerArray([0, -1]))
        assert_equal(Integer(0).subtract(IntegerArray([0, 1])), IntegerArray([0, -1]))

    def test_subtract_integer_float_array(self):
        assert_equal(Integer(1).subtract(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Integer(-1).subtract(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Integer(0).subtract(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_integer_mixed_array(self):
        assert_equal(Integer(1).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(-1), Float(-2)]))
        assert_equal(Integer(-1).subtract(MixedArray([Integer(-1), Float(0)])), MixedArray([Integer(0), Float(-1)]))
        assert_equal(Integer(0).subtract(MixedArray([Integer(0), Float(1)])), MixedArray([Integer(0), Float(-1)]))

    def test_subtract_float_integer(self):
        assert_equal(Float(1).subtract(Integer(-1)), Float(2))
        assert_equal(Float(-1).subtract(Integer(0)), Float(-1))
        assert_equal(Float(0).subtract(Integer(0)), Float(0))

    def test_subtract_float_float(self):
        assert_equal(Float(1).subtract(Float(2)), Float(-1))
        assert_equal(Float(-1).subtract(Float(-1)), Float(0))
        assert_equal(Float(0).subtract(Float(0)), Float(0))

    def test_subtract_float_integer_array(self):
        assert_equal(Float(1).subtract(IntegerArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).subtract(IntegerArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).subtract(IntegerArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_float_float_array(self):
        assert_equal(Float(1).subtract(FloatArray([2, 3])), FloatArray([-1, -2]))
        assert_equal(Float(-1).subtract(FloatArray([-1, 0])), FloatArray([0, -1]))
        assert_equal(Float(0).subtract(FloatArray([0, 1])), FloatArray([0, -1]))

    def test_subtract_float_mixed_array(self):
        assert_equal(Float(1).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([Float(-1), Float(-2)]))
        assert_equal(Float(-1).subtract(MixedArray([Integer(-1), Float(0)])), MixedArray([Float(0), Float(-1)]))
        assert_equal(Float(0).subtract(MixedArray([Integer(0), Float(1)])), MixedArray([Float(0), Float(-1)]))

    def test_subtract_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).subtract(Integer(1)), IntegerArray([1, 2]))
        assert_equal(IntegerArray([-1, 0]).subtract(Integer(-1)), IntegerArray([0, 1]))
        assert_equal(IntegerArray([0, 1]).subtract(Integer(0)), IntegerArray([0, 1]))

    def test_subtract_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).subtract(Float(1)), FloatArray([1, 2]))
        assert_equal(IntegerArray([-1, 0]).subtract(Float(-1)), FloatArray([0, 1]))
        assert_equal(IntegerArray([0, 1]).subtract(Float(0)), FloatArray([0, 1]))

    def test_subtract_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([0, -1]), IntegerArray([1, 0])]))
        assert_equal(IntegerArray([-1, 0]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([-3, -4]), IntegerArray([-2, -3])]))
        assert_equal(IntegerArray([0, 1]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([-2, -3]), IntegerArray([-1, -2])]))

    def test_subtract_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(IntegerArray([-1, 0]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(IntegerArray([0, 1]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(0), Float(-1)]), MixedArray([Integer(1), Float(0)])]))
        assert_equal(IntegerArray([-1, 0]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-3), Float(-4)]), MixedArray([Integer(-2), Float(-3)])]))
        assert_equal(IntegerArray([0, 1]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-2), Float(-3)]), MixedArray([Integer(-1), Float(-2)])]))

    def test_subtract_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).subtract(Integer(2)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).subtract(Integer(2)), MixedArray([Integer(-3), Float(-2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).subtract(Integer(2)), MixedArray([Integer(-2), Float(-1)]))

    def test_subtract_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).subtract(Float(2)), MixedArray([Float(0), Float(1)]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).subtract(Float(2)), MixedArray([Float(-3), Float(-2)]))
        assert_equal(MixedArray([Integer(0), Float(1)]).subtract(Float(2)), MixedArray([Float(-2), Float(-1)]))

    def test_subtract_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).subtract(IntegerArray([2, 3])), MixedArray([IntegerArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([0, -1]), FloatArray([1, 0])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([-3, -4]), FloatArray([-2, -3])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).subtract(FloatArray([2, 3])), MixedArray([FloatArray([-2, -3]), FloatArray([-1, -2])]))

    def test_subtract_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(0), Float(-1)]), MixedArray([Float(1), Float(0)])]))
        assert_equal(MixedArray([Integer(-1), Float(0)]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-3), Float(-4)]), MixedArray([Float(-2), Float(-3)])]))
        assert_equal(MixedArray([Integer(0), Float(1)]).subtract(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(-2), Float(-3)]), MixedArray([Float(-1), Float(-2)])]))

class MultiplyTests(TestCase):
    def test_multiply_integer_integer(self):
        assert_equal(Integer(1).multiply(Integer(2)), Integer(2))

    def test_multiply_integer_float(self):
        assert_equal(Integer(1).multiply(Float(2)), Float(2))

    def test_multiply_integer_integer_array(self):
        assert_equal(Integer(1).multiply(IntegerArray([2, 3])), IntegerArray([2, 3]))

    def test_multiply_integer_float_array(self):
        assert_equal(Integer(1).multiply(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_multiply_integer_mixed_array(self):
        assert_equal(Integer(1).multiply(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3)]))

    def test_multiply_float_integer(self):
        assert_equal(Float(1).multiply(Integer(-1)), Float(-1))

    def test_multiply_float_float(self):
        assert_equal(Float(1).multiply(Float(2)), Float(2))

    def test_multiply_float_integer_array(self):
        assert_equal(Float(1).multiply(IntegerArray([2, 3])), FloatArray([2, 3]))

    def test_multiply_float_float_array(self):
        assert_equal(Float(1).multiply(FloatArray([2, 3])), FloatArray([2, 3]))

    def test_multiply_float_mixed_array(self):
        assert_equal(Float(1).multiply(MixedArray([Integer(2), Float(3)])), MixedArray([Float(2), Float(3)]))

    def test_multiply_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).multiply(Integer(1)), IntegerArray([2, 3]))

    def test_multiply_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).multiply(Float(1)), FloatArray([2, 3]))

    def test_multiply_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).multiply(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 6]), IntegerArray([6, 9])]))

    def test_multiply_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).multiply(FloatArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_multiply_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).multiply(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(6)]), MixedArray([Integer(6), Float(9)])]))

    def test_multiply_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).multiply(Integer(2)), MixedArray([Integer(4), Float(6)]))

    def test_multiply_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).multiply(Float(2)), MixedArray([Float(4), Float(6)]))

    def test_multiply_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).multiply(IntegerArray([2, 3])), MixedArray([IntegerArray([4, 6]), FloatArray([6, 9])]))

    def test_multiply_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).multiply(FloatArray([2, 3])), MixedArray([FloatArray([4, 6]), FloatArray([6, 9])]))

    def test_multiply_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).multiply(MixedArray([Integer(2), Float(3)])), MixedArray([MixedArray([Integer(4), Float(6)]), MixedArray([Float(6), Float(9)])]))

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
        assert_equal(Integer(5).count(), Integer(1))

    def test_count_float(self):
        assert_equal(Float(5.5).count(), Integer(1))

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
        assert_equal(Integer(5).shape(), IntegerArray([]))

    def test_shape_float(self):
        assert_equal(Float(5.5).shape(), IntegerArray([]))

    def test_shape_integer_array(self):
        assert_equal(IntegerArray([0, 1, 2]).shape(), IntegerArray([3]))

    def test_shape_float_array(self):
        assert_equal(FloatArray([0.1, 1.5, 2.9]).shape(), IntegerArray([3]))

    def test_shape_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), IntegerArray([1, 2, 3])]).shape(), MixedArray([IntegerArray([]), IntegerArray([]), IntegerArray([3])]))

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

    def test_take_float_array(self):
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(2)), FloatArray([0, 1]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(-2)), FloatArray([0, 2]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(0)), FloatArray([]))
        assert_equal(FloatArray([0, 1, 0, 2]).take(Integer(9)), FloatArray([0, 1, 0, 2, 0, 1, 0, 2, 0]))

    def test_take_mixed_array(self):
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(2)), MixedArray([Integer(0), Float(1)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(-2)), MixedArray([Integer(0), Float(2)]))
        assert_equal(MixedArray([Integer(0), Float(1), Integer(0), Float(2)]).take(Integer(0)), MixedArray([]))
        assert_equal(MixedArray([Float(0), Float(1), Float(0), Float(2)]).take(Integer(9)), MixedArray([Float(0), Float(1), Float(0), Float(2), Float(0), Float(1), Float(0), Float(2), Float(0)]))

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
        assert_equal(MixedArray([Integer(2), Float(3)]).split(Float(0.5)), MixedArray([MixedArray([Integer(2)]), MixedArray([Float(3), Float(2)])]))

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
        assert_equal(Float(1).max(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(2), Float(3)]))

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

    def test_max_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(Integer(3)), MixedArray([Integer(3), Integer(3)]))

    def test_max_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(Float(3)), MixedArray([Integer(3), Integer(3)]))

    def test_max_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(IntegerArray([2, 3])), MixedArray([Integer(3), Float(3)]))

    def test_max_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(FloatArray([2, 3])), MixedArray([Float(3), Float(3)]))

    def test_max_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).max(MixedArray([Integer(2), Float(3)])), MixedArray([Float(3), Float(3)]))

class MinTests(TestCase):
    def test_min_integer_integer(self):
        assert_equal(Integer(1).min(Integer(2)), Integer(1))

    def test_min_integer_float(self):
        assert_equal(Integer(1).min(Float(2)), Float(1))

    def test_min_integer_integer_array(self):
        assert_equal(Integer(1).min(IntegerArray([2, 3])), IntegerArray([1, 1]))

    def test_min_integer_float_array(self):
        assert_equal(Integer(1).min(FloatArray([2, 3])), FloatArray([1, 1]))

    def test_min_integer_mixed_array(self):
        assert_equal(Integer(1).min(MixedArray([Integer(2), Float(3)])), MixedArray([Integer(1), Integer(1)]))

    def test_min_float_integer(self):
        assert_equal(Float(1).min(Integer(-1)), Float(-1))

    def test_min_float_float(self):
        assert_equal(Float(1).min(Float(2)), Float(1))

    def test_min_float_integer_array(self):
        assert_equal(Float(1).min(IntegerArray([2, 3])), FloatArray([1, 1]))

    def test_min_float_float_array(self):
        assert_equal(Float(1).min(FloatArray([2, 3])), FloatArray([1, 1]))

    def test_min_float_mixed_array(self):
        assert_equal(Float(1).min(MixedArray([Integer(2), Float(3)])), MixedArray([Float(1), Float(1)]))

    def test_min_integer_array_integer(self):
        assert_equal(IntegerArray([2, 3]).min(Integer(1)), IntegerArray([1, 1]))

    def test_min_integer_array_float(self):
        assert_equal(IntegerArray([2, 3]).min(Float(1)), FloatArray([1, 1]))

    def test_min_integer_array_integer_array(self):
        assert_equal(IntegerArray([2, 3]).min(IntegerArray([2, 3])), IntegerArray([2, 2]))

    def test_min_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).min(FloatArray([2, 3])), FloatArray([2, 2]))

    def test_min_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).min(MixedArray([Integer(2), Float(3)])), MixedArray([Float(2), Float(2)]))

    def test_min_mixed_array_integer(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Integer(3)), MixedArray([Integer(2), Float(3)]))

    def test_min_mixed_array_float(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(Float(3)), MixedArray([Integer(2), Float(3)]))

    def test_min_mixed_array_integer_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(IntegerArray([2, 3])), MixedArray([Integer(2), Float(2)]))

    def test_min_mixed_array_float_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(FloatArray([2, 3])), MixedArray([Float(2), Float(2)]))

    def test_min_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).min(MixedArray([Integer(2), Float(2)])), MixedArray([Float(2), Float(2)]))

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
        assert_equal(IntegerArray([2, 3]).equal(IntegerArray([2, 3])), IntegerArray([0, 0]))

    def test_equal_integer_array_float_array(self):
        assert_equal(IntegerArray([2, 3]).equal(FloatArray([2, 3])), IntegerArray([0, 0]))

    def test_equal_integer_array_mixed_array(self):
        assert_equal(IntegerArray([2, 3]).equal(MixedArray([Integer(2), Float(3)])), IntegerArray([0, 0]))

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
        assert_equal(MixedArray([Integer(2), Float(3)]).cut(IntegerArray([1, 2])), MixedArray([MixedArray([Float(3)])]))

    def test_cut_mixed_array_mixed_array(self):
        assert_equal(MixedArray([Integer(2), Float(3)]).cut(MixedArray([Integer(1), Integer(2)])), MixedArray([MixedArray([Float(3)])]))

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

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
