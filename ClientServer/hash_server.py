from concurrent import futures
import grpc
import hashlib

import hash_pb2
import hash_pb2_grpc
import data_pb2
import data_pb2_grpc


class HSServicer(hash_pb2_grpc.HSServicer):
    def GetHash(self, request, context):
        passcode = request.passcode
        ip = request.ip
        port = request.port

        # Connect to Data Server
        data_server_address = f'{ip}:{port}'
        channel = grpc.insecure_channel(data_server_address)
        data_stub = data_pb2_grpc.DBStub(channel)

        # Retrieve data using passcode
        passcode_msg = data_pb2.Passcode(code=passcode)
        try:
            response = data_stub.GetAuthData(passcode_msg)
            data = response.msg
        except grpc.RpcError as e:
            context.set_details(f"Error retrieving data: {e.details()}")
            context.set_code(e.code())
            return hash_pb2.Response()

        # Calculate hash of the data
        data_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()

        # Return the hash
        return hash_pb2.Response(hash=data_hash)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hash_pb2_grpc.add_HSServicer_to_server(HSServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Hash Server is running on port 50052.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()