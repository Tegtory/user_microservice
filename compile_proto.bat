@echo off

python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. protos/user/*.proto

echo Competed!
