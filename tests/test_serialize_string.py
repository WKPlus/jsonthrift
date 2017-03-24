#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import unittest
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
))
from jsonthrift.jsonthrift import JsonThrift

transport = 'TBufferedTransport'
protocol = 'TBinaryProtocol'
thrift_file = 'data/string.thrift'
service = 'TestService'
method = 'test_call'


class SerializeStringTest(unittest.TestCase):
    def test_serialize_unprintable_char(self):
        with open('data/string.json') as in_fd:
            data = in_fd.read()
        params = json.loads(data)
        jt = JsonThrift(transport, protocol, thrift_file, service, method)
        msg = jt.pack_request(params, 1)
        expect = (
            '\x80\x01\x00\x01\x00\x00\x00\x09test_call\x00\x00\x00\x01'
            '\x0b\x00\x01\x00\x00\x00\x06\x00\x01\x02\x03\x91\x7f\x00'
        )

        self.assertEqual(msg, expect)


if __name__ == '__main__':
    unittest.main()

