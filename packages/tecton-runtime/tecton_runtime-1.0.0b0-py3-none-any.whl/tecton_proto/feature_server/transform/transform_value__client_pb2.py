# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/feature_server/transform/transform_value__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nCtecton_proto/feature_server/transform/transform_value__client.proto\x12%tecton_proto.feature_server.transform\x1a\x1fgoogle/protobuf/timestamp.proto\"\x84\x04\n\x0eTransformValue\x12]\n\x0b\x61rray_value\x18\x01 \x01(\x0b\x32:.tecton_proto.feature_server.transform.ArrayTransformValueH\x00R\narrayValue\x12W\n\tmap_value\x18\x02 \x01(\x0b\x32\x38.tecton_proto.feature_server.transform.MapTransformValueH\x00R\x08mapValue\x12%\n\rfloat64_value\x18\x03 \x01(\x01H\x00R\x0c\x66loat64Value\x12!\n\x0bint64_value\x18\x04 \x01(\x03H\x00R\nint64Value\x12\x1f\n\nbool_value\x18\x05 \x01(\x08H\x00R\tboolValue\x12#\n\x0cstring_value\x18\x06 \x01(\tH\x00R\x0bstringValue\x12Z\n\nnull_value\x18\x07 \x01(\x0b\x32\x39.tecton_proto.feature_server.transform.NullTransformValueH\x00R\tnullValue\x12\x45\n\x0ftimestamp_value\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R\x0etimestampValueB\x07\n\x05value\"\x14\n\x12NullTransformValue\"h\n\x13\x41rrayTransformValue\x12Q\n\x08\x65lements\x18\x01 \x03(\x0b\x32\x35.tecton_proto.feature_server.transform.TransformValueR\x08\x65lements\"\xec\x01\n\x11MapTransformValue\x12\x63\n\tvalue_map\x18\x01 \x03(\x0b\x32\x46.tecton_proto.feature_server.transform.MapTransformValue.ValueMapEntryR\x08valueMap\x1ar\n\rValueMapEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12K\n\x05value\x18\x02 \x01(\x0b\x32\x35.tecton_proto.feature_server.transform.TransformValueR\x05value:\x02\x38\x01\x42<Z:github.com/tecton-ai/tecton_proto/feature_server/transform')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.feature_server.transform.transform_value__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z:github.com/tecton-ai/tecton_proto/feature_server/transform'
  _MAPTRANSFORMVALUE_VALUEMAPENTRY._options = None
  _MAPTRANSFORMVALUE_VALUEMAPENTRY._serialized_options = b'8\001'
  _TRANSFORMVALUE._serialized_start=144
  _TRANSFORMVALUE._serialized_end=660
  _NULLTRANSFORMVALUE._serialized_start=662
  _NULLTRANSFORMVALUE._serialized_end=682
  _ARRAYTRANSFORMVALUE._serialized_start=684
  _ARRAYTRANSFORMVALUE._serialized_end=788
  _MAPTRANSFORMVALUE._serialized_start=791
  _MAPTRANSFORMVALUE._serialized_end=1027
  _MAPTRANSFORMVALUE_VALUEMAPENTRY._serialized_start=913
  _MAPTRANSFORMVALUE_VALUEMAPENTRY._serialized_end=1027
# @@protoc_insertion_point(module_scope)
