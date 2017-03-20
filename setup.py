try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.1.0'

LONG_DESCRIPTION = '''
jsonthrift is implemented for serializing and deserializing json to/from thrift.

Usage
-----

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


'''

setup(
    name='jsonthrift',
    description='a package for serializing json to/from thrift',
    long_description=LONG_DESCRIPTION,
    author='WKPlus',
    url='https://github.com/WKPlus/jsonthrift',
    license='MIT',
    author_email='qifa.zhao@gmail.com',
    version=VERSION,
    packages = ['jsonthrift'],
    install_requires=['thrift', 'thriftpy'],
    test_requires=['nose'],
    zip_safe=False,
)
