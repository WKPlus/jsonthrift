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

    def __init__(self, transport, protocol, thrift_idl, service):
        if transport not in JsonThrift.TRANSPORTS:
            raise Exception('Not supported transport: %s' % transport)
        self.transport = JsonThrift.TRANSPORTS[transport]()
        if protocol not in JsonThrift.PROTOCOLS:
            raise Exception('Not supported protocol: %s' % protocol)
        self.protocol = JsonThrift.PROTOCOLS[protocol](self.transport)
        self.thrift_idl = thrift_idl
        self.service = service
        self._init()

    def _init(self):
        self.method_specs = self._get_method_specs()

    def _get_method_specs(self):
        thrift_meta = parse(self.thrift_idl).__thrift_meta__
        service_spec = None
        for s in thrift_meta['services']:
            if s.__name__ == self.service:
                service_spec = s
        if not service_spec:
            raise Exception('Service %s not found in %s' % (
                self.service, self.thrift_idl))

        method_specs = {}
        for method in service_spec.thrift_services:
            method_specs[method] = self._get_method_spec(service_spec, method)
        return method_specs

    def _get_method_spec(self, service_spec, method):
        args_spec_name = '%s_args' % method
        if not hasattr(service_spec, args_spec_name):
            raise Exception('Method %s args spec not found in %s' % (
                method, self.service))
        args_spec = getattr(service_spec, args_spec_name).thrift_spec

        result_spec_name = '%s_result' % method
        if not hasattr(service_spec, result_spec_name):
            raise Exception('Method %s result spec not found in %s' % (
                method, self.service))
        result_spec = getattr(service_spec, result_spec_name).thrift_spec
        return args_spec, result_spec

    def pack_request(self, method, json_data, seq_id=1,
                     msg_type=TMessageType.CALL):
        if method not in self.method_specs:
            raise Exception('Pack req failed: method %s not defined in %s'
                            % (method, self.service))
        args_spec = self.method_specs[method][0]
        return self.protocol.pack_message(
            msg_type, method, seq_id, args_spec, json_data)

    def pack_response(self, method, json_data, seq_id,
                      msg_type=TMessageType.REPLY):
        if method not in self.method_specs:
            raise Exception('Pack resp failed: method %s not defined in %s'
                            % (method, self.service))
        result_spec = self.method_specs[method][1]
        return self.protocol.pack_message(
            msg_type, method, seq_id, result_spec, json_data)

    def unpack_response(self, msg):
        size, msg_type, method, seq_id = self.protocol.unpack_message_header(msg)
        if method not in self.method_specs:
            raise Exception('Unpack resp failed: method %s not defined in %s'
                            % (method, self.service))
        result_spec = self.method_specs[method][1]
        value =  self.protocol.read_fields(result_spec)
        return size, msg_type, method, seq_id, value

    def unpack_request(self, msg):
        size, msg_type, method, seq_id = self.protocol.unpack_message_header(msg)
        if method not in self.method_specs:
            raise Exception('Unpack req failed: method %s not defined in %s'
                            % (method, self.service))
        args_spec = self.method_specs[method][0]
        value = self.protocol.read_fields(args_spec)
        return size, msg_type, method, seq_id, value
