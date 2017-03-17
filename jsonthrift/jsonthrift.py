# -*- coding:utf-8 -*-
from thriftpy.parser import parse
from .TBinaryProtocol import TBinaryProtocol
from .TFramedTransport import TFramedTransport
from .TBufferedTransport import TBufferedTransport
from .TTypes import TMessageType


class JsonThrift(object):

    PROTOCOLS = {
        'TBinaryProtocol': TBinaryProtocol,
    }

    TRANSPORTS = {
        'TFramedTransport': TFramedTransport,
        'TBufferedTransport': TBufferedTransport,
    }

    def __init__(self, transport, protocol, thrift_idl, service, method):
        if transport not in JsonThrift.TRANSPORTS:
            raise Exception('Not supported transport: %s' % transport)
        self.transport = JsonThrift.TRANSPORTS[transport]()
        if protocol not in JsonThrift.PROTOCOLS:
            raise Exception('Not supported protocol: %s' % protocol)
        self.protocol = JsonThrift.PROTOCOLS[protocol](self.transport)
        self.thrift_idl = thrift_idl
        self.service = service
        self.method = method
        self._init()

    def _init(self):
        self.args_spec, self.result_spec = self.get_method_spec()

    def get_method_spec(self):
        thrift_meta = parse(self.thrift_idl).__thrift_meta__
        service_spec = None
        for s in thrift_meta['services']:
            if s.__name__ == self.service:
                service_spec = s
        if not service_spec:
            raise Exception('Service %s not found in %s' % (
                self.service, self.thrift_idl))

        args_spec_name = '%s_args' % self.method
        if not hasattr(service_spec, args_spec_name):
            raise Exception('Method %s args spec not found in %s' % (
                self.method, self.service))
        args_spec = getattr(service_spec, args_spec_name).thrift_spec

        result_spec_name = '%s_result' % self.method
        if not hasattr(service_spec, result_spec_name):
            raise Exception('Method %s result spec not found in %s' % (
                self.method, self.service))
        result_spec = getattr(service_spec, result_spec_name).thrift_spec
        return args_spec, result_spec

    def pack_request(self, json_data, seq_id, msg_type=TMessageType.CALL):
        return self.protocol.pack_message(
            msg_type, self.method, seq_id, self.args_spec, json_data)

    def pack_response(self, json_data, seq_id):
        return self.protocol.pack_message(
            TMessageType.REPLY, self.method, seq_id,
            self.result_spec, json_data)

    def unpack_response(self, msg):
        return self.protocol.unpack_message(self.result_spec, msg)

    def unpack_request(self, msg):
        return self.protocol.unpack_message(self.args_spec, msg)
