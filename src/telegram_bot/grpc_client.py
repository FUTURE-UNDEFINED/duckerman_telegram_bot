import grpc.aio
from generated.telegram_stickers_converter.telegram_stickers_converter_pb2_grpc import StickerConverterServiceStub

channel = grpc.aio.insecure_channel('localhost:50051')
tg_stick_conv_client = StickerConverterServiceStub(channel)
