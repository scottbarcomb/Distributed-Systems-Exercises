import grpc

import data_pb2
import data_pb2_grpc
import hash_pb2
import hash_pb2_grpc

def main():
    # User details
    username = 'scott.barcomb'
    password = 'SuperSecurePassword'
    message = 'Go Gators!'

    # Data Server details
    data_server_ip = '46.249.101.244'
    data_server_port = 50051
    data_server_address = f'{data_server_ip}:{data_server_port}'

    # Connect to Data Server
    data_channel = grpc.insecure_channel(data_server_address)
    data_stub = data_pb2_grpc.DBStub(data_channel)

    # Register User
    user_pass = data_pb2.UserPass(username=username, password=password)
    response = data_stub.RegisterUser(user_pass)
    if response.success:
        print("Registration successful.") # Only works if user not previously registered.
    else:
        print("Registration failed.") # If user already registered, it fails but GenPasscode still works.

    # Store Data
    store_req = data_pb2.StoreReq(
        username=username,
        password=password,
        msg=message
    )
    response = data_stub.StoreData(store_req)
    if response.success:
        print("Data stored successfully.")
    else:
        print("Data store request failed.")

    # Generate Passcode
    passcode_response = data_stub.GenPasscode(user_pass)
    passcode = passcode_response.code
    print(f"Generated passcode: {passcode}")

    # Hash Server details
    hash_server_address = 'localhost:50052'

    # Connect to Hash Server
    hash_channel = grpc.insecure_channel(hash_server_address)
    hash_stub = hash_pb2_grpc.HSStub(hash_channel)

    # Prepare request for Hash Server
    hash_request = hash_pb2.Request(
        passcode=passcode,
        ip=data_server_ip,
        port=data_server_port
    )

    # Get hash value
    try:
        hash_response = hash_stub.GetHash(hash_request)
        print(f"Hash value for the data: {hash_response.hash}")
    except grpc.RpcError as e:
        print(f"Failed to get hash value: {e.details()}")


if __name__ == '__main__':
    main()