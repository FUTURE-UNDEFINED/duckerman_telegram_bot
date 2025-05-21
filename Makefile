generate-proto-stickers-converter:
	python -m grpc_tools.protoc \
	-I protos \
	--python_out=src/generated \
	--pyi_out=src/generated \
	--grpc_python_out=src/generated \
	protos/v1/telegram_stickers_converter/telegram_stickers_converter.proto

update-submodules:
	git submodule update --recursive --remote --merge


generate-all: generate-proto-stickers-converter