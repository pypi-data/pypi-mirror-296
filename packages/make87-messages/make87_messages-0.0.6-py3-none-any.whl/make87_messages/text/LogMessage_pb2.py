# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: text/LogMessage.proto
# Protobuf Python Version: 5.28.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    0,
    '',
    'text/LogMessage.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15text/LogMessage.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x97\x02\n\nLogMessage\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12#\n\x05level\x18\x02 \x01(\x0e\x32\x14.LogMessage.LogLevel\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x11\n\tfile_name\x18\x05 \x01(\t\x12\x13\n\x0bline_number\x18\x06 \x01(\x05\x12\x12\n\nprocess_id\x18\x07 \x01(\x03\x12\x11\n\tthread_id\x18\x08 \x01(\x03\"E\n\x08LogLevel\x12\t\n\x05\x44\x45\x42UG\x10\x00\x12\x08\n\x04INFO\x10\x01\x12\x0b\n\x07WARNING\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x0c\n\x08\x43RITICAL\x10\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'text.LogMessage_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_LOGMESSAGE']._serialized_start=59
  _globals['_LOGMESSAGE']._serialized_end=338
  _globals['_LOGMESSAGE_LOGLEVEL']._serialized_start=269
  _globals['_LOGMESSAGE_LOGLEVEL']._serialized_end=338
# @@protoc_insertion_point(module_scope)
