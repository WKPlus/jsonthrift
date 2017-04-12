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

transport = 'TFramedTransport'
protocol = 'TBinaryProtocol'
thrift_file = 'data/complex.thrift'
service = 'TestService'
method = 'test_call'


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def compare(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, dict):
        for k, v in a.iteritems():
            if k not in b:
                return False
            return compare(v, b[k])
    elif isinstance(a, list):
        if len(a) != len(b):
            return False
        for i in xrange(len(a)):
            return compare(a[i], b[i])
    else:
        return a == b


class SerializeTest(unittest.TestCase):
    def test_serialize(self):
        with open('data/complex.json') as in_fd:
            data = in_fd.read()
        params = json.loads(data, object_hook=_decode_dict)
        jt = JsonThrift(transport, protocol, thrift_file, service)
        msg = jt.pack_request(method, params, 1)

        with open('data/binary') as in_fd:
            data = in_fd.read().strip()
        binary = data.decode('string-escape')
        self.assertEqual(len(msg), len(binary))

    def test_deserialize(self):
        with open('data/binary') as in_fd:
            data = in_fd.read()
        binary = data.decode('string-escape')
        jt = JsonThrift(transport, protocol, thrift_file, service)
        content = jt.unpack_request(binary)[4]

        with open('data/complex.json') as in_fd:
            data = in_fd.read()
        params = json.loads(data, object_hook=_decode_dict)
        self.assertTrue(compare(params, content))


if __name__ == '__main__':
    unittest.main()
