#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
))
from jsonthrift.jsonthrift import JsonThrift
import socket
import unittest
import multiprocessing
import time
from thrift_tutorial.server import CalculatorHandler

transport = 'TBufferedTransport'
protocol = 'TBinaryProtocol'
thrift_file = 'thrift_tutorial/tutorial.thrift'
service = 'Calculator'

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


def start_server():
    sys.path.append('thrift_tutorial/gen-py')

    from tutorial import Calculator
    from tutorial.ttypes import InvalidOperation, Operation
    from shared.ttypes import SharedStruct

    from thrift.transport import TSocket
    from thrift.transport import TTransport
    from thrift.protocol import TBinaryProtocol
    from thrift.server import TServer
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    server.serve()


class RemoteCallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = multiprocessing.Process(target=start_server)
        cls.p.start()
        time.sleep(1)

        addr = socket.getaddrinfo(
            "localhost", 9090, socket.AF_UNSPEC, socket.SOCK_STREAM, 0,
            socket.AI_PASSIVE | socket.AI_ADDRCONFIG)
        cls.socket = socket.socket(addr[0][0], addr[0][1])
        try:
            cls.socket.connect(addr[0][4])
        except Exception, e:
            print "To run these tests, you have to start tutorial server first!"
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.socket.close()
        cls.p.terminate()

    @classmethod
    def remote_call(cls, msg):
        cls.socket.send(msg)
        return cls.socket.recv(1024)

    def test_add(self):
        method = 'add'
        params = {"num1": 1, "num2": 3}
        expect = {"success": 4}
        jt = JsonThrift(transport, protocol, thrift_file, service, method)
        msg = jt.pack_request(params, 1)
        result = jt.unpack_response(self.remote_call(msg))[4]
        self.assertTrue(compare(result, expect))

    def test_calculate_normal(self):
        method = 'calculate'
        params = {"logid": 1, "w": { "op": 1, "num1": 1, "num2": 0 } }
        expect = {'success': 1}
        jt = JsonThrift(transport, protocol, thrift_file, service, method)
        msg = jt.pack_request(params, 1)
        result = jt.unpack_response(self.remote_call(msg))[4]
        self.assertTrue(compare(result, expect))

    def test_calculate_exception(self):
        method = 'calculate'
        params = {"logid": 1, "w":{"op": 4, "num1": 1, "num2": 0}}
        expect = {'ouch': {'whatOp': 4, 'why': 'Cannot divide by 0'}}
        jt = JsonThrift(transport, protocol, thrift_file, service, method)
        msg = jt.pack_request(params, 1)
        result = jt.unpack_response(self.remote_call(msg))[4]
        self.assertTrue(compare(result, expect))


if __name__ == '__main__':
    unittest.main()
