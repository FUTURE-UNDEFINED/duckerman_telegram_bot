generate-proto-stickers-converter:
	python -m grpc_tools.protoc \
	-I protos \
	--python_out=src/ \
	--pyi_out=src/ \
	--grpc_python_out=src/ \
	protos/generated/telegram_stickers_converter/telegram_stickers_converter.proto

update-submodules:
	git submodule update --recursive --remote --merge


generate-all: generate-proto-stickers-converter