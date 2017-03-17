# -*- coding:utf-8 -*-
from .TTransport import TTransport

class TBufferedTransport(TTransport):
    def __init__(self):
        super(TBufferedTransport, self).__init__()
