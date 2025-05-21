from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OUTPUT_FORMAT_UNSPECIFIED: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_PNG: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_WEBP_STATIC: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_WEBP_ANIMATED: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_GIF: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_WEBM: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_SVG: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_TGS_RAW: _ClassVar[OutputFormat]
    OUTPUT_FORMAT_PNG_SEQUENCE: _ClassVar[OutputFormat]
OUTPUT_FORMAT_UNSPECIFIED: OutputFormat
OUTPUT_FORMAT_PNG: OutputFormat
OUTPUT_FORMAT_WEBP_STATIC: OutputFormat
OUTPUT_FORMAT_WEBP_ANIMATED: OutputFormat
OUTPUT_FORMAT_GIF: OutputFormat
OUTPUT_FORMAT_WEBM: OutputFormat
OUTPUT_FORMAT_SVG: OutputFormat
OUTPUT_FORMAT_TGS_RAW: OutputFormat
OUTPUT_FORMAT_PNG_SEQUENCE: OutputFormat

class GetStickerRequest(_message.Message):
    __slots__ = ("sticker_file_id", "is_animated", "is_video", "desired_format")
    STICKER_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    IS_ANIMATED_FIELD_NUMBER: _ClassVar[int]
    IS_VIDEO_FIELD_NUMBER: _ClassVar[int]
    DESIRED_FORMAT_FIELD_NUMBER: _ClassVar[int]
    sticker_file_id: str
    is_animated: bool
    is_video: bool
    desired_format: OutputFormat
    def __init__(self, sticker_file_id: _Optional[str] = ..., is_animated: bool = ..., is_video: bool = ..., desired_format: _Optional[_Union[OutputFormat, str]] = ...) -> None: ...

class StickerFileMetadata(_message.Message):
    __slots__ = ("input_file_id", "content_type", "actual_format")
    INPUT_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    input_file_id: str
    content_type: str
    actual_format: OutputFormat
    def __init__(self, input_file_id: _Optional[str] = ..., content_type: _Optional[str] = ..., actual_format: _Optional[_Union[OutputFormat, str]] = ...) -> None: ...

class StickerFileChunk(_message.Message):
    __slots__ = ("metadata", "data_chunk")
    METADATA_FIELD_NUMBER: _ClassVar[int]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    metadata: StickerFileMetadata
    data_chunk: bytes
    def __init__(self, metadata: _Optional[_Union[StickerFileMetadata, _Mapping]] = ..., data_chunk: _Optional[bytes] = ...) -> None: ...

class GetStickerSetRequest(_message.Message):
    __slots__ = ("sticker_set_name", "desired_format_for_all")
    STICKER_SET_NAME_FIELD_NUMBER: _ClassVar[int]
    DESIRED_FORMAT_FOR_ALL_FIELD_NUMBER: _ClassVar[int]
    sticker_set_name: str
    desired_format_for_all: OutputFormat
    def __init__(self, sticker_set_name: _Optional[str] = ..., desired_format_for_all: _Optional[_Union[OutputFormat, str]] = ...) -> None: ...

class StickerInSetHeader(_message.Message):
    __slots__ = ("input_file_id", "content_type", "actual_format")
    INPUT_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    input_file_id: str
    content_type: str
    actual_format: OutputFormat
    def __init__(self, input_file_id: _Optional[str] = ..., content_type: _Optional[str] = ..., actual_format: _Optional[_Union[OutputFormat, str]] = ...) -> None: ...

class StickerProcessingError(_message.Message):
    __slots__ = ("input_file_id", "error_message")
    INPUT_FILE_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    input_file_id: str
    error_message: str
    def __init__(self, input_file_id: _Optional[str] = ..., error_message: _Optional[str] = ...) -> None: ...

class StickerSetItem(_message.Message):
    __slots__ = ("header", "data_chunk", "error")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_CHUNK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: StickerInSetHeader
    data_chunk: bytes
    error: StickerProcessingError
    def __init__(self, header: _Optional[_Union[StickerInSetHeader, _Mapping]] = ..., data_chunk: _Optional[bytes] = ..., error: _Optional[_Union[StickerProcessingError, _Mapping]] = ...) -> None: ...
