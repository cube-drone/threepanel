from django.test import TestCase
from .bloom import calculator, bloom, hash_to_location

class CalculatorTest(TestCase):

    def test_calculator(self):
        m, k = calculator(5000, 0.001)

        self.assertEqual(m, 71888)
        self.assertEqual(k, 10)


class HashToLocationTest(TestCase): 

    def test_hash_to_location(self):
        loc1 = hash_to_location(1, "hello", 100)
        loc2 = hash_to_location(2, "hello", 100)

        self.assertNotEqual(loc1, loc2)
        assert loc1 >= 0
        assert loc1 < 100
        assert loc2 >= 0
        assert loc2 < 100


class BloomFilterTest(TestCase):

    def test_filter_works(self):
        b = bloom(["one", "two", "three"])
        assert b.check("one")
        assert b.check("two")
        assert b.check("three")
        assert not b.check("four")
        assert not b.check("FIVE")
    
    def test_get_bits(self):
        b = bloom(["one", "two", "three"])
        self.assertEqual(b.bits.to01(), 
                         "10101001011000111110100010100100010001100011")

    def test_empty_set(self):
        with self.assertRaises(ValueError):
            bloom([])
