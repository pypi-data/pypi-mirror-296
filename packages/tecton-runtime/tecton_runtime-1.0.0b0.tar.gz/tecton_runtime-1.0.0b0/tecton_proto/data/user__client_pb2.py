# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/user__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$tecton_proto/data/user__client.proto\x12\x11tecton_proto.data\x1a\x1fgoogle/protobuf/timestamp.proto\"\xae\x02\n\x04User\x12\x17\n\x07okta_id\x18\x01 \x01(\tR\x06oktaId\x12\x1d\n\nfirst_name\x18\x02 \x01(\tR\tfirstName\x12\x1b\n\tlast_name\x18\x03 \x01(\tR\x08lastName\x12\x1f\n\x0blogin_email\x18\x04 \x01(\tR\nloginEmail\x12\x1f\n\x0bokta_status\x18\x05 \x01(\tR\noktaStatus\x12\x39\n\ncreated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x19\n\x08is_admin\x18\x07 \x01(\x08R\x07isAdmin\x12\x39\n\nlast_login\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tlastLoginB\x13\n\x0f\x63om.tecton.dataP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.data.user__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.dataP\001'
  _USER._serialized_start=93
  _USER._serialized_end=395
# @@protoc_insertion_point(module_scope)
