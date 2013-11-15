#!/usr/bin/python3 -tt
import unittest
import sys

sys.path.insert(0, '..')
import innodb_tablespace_info


class TestCheckDatafiles(unittest.TestCase):
    def setUp(self):
        self.cdf = innodb_tablespace_info.check_datafiles

    def test_1file_10M_extend_100M(self):
        '''Test ibdata1:10M:autoextend:max:100M'''
        result = self.cdf('/nonexistend', 'ibdata1:10M:autoextend:max:100M')
        self.assertEqual(result['ibdata1'].initsize, 10485760)
        self.assertEqual(result['ibdata1'].maxsize, 104857600)
        self.assertEqual(result['ibdata1'].autoextend, 'on')

    def test_1file_10M_extend(self):
        '''Test ibdata1:10M:autoextend'''
        result = self.cdf('/nonexistend', 'ibdata1:10M:autoextend')
        self.assertEqual(result['ibdata1'].initsize, 10485760)
        self.assertEqual(result['ibdata1'].maxsize, None)
        self.assertEqual(result['ibdata1'].autoextend, 'on')

    def test_2file_10M(self):
        '''Test ibdata1:10M;ibdata2:10M'''
        result = self.cdf('/nonexistend', 'ibdata1:10M;ibdata2:10M')
        self.assertEqual(result['ibdata1'].initsize, 10485760)
        self.assertEqual(result['ibdata1'].maxsize, None)
        self.assertEqual(result['ibdata1'].autoextend, None)
        self.assertEqual(result['ibdata2'].initsize, 10485760)
        self.assertEqual(result['ibdata2'].maxsize, None)
        self.assertEqual(result['ibdata2'].autoextend, None)

    def test_2file_10M_extend_100M(self):
        '''Test ibdata1:10M;ibdata2:10M:autoextend:max:100M'''
        result = self.cdf('/nonexistend',
                          'ibdata1:10M;ibdata2:10M:autoextend:max:100M')
        self.assertEqual(result['ibdata1'].initsize, 10485760)
        self.assertEqual(result['ibdata1'].maxsize, None)
        self.assertEqual(result['ibdata1'].autoextend, None)
        self.assertEqual(result['ibdata2'].initsize, 10485760)
        self.assertEqual(result['ibdata2'].maxsize, 104857600)
        self.assertEqual(result['ibdata2'].autoextend, 'on')

    def test_2file_invalid(self):
        '''Test ibdata1:10M:ibdata2:autoextend:max:100M'''
        result = self.cdf('/nonexistend',
                          'ibdata1:10M:ibdata2:autoextend:max:100M')
        self.assertEqual(result['ibdata1'].initsize, 10485760)
        self.assertEqual(result['ibdata1'].maxsize, 104857600)
        self.assertEqual(result['ibdata1'].autoextend, 'on')

if __name__ == '__main__':
    unittest.main()
