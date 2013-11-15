#!/usr/bin/python3 -tt
import unittest
import sys

sys.path.insert(0, '..')
import innodb_tablespace_info


class TestSizeToInt(unittest.TestCase):

    def test_s2i_b(self):
        '''Test 100 Bytes'''
        result = innodb_tablespace_info.size_to_int('100')
        self.assertEqual(result, 100)

    def test_s2i_k(self):
        '''Test 100K'''
        result = innodb_tablespace_info.size_to_int('100K')
        self.assertEqual(result, 102400)

    def test_s2i_m(self):
        '''Test 100M'''
        result = innodb_tablespace_info.size_to_int('100M')
        self.assertEqual(result, 104857600)

    def test_s2i_g(self):
        '''Test 100G'''
        result = innodb_tablespace_info.size_to_int('100G')
        self.assertEqual(result, 107374182400)

    def test_s2i_x(self):
        '''Test 100X (invalid)'''
        self.assertRaises(ValueError,
                          innodb_tablespace_info.size_to_int,
                          '100X')

if __name__ == '__main__':
    unittest.main()
