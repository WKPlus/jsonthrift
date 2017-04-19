# -*- coding:utf-8 -*-
from thriftpy.parser import parse
from .TBinaryProtocol import TBinaryProtocol
from .TBufferedTransport import TBufferedTransport


class ThriftStruct(object):

    PROTOCOLS = {
        'TBinaryProtocol': TBinaryProtocol,
    }

    def __init__(self, thrift_idl, protocol='TBinaryProtocol'):
        if protocol not in self.PROTOCOLS:
            raise Exception('Not supported protocol: %s' % protocol)
        self.protocol = self.PROTOCOLS[protocol](TBufferedTransport())
        self.thrift_idl = thrift_idl
        self._init()

    def _init(self):
        self.struct_specs = self._get_struct_specs()

    def _get_struct_specs(self):
        thrift_meta = parse(self.thrift_idl).__thrift_meta__
        struct_specs = {}
        for s in thrift_meta['structs']:
            sname = '%s.%s' % (s.__module__, s.__name__)
            struct_specs[sname] = s.thrift_spec
        return struct_specs

    def pack_struct(self, struct, data):
        if struct not in self.struct_specs:
            raise Exception('Pack struct failed: struct %s not defined in %s'
                            % (struct, self.thrift_idl))
        return self.protocol.pack_fields(self.struct_specs[struct], data)

    def unpack_struct(self, struct, data):
        if struct not in self.struct_specs:
            raise Exception('Unpack struct failed: struct %s not defined in %s'
                            % (struct, self.thrift_idl))
        return self.protocol.unpack_struct(self.struct_specs[struct], data)
