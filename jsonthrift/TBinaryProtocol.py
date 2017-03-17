# -*- coding:utf-8 -*-
from struct import pack, unpack
from functools import partial
from .TTypes import DataType
from types import StringType, UnicodeType


class TBinaryProtocol(object):
    _TYPE_TRANSFORMER = {
        DataType.I32: {
            "accept": set([StringType, UnicodeType]),
            "transformer": int,
        }
    }
    VERSION = -2147418112
    VERSION_MASK = -65536
    TYPE_MASK = 0x000000ff

    def __init__(self, transport):
        self.transport = transport

        self.write_byte = partial(self.basic_write, "!b")
        self.write_i16 = partial(self.basic_write, "!h")
        self.write_i32 = partial(self.basic_write, "!i")
        self.write_i64 = partial(self.basic_write, "!q")
        self.write_double = partial(self.basic_write, "!d")
        self.basic_writers = {
            DataType.BOOL: self.write_bool,
            DataType.BYTE: self.write_byte,
            DataType.DOUBLE: self.write_double,
            DataType.I16: self.write_i16,
            DataType.I32: self.write_i32,
            DataType.I64: self.write_i64,
            DataType.STRING: self.write_str,
        }

        self.read_byte = partial(self.basic_read, "!b", 1)
        self.read_i16 = partial(self.basic_read, "!h", 2)
        self.read_i32 = partial(self.basic_read, "!i", 4)
        self.read_i64 = partial(self.basic_read, "!q", 8)
        self.read_double = partial(self.basic_read, "!d", 8)
        self.basic_readers = {
            DataType.BOOL: self.read_bool,
            DataType.BYTE: self.read_byte,
            DataType.DOUBLE: self.read_double,
            DataType.I16: self.read_i16,
            DataType.I32: self.read_i32,
            DataType.I64: self.read_i64,
            DataType.STRING: self.read_str,
        }

    def basic_write(self, fmt, value):
        '''
        implementation for bool, byte, i16, i32, i64, double
        fmt should be:
            byte: !b, i16: !h, i32: !i, i64: !q, double: !d,
        '''
        self.transport.write(pack(fmt, value))

    def write_bool(self, value):
        self.write_byte(1 if value else 0)

    def write_str(self, _str):
        if isinstance(_str, unicode):
            _str = _str.encode('utf8')
        self.write_i32(len(_str))
        self.transport.write(_str)

    def write_list_or_set(self, thrift_spec, values):
        ttype, elem_spec = self.extract_ttype(thrift_spec)
        self.write_byte(ttype)
        self.write_i32(len(values))
        for v in values:
            self.write_value(ttype, elem_spec, v)

    def extract_ttype(self, thrift_spec):
        if not isinstance(thrift_spec, tuple):
            # basic type, thrift_spec is ttype
            ttype, spec = thrift_spec, None
        else:
            # non-basic type, thrift_spec[0] is ttype
            ttype, spec = thrift_spec[0], thrift_spec[1]
        return ttype, spec

    def write_map(self, thrift_spec, values):
        key_ttype, key_spec = self.extract_ttype(thrift_spec[0])
        value_ttype, value_spec = self.extract_ttype(thrift_spec[1])
        self.write_byte(key_ttype)
        self.write_byte(value_ttype)
        self.write_i32(len(values))
        for k, v in values.iteritems():
            self.write_value(key_ttype, key_spec, k)
            self.write_value(value_ttype, value_spec, v)

    def write_struct(self, _class, value):
        self.write_fields(_class.thrift_spec, value)
        self.write_byte(DataType.STOP)

    def verify_value(self, ttype, value):
        # verify field value type according to thrift spec
        # struct type must be {}
        #
        if ttype not in TBinaryProtocol._TYPE_TRANSFORMER:
            return value
        transformer = TBinaryProtocol._TYPE_TRANSFORMER[ttype]
        if type(value) not in transformer["accept"]:
            return value
        return transformer["transformer"](value)

    def write_field(self, ttype, thrift_spec, _id, value):
        self.write_byte(ttype)
        self.write_i16(_id)
        self.write_value(ttype, thrift_spec, value)

    def write_value(self, ttype, thrift_spec, value):
        value = self.verify_value(ttype, value)

        if ttype in DataType.BASIC_TYPES:
            self.basic_writers[ttype](value)
        elif ttype == DataType.STRUCT:
            self.write_struct(thrift_spec, value)
        elif ttype == DataType.LIST or ttype == DataType.SET:
            self.write_list_or_set(thrift_spec, value)
        elif ttype == DataType.MAP:
            self.write_map(thrift_spec, value)
        else:
            raise Exception("Not supported ttype: %s" % ttype)

    def write_fields(self, thrift_spec, values):
        for _id, field in thrift_spec.iteritems():
            # thrift_spec as follows:
            # {1: (8, 'empId', True), 2: (10, 'poiId', True)}
            # {1: (12, 'conditionTO', <class 'SearchModel.conditionTO'>, True)}
            # {1: (15, 'cityTOs', (12, <class 'Model.CityTO'>), False)}
            # {1: (13, 'poiHardwareList', (11, 8), True)}
            # {1: (15, 'workOrderProcessTOs', 8, False)}
            ttype = field[0]
            name = field[1]
            required = field[-1]
            if required and name not in values:
                raise Exception("Required field [%s] not in json data" % name)
            if name not in values:
                # verify passed, but name does not exist in values
                # it must be an optional field, skip
                continue
            if ttype in DataType.BASIC_TYPES:
                field_spec = None
            elif ttype in DataType.COLLECTIONS:
                field_spec = field[2]
            else:
                raise Exception("Not supported data type: %s" % ttype)
            self.write_field(ttype, field_spec, _id, values[name])

    def write_message_begin(self, msg_type, method, seq_id):
        self.write_i32(TBinaryProtocol.VERSION | msg_type)
        self.write_str(method)
        self.write_i32(seq_id)

    def write_message_end(self):
        self.write_byte(DataType.STOP)

    def pack_message(self, msg_type, method, seq_id, thrift_spec, values):
        self.transport.reset()
        self.write_message_begin(msg_type, method, seq_id)
        self.write_fields(thrift_spec, values)
        self.write_message_end()
        return self.transport.pack_message()

    def unpack_message(self, thrift_spec, msg):
        size = self.transport.unpack_message(msg)
        msg_type, method, seq_id = self.read_message_begin()
        values = self.read_fields(thrift_spec)
        # read_fields will read message end
        # no need to read message end here
        # self.read_message_end()
        return size, msg_type, method, seq_id, values

    def read_message_begin(self):
        msg_type = self.read_i32() & TBinaryProtocol.TYPE_MASK
        method = self.read_str()
        seq_id = self.read_i32()
        return msg_type, method, seq_id

    def read_message_end(self):
        assert self.read_byte() == 0

    def read_fields(self, thrift_spec):
        values = {}
        while 1:
            ttype = self.read_byte()
            if ttype == DataType.STOP:
                break
            _id = self.read_i16()
            spec = thrift_spec[_id]
            name = spec[1]
            value = self.read_value(ttype, spec[2])
            values[name] = value
        return values

    def read_value(self, ttype, spec):
        if ttype in self.basic_readers:
            return self.basic_readers[ttype]()
        elif ttype == DataType.LIST or ttype == DataType.SET:
            return self.read_list_or_set(spec)
        elif ttype == DataType.MAP:
            return self.read_map(spec)
        elif ttype == DataType.STRUCT:
            return self.read_struct(spec)
        else:
            raise Exception("Not supported ttype: %s" % ttype)

    def basic_read(self, fmt, size):
        return unpack(fmt, self.transport.read(size))[0]

    def read_bool(self):
        return self.read_byte() != 0

    def read_str(self):
        length = self.read_i32()
        return self.transport.read(length)

    def read_struct(self, _class):
        return self.read_fields(_class.thrift_spec)

    def read_list_or_set(self, list_spec):
        type_spec, elem_spec = self.extract_ttype(list_spec)
        ttype = self.read_byte()
        length = self.read_i32()
        return [self.read_value(ttype, elem_spec) for i in xrange(length)]

    def read_map(self, map_spec):
        key_ttype, key_spec = self.extract_ttype(map_spec[0])
        value_ttype, value_spec = self.extract_ttype(map_spec[1])
        key_ttype = self.read_byte()
        value_ttype = self.read_byte()
        length = self.read_i32()
        ret = {}
        for i in xrange(length):
            k = self.read_value(key_ttype, key_spec)
            v = self.read_value(value_ttype, value_spec)
            ret[k] = v
        return ret
