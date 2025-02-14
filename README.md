# Distributed Systems Exercies

A collection of short exercises working with fundamental aspects of distributed systems. I practiced implementing a vector clock algorithm, a leader election cycle algorithm, a client/server application using gRPC, and a Causal Length Set (CLS, a type of conflict-free replicated datatype).

## Technologies
- Python
- gRPC

## How to Run
1. Clone the repository: 'git clone https://github.com/scottbarcomb/Distributed-Systems-Exercises'
2. Run each program: 'python ./...'

⚠️ Extra steps are required to run the client/server application, which is detailed in its section of the readme.

## Features
- An implmentation of a Causal Length Set, a type of CRDT (conflict free replicated datatype).
- A client/server application using remote procedure calls (gRPC).
- An implementation of the consensus algorithm for nodes in a distributed system.
- An implementation of a vector clock algorithm to represent the causality of Git commits.

## [Client/Server](ClientServer)
1. To run this application, ensure you have the grpcio and grpcio-tools packages installed.
2. Build the gRPC Python classes using the .proto files:
  - python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. data.proto
  - python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hash.proto
3. Run the server: 'python hash_server.py'
4. Run the client: 'python client.py'
5. The client will connect to the data server, register the user, store the data, and get the hash value of the data from the hash server.
