# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/common/aws_credentials__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1tecton_proto/common/aws_credentials__client.proto\x12\x13tecton_proto.common\x1a\x1fgoogle/protobuf/timestamp.proto\"\xc1\x01\n\x0e\x41wsCredentials\x12\"\n\raccess_key_id\x18\x01 \x01(\tR\x0b\x61\x63\x63\x65ssKeyId\x12*\n\x11secret_access_key\x18\x02 \x01(\tR\x0fsecretAccessKey\x12#\n\rsession_token\x18\x03 \x01(\tR\x0csessionToken\x12:\n\nexpiration\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nexpiration\"\x96\x01\n\nAwsIamRole\x12\x19\n\x08role_arn\x18\x01 \x01(\tR\x07roleArn\x12L\n\x11intermediate_role\x18\x02 \x01(\x0b\x32\x1f.tecton_proto.common.AwsIamRoleR\x10intermediateRole\x12\x1f\n\x0b\x65xternal_id\x18\x03 \x01(\tR\nexternalIdB\x15\n\x11\x63om.tecton.commonP\x01')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.common.aws_credentials__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\021com.tecton.commonP\001'
  _AWSCREDENTIALS._serialized_start=108
  _AWSCREDENTIALS._serialized_end=301
  _AWSIAMROLE._serialized_start=304
  _AWSIAMROLE._serialized_end=454
# @@protoc_insertion_point(module_scope)
