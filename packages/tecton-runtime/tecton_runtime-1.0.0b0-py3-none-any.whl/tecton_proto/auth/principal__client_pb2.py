# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/auth/principal__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)tecton_proto/auth/principal__client.proto\x12\x11tecton_proto.auth\"d\n\tPrincipal\x12G\n\x0eprincipal_type\x18\x01 \x01(\x0e\x32 .tecton_proto.auth.PrincipalTypeR\rprincipalType\x12\x0e\n\x02id\x18\x02 \x01(\tR\x02id\"\x9f\x02\n\x0ePrincipalBasic\x12\x32\n\x04user\x18\x03 \x01(\x0b\x32\x1c.tecton_proto.auth.UserBasicH\x00R\x04user\x12Q\n\x0fservice_account\x18\x04 \x01(\x0b\x32&.tecton_proto.auth.ServiceAccountBasicH\x00R\x0eserviceAccount\x12\x35\n\x05group\x18\x05 \x01(\x0b\x32\x1d.tecton_proto.auth.GroupBasicH\x00R\x05group\x12\x41\n\tworkspace\x18\x06 \x01(\x0b\x32!.tecton_proto.auth.WorkspaceBasicH\x00R\tworkspaceB\x0c\n\nbasic_info\"\xe9\x01\n\x13ServiceAccountBasic\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x1b\n\tis_active\x18\x04 \x01(\x08R\x08isActive\x12\x36\n\x07\x63reator\x18\x05 \x01(\x0b\x32\x1c.tecton_proto.auth.PrincipalR\x07\x63reator\x12\x37\n\x05owner\x18\x06 \x01(\x0b\x32!.tecton_proto.auth.PrincipalBasicR\x05owner\"\x81\x01\n\tUserBasic\x12\x17\n\x07okta_id\x18\x01 \x01(\tR\x06oktaId\x12\x1d\n\nfirst_name\x18\x02 \x01(\tR\tfirstName\x12\x1b\n\tlast_name\x18\x03 \x01(\tR\x08lastName\x12\x1f\n\x0blogin_email\x18\x04 \x01(\tR\nloginEmail\"0\n\nGroupBasic\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\"$\n\x0eWorkspaceBasic\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name*\xa4\x01\n\rPrincipalType\x12\x1e\n\x1aPRINCIPAL_TYPE_UNSPECIFIED\x10\x00\x12\x17\n\x13PRINCIPAL_TYPE_USER\x10\x01\x12\"\n\x1ePRINCIPAL_TYPE_SERVICE_ACCOUNT\x10\x02\x12\x18\n\x14PRINCIPAL_TYPE_GROUP\x10\x03\x12\x1c\n\x18PRINCIPAL_TYPE_WORKSPACE\x10\x04\x42;\n\x0f\x63om.tecton.authP\x01Z&github.com/tecton-ai/tecton_proto/auth')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.auth.principal__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.authP\001Z&github.com/tecton-ai/tecton_proto/auth'
  _PRINCIPALTYPE._serialized_start=913
  _PRINCIPALTYPE._serialized_end=1077
  _PRINCIPAL._serialized_start=64
  _PRINCIPAL._serialized_end=164
  _PRINCIPALBASIC._serialized_start=167
  _PRINCIPALBASIC._serialized_end=454
  _SERVICEACCOUNTBASIC._serialized_start=457
  _SERVICEACCOUNTBASIC._serialized_end=690
  _USERBASIC._serialized_start=693
  _USERBASIC._serialized_end=822
  _GROUPBASIC._serialized_start=824
  _GROUPBASIC._serialized_end=872
  _WORKSPACEBASIC._serialized_start=874
  _WORKSPACEBASIC._serialized_end=910
# @@protoc_insertion_point(module_scope)
