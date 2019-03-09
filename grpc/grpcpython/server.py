import logging
import time
from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        print('Send: Hello, %s!' % request.name)
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    # read in certificate
    trusted_file = 'keys/ca.crt'
    keyfile = 'keys/server.key'
    certfile = 'keys/server.crt'

    try:
        with open(trusted_file, 'rb') as f:
            trusted_certs = f.read()
        
        with open(keyfile, 'rb') as f:
            server_key = f.read()

        with open(certfile, 'rb') as f:
            server_cert = f.read()


    except Exception as e:
        log.error('failed-to-read-cert-keys', reason=e)

    # create credentials

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    
    server_cred = grpc.ssl_server_credentials([(server_key, server_cert)], trusted_certs)
    server.add_secure_port('localhost:50051', server_cred)
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()