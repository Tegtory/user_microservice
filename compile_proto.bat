@echo off

echo [1/3] Copying files...
mkdir protos\user
copy protos\auth.proto protos\user

echo [2/3] Generating proto...
python -m grpc_tools.protoc --proto_path=./protos/ --python_out=. --grpc_python_out=. user/auth.proto

echo [3/3] Removing files...
rmdir protos\user /s /q

echo Competed!
