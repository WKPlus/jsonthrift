# -*- coding:utf-8 -*-
from StringIO import StringIO


class TTransport(object):
    def __init__(self):
        self._buf = []

    def write(self, s):
        self._buf.append(s)

    def reset(self):
        self._buf = []

    def pack_message(self):
        return ''.join(self._buf)

    def unpack_message(self, msg):
        self._msg = StringIO(msg)
        return None

    def read(self, size):
        return self._msg.read(size)
