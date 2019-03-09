"""Generates protocol messages and gRPC stubs."""

from grpc_tools import protoc

protoc.main((
    '',
    '-I=./proto',
    '--python_out=.',
    '--grpc_python_out=.',
    './proto/helloworld.proto',
))

print('conversion from proto -> .py complete')