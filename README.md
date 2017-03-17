# jsonthrift [![Build Status](https://travis-ci.org/WKPlus/jsonthrift.svg?branch=master)](https://travis-ci.org/WKPlus/jsonthrift)

  jsonthrift is a python module for convert json data to thrift binary data and verse vice.


## Usage
  You can use it like this:

```
transport = 'TBufferedTransport'
protocol = 'TBinaryProtocol'
thrift_file = 'thrift_tutorial/tutorial.thrift'
service = 'Calculator'
method = 'add'
params = {"num1": 1, "num2": 3}

jt = JsonThrift(transport, protocol, thrift_file, service, method)
msg = jt.pack_request(params, 1)
# call remote server, get response
result = jt.unpack_response(response)[4]
# unpack_response returns a tuple, which contains: 
#   message size(TFramedTransport)/None(TBufferedTransport),
#   message type, will be 2 for thrift REPLY message
#   method
#   sequence id
#   return value
print result
# result is {"success": 4}

```
