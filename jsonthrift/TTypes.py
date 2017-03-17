#-*- coding:utf-8 -*-


class Byte(object):
    '''represents thrift byte type'''
    __slots__ = ['_value']
    def __init__(self, value):
        self._value = value


class Int16(object):
    '''represents thrift i16 type'''
    __slots__ = ['_value']
    def __init__(self, value):
        self._value = value


class Binary(object):
    '''represents thrift binary type'''
    __slots__ = ['_value']
    def __init__(self, value):
        self._value = value


class Struct(object):
    '''represents thrift struct type'''
    __slots__ = ['_value']
    def __init__(self, value):
        self._value = value


class DataType:
    STOP = 0 #
    VOID = 1 #
    BOOL = 2
    BYTE = 3
    I08 = 3
    DOUBLE = 4
    I16 = 6
    I32 = 8
    I64 = 10
    STRING = 11
    UTF7 = 11
    STRUCT = 12
    MAP = 13
    SET = 14
    LIST = 15
    UTF8 = 16 #
    UTF16 = 17 #

    COLLECTIONS = set((SET, LIST, MAP, STRUCT))
    BASIC_TYPES = set((BYTE, BOOL, DOUBLE, I16, I32, I64, STRING))


class TMessageType:
    CALL = 1
    REPLY = 2
    EXCEPTION = 3
    ONEWAY = 4
