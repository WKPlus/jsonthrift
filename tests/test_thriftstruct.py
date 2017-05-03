#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import unittest
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
))
from jsonthrift.thriftstruct import ThriftStruct

protocol = 'TBinaryProtocol'
thrift_file = 'data/complex.thrift'


class ThriftStructTest(unittest.TestCase):
    def test_pack_struct(self):
        ts = ThriftStruct(thrift_file)
        data = {
            'index': 2,
            'istrue': 'true'
        }
        binary = ts.pack_struct('complex.returnType', data)
        expect1 = '\x08\x00\x01\x00\x00\x00\x02\x0b\x00\x02\x00\x00\x00\x04true\x00'
        expect2 = '\x0b\x00\x02\x00\x00\x00\x04true\x08\x00\x01\x00\x00\x00\x02\x00'
        equal = expect1 == binary or expect2 == binary
        self.assertTrue(equal)

    def test_unpack_struct(self):
        ts = ThriftStruct(thrift_file)
        binary = '\x08\x00\x01\x00\x00\x00\x02\x0b\x00\x02\x00\x00\x00\x04true\x00'
        data = ts.unpack_struct('complex.returnType', binary)
        expect = {
            'index': 2,
            'istrue': 'true'
        }
        self.assertEqual(expect, data)


if __name__ == '__main__':
    unittest.main()

