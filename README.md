# jsonthrift [![Build Status](https://travis-ci.org/WKPlus/jsonthrift.svg?branch=master)](https://travis-ci.org/WKPlus/jsonthrift)

  jsonthrift is a python module for convert json data to thrift binary data and verse vice.


## Usage
  You can use it like this:

```python
     >>> transport = 'TBufferedTransport'
     >>> protocol = 'TBinaryProtocol'
     >>> thrift_file = 'tutorial.thrift'
     >>> service = 'Calculator'
     >>> method = 'add'
     >>> params = {'num1': 1, 'num2': 3}

     >>> jt = JsonThrift(transport, protocol, thrift_file, service, method)
     >>> msg = jt.pack_request(params, 1)
     >>> response = send_and_recv(msg) # send msg to server, receive response
     >>> result = jt.unpack_response(response)[4]
     >>> print result
     {'success': 4}

     >>> method = 'calculate'
     >>> params = {'logid': 1, 'w':{'op': 4, 'num1': 1, 'num2': 0}}
     >>> msg = jt.pack_request(params, 2)
     >>> response = send_and_recv(msg) # send msg to server, receive response
     >>> result = jt.unpack_response(response)[4]
     >>> print result
     {'ouch': {'whatOp': 4, 'why': 'Cannot divide by 0'}}

     >>> # unpack_response returns a tuple, which contains:
     >>> #   message size(TFramedTransport)/None(TBufferedTransport),
     >>> #   message type, will be 2 for thrift REPLY message
     >>> #   method
     >>> #   sequence id
     >>> #   return value

```
