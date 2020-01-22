import unittest
from process_yaml import convert_retention_to_int

class TestConversion(unittest.TestCase):
    def test_convert_retention_to_int(self):
        self.assertEqual(convert_retention_to_int('9'), 9)
        self.assertEqual(convert_retention_to_int('0s'), 0)
        self.assertEqual(convert_retention_to_int('2s'), 2)
        self.assertEqual(convert_retention_to_int('3m'), 180)
        self.assertEqual(convert_retention_to_int('4h'), 14400)
        self.assertEqual(convert_retention_to_int('5d'), 432000)
        self.assertEqual(convert_retention_to_int('2y'), 63072000)
        self.assertRaises(Exception, convert_retention_to_int, '')
        self.assertRaises(Exception, convert_retention_to_int, 'randoms string')
        self.assertRaises(Exception, convert_retention_to_int, '000badformat')
        self.assertRaises(Exception, convert_retention_to_int, '12x')

if __name__ == '__main__':
    unittest.main()