import grpc.aio
from v1.telegram_stickers_converter.telegram_stickers_converter_pb2_grpc import StickerConverterServiceStub

channel = grpc.aio.insecure_channel('localhost:5051')
tg_stick_conv_client = StickerConverterServiceStub(channel)
