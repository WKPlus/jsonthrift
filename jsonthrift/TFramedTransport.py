# -*- coding:utf-8 -*-
from .TTransport import TTransport
from struct import pack, unpack
from StringIO import StringIO


class TFramedTransport(TTransport):
    def __init__(self):
        super(TFramedTransport, self).__init__()

    def pack_message(self):
        msg = ''.join(self._buf)
        return pack('!i', len(msg)) + msg

    def unpack_message(self, msg):
        self._msg = StringIO(msg)
        size, = unpack('!i', self._msg.read(4))
        return size
