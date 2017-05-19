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


class ThriftStructTest(unittest.TestCase):
    def test_pack_struct(self):
        thrift_file = 'data/complex.thrift'
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
        thrift_file = 'data/complex.thrift'
        ts = ThriftStruct(thrift_file)
        binary = '\x08\x00\x01\x00\x00\x00\x02\x0b\x00\x02\x00\x00\x00\x04true\x00'
        data = ts.unpack_struct('complex.returnType', binary)
        expect = {
            'index': 2,
            'istrue': 'true'
        }
        self.assertEqual(expect, data)

    def test_pack_intkey(self):
        thrift_file = 'data/intkey.thrift'
        ts = ThriftStruct(thrift_file)
        data = {
            'byte_key': {
                '1': '1',
            },
            'i16_key': {
                '2': '2',
            },
            'i32_key': {
                '3': '3',
            },
            'i64_key': {
                '4': '4',
            },
        }
        binary = ts.pack_struct('intkey.IntKey', data)


if __name__ == '__main__':
    unittest.main()

