# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/auth/resource_role_assignments__client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.auth import resource__client_pb2 as tecton__proto_dot_auth_dot_resource____client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n9tecton_proto/auth/resource_role_assignments__client.proto\x12\x11tecton_proto.auth\x1a(tecton_proto/auth/resource__client.proto\"\xe8\x01\n\x1aResourceAndRoleAssignments\x12\x44\n\rresource_type\x18\x03 \x01(\x0e\x32\x1f.tecton_proto.auth.ResourceTypeR\x0cresourceType\x12\x1f\n\x0bresource_id\x18\x01 \x01(\tR\nresourceId\x12\x14\n\x05roles\x18\x02 \x03(\tR\x05roles\x12M\n\rroles_granted\x18\x04 \x03(\x0b\x32(.tecton_proto.auth.RoleAssignmentSummaryR\x0crolesGranted\"\xd4\x01\n\x1cResourceAndRoleAssignmentsV2\x12\x44\n\rresource_type\x18\x01 \x01(\x0e\x32\x1f.tecton_proto.auth.ResourceTypeR\x0cresourceType\x12\x1f\n\x0bresource_id\x18\x02 \x01(\tR\nresourceId\x12M\n\rroles_granted\x18\x03 \x03(\x0b\x32(.tecton_proto.auth.RoleAssignmentSummaryR\x0crolesGranted\"\xc6\x01\n\x14RoleAssignmentSource\x12N\n\x0f\x61ssignment_type\x18\x01 \x01(\x0e\x32%.tecton_proto.auth.RoleAssignmentTypeR\x0e\x61ssignmentType\x12\x30\n\x14principal_group_name\x18\x02 \x01(\tR\x12principalGroupName\x12,\n\x12principal_group_id\x18\x03 \x01(\tR\x10principalGroupId\"\x8c\x01\n\x15RoleAssignmentSummary\x12\x12\n\x04role\x18\x01 \x01(\tR\x04role\x12_\n\x17role_assignment_sources\x18\x02 \x03(\x0b\x32\'.tecton_proto.auth.RoleAssignmentSourceR\x15roleAssignmentSources*\x8a\x01\n\x12RoleAssignmentType\x12$\n ROLE_ASSIGNMENT_TYPE_UNSPECIFIED\x10\x00\x12\x1f\n\x1bROLE_ASSIGNMENT_TYPE_DIRECT\x10\x01\x12-\n)ROLE_ASSIGNMENT_TYPE_FROM_PRINCIPAL_GROUP\x10\x02\x42J\n\x0f\x63om.tecton.authP\x01Z5github.com/tecton-ai/tecton_proto/auth/resource_roles')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tecton_proto.auth.resource_role_assignments__client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017com.tecton.authP\001Z5github.com/tecton-ai/tecton_proto/auth/resource_roles'
  _ROLEASSIGNMENTTYPE._serialized_start=917
  _ROLEASSIGNMENTTYPE._serialized_end=1055
  _RESOURCEANDROLEASSIGNMENTS._serialized_start=123
  _RESOURCEANDROLEASSIGNMENTS._serialized_end=355
  _RESOURCEANDROLEASSIGNMENTSV2._serialized_start=358
  _RESOURCEANDROLEASSIGNMENTSV2._serialized_end=570
  _ROLEASSIGNMENTSOURCE._serialized_start=573
  _ROLEASSIGNMENTSOURCE._serialized_end=771
  _ROLEASSIGNMENTSUMMARY._serialized_start=774
  _ROLEASSIGNMENTSUMMARY._serialized_end=914
# @@protoc_insertion_point(module_scope)
