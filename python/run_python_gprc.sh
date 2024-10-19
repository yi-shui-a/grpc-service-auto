#!/bin/bash
#protoc -I ../protos/ ../protos/my_service.proto --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=`which grpc_cpp_plugin`
python -m grpc_tools.protoc -I ../protos/ ../protos/my_service.proto --python_out=. --grpc_python_out=.

