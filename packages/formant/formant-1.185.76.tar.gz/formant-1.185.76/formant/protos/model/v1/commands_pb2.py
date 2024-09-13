# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/model/v1/commands.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from formant.protos.model.v1 import datapoint_pb2 as protos_dot_model_dot_v1_dot_datapoint__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/model/v1/commands.proto',
  package='v1.model',
  syntax='proto3',
  serialized_options=b'Z)github.com/FormantIO/genproto/go/v1/model',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1eprotos/model/v1/commands.proto\x12\x08v1.model\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1fprotos/model/v1/datapoint.proto\"\xa0\x01\n\x0e\x43ommandRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x0e\n\x04text\x18\x03 \x01(\tH\x00\x12\x31\n\rscrubber_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12!\n\x05\x66iles\x18\x05 \x03(\x0b\x32\x12.v1.model.FileInfoB\x0b\n\tparameter\"j\n\x0f\x43ommandResponse\x12\x12\n\nrequest_id\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12(\n\tdatapoint\x18\x03 \x01(\x0b\x32\x13.v1.model.DatapointH\x00\x42\x08\n\x06result\"1\n\x08\x46ileInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\"?\n\x10\x43ommandsMetadata\x12+\n\x08\x63ommands\x18\x01 \x03(\x0b\x32\x19.v1.model.CommandMetadata\"\xf2\x02\n\x0f\x43ommandMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x19\n\x11parameter_enabled\x18\x04 \x01(\x08\x12\x17\n\x0fparameter_value\x18\x05 \x01(\t\x12\x44\n\x0eparameter_meta\x18\x06 \x03(\x0b\x32,.v1.model.CommandMetadata.ParameterMetaEntry\x12\x0f\n\x07\x65nabled\x18\x07 \x01(\x08\x12\n\n\x02id\x18\x08 \x01(\t\x12\x31\n\x04tags\x18\t \x03(\x0b\x32#.v1.model.CommandMetadata.TagsEntry\x1a\x34\n\x12ParameterMetaEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a+\n\tTagsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42+Z)github.com/FormantIO/genproto/go/v1/modelb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,protos_dot_model_dot_v1_dot_datapoint__pb2.DESCRIPTOR,])




_COMMANDREQUEST = _descriptor.Descriptor(
  name='CommandRequest',
  full_name='v1.model.CommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='v1.model.CommandRequest.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='command', full_name='v1.model.CommandRequest.command', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='text', full_name='v1.model.CommandRequest.text', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scrubber_time', full_name='v1.model.CommandRequest.scrubber_time', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='files', full_name='v1.model.CommandRequest.files', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='parameter', full_name='v1.model.CommandRequest.parameter',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=111,
  serialized_end=271,
)


_COMMANDRESPONSE = _descriptor.Descriptor(
  name='CommandResponse',
  full_name='v1.model.CommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_id', full_name='v1.model.CommandResponse.request_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='success', full_name='v1.model.CommandResponse.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='datapoint', full_name='v1.model.CommandResponse.datapoint', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='result', full_name='v1.model.CommandResponse.result',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=273,
  serialized_end=379,
)


_FILEINFO = _descriptor.Descriptor(
  name='FileInfo',
  full_name='v1.model.FileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='v1.model.FileInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='v1.model.FileInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.FileInfo.url', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=381,
  serialized_end=430,
)


_COMMANDSMETADATA = _descriptor.Descriptor(
  name='CommandsMetadata',
  full_name='v1.model.CommandsMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='commands', full_name='v1.model.CommandsMetadata.commands', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=432,
  serialized_end=495,
)


_COMMANDMETADATA_PARAMETERMETAENTRY = _descriptor.Descriptor(
  name='ParameterMetaEntry',
  full_name='v1.model.CommandMetadata.ParameterMetaEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v1.model.CommandMetadata.ParameterMetaEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='v1.model.CommandMetadata.ParameterMetaEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=771,
  serialized_end=823,
)

_COMMANDMETADATA_TAGSENTRY = _descriptor.Descriptor(
  name='TagsEntry',
  full_name='v1.model.CommandMetadata.TagsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v1.model.CommandMetadata.TagsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='v1.model.CommandMetadata.TagsEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=825,
  serialized_end=868,
)

_COMMANDMETADATA = _descriptor.Descriptor(
  name='CommandMetadata',
  full_name='v1.model.CommandMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='v1.model.CommandMetadata.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='command', full_name='v1.model.CommandMetadata.command', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='v1.model.CommandMetadata.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameter_enabled', full_name='v1.model.CommandMetadata.parameter_enabled', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameter_value', full_name='v1.model.CommandMetadata.parameter_value', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parameter_meta', full_name='v1.model.CommandMetadata.parameter_meta', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='v1.model.CommandMetadata.enabled', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='v1.model.CommandMetadata.id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='v1.model.CommandMetadata.tags', index=8,
      number=9, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_COMMANDMETADATA_PARAMETERMETAENTRY, _COMMANDMETADATA_TAGSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=498,
  serialized_end=868,
)

_COMMANDREQUEST.fields_by_name['scrubber_time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_COMMANDREQUEST.fields_by_name['files'].message_type = _FILEINFO
_COMMANDREQUEST.oneofs_by_name['parameter'].fields.append(
  _COMMANDREQUEST.fields_by_name['text'])
_COMMANDREQUEST.fields_by_name['text'].containing_oneof = _COMMANDREQUEST.oneofs_by_name['parameter']
_COMMANDRESPONSE.fields_by_name['datapoint'].message_type = protos_dot_model_dot_v1_dot_datapoint__pb2._DATAPOINT
_COMMANDRESPONSE.oneofs_by_name['result'].fields.append(
  _COMMANDRESPONSE.fields_by_name['datapoint'])
_COMMANDRESPONSE.fields_by_name['datapoint'].containing_oneof = _COMMANDRESPONSE.oneofs_by_name['result']
_COMMANDSMETADATA.fields_by_name['commands'].message_type = _COMMANDMETADATA
_COMMANDMETADATA_PARAMETERMETAENTRY.containing_type = _COMMANDMETADATA
_COMMANDMETADATA_TAGSENTRY.containing_type = _COMMANDMETADATA
_COMMANDMETADATA.fields_by_name['parameter_meta'].message_type = _COMMANDMETADATA_PARAMETERMETAENTRY
_COMMANDMETADATA.fields_by_name['tags'].message_type = _COMMANDMETADATA_TAGSENTRY
DESCRIPTOR.message_types_by_name['CommandRequest'] = _COMMANDREQUEST
DESCRIPTOR.message_types_by_name['CommandResponse'] = _COMMANDRESPONSE
DESCRIPTOR.message_types_by_name['FileInfo'] = _FILEINFO
DESCRIPTOR.message_types_by_name['CommandsMetadata'] = _COMMANDSMETADATA
DESCRIPTOR.message_types_by_name['CommandMetadata'] = _COMMANDMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CommandRequest = _reflection.GeneratedProtocolMessageType('CommandRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDREQUEST,
  '__module__' : 'protos.model.v1.commands_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.CommandRequest)
  })
_sym_db.RegisterMessage(CommandRequest)

CommandResponse = _reflection.GeneratedProtocolMessageType('CommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDRESPONSE,
  '__module__' : 'protos.model.v1.commands_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.CommandResponse)
  })
_sym_db.RegisterMessage(CommandResponse)

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), {
  'DESCRIPTOR' : _FILEINFO,
  '__module__' : 'protos.model.v1.commands_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.FileInfo)
  })
_sym_db.RegisterMessage(FileInfo)

CommandsMetadata = _reflection.GeneratedProtocolMessageType('CommandsMetadata', (_message.Message,), {
  'DESCRIPTOR' : _COMMANDSMETADATA,
  '__module__' : 'protos.model.v1.commands_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.CommandsMetadata)
  })
_sym_db.RegisterMessage(CommandsMetadata)

CommandMetadata = _reflection.GeneratedProtocolMessageType('CommandMetadata', (_message.Message,), {

  'ParameterMetaEntry' : _reflection.GeneratedProtocolMessageType('ParameterMetaEntry', (_message.Message,), {
    'DESCRIPTOR' : _COMMANDMETADATA_PARAMETERMETAENTRY,
    '__module__' : 'protos.model.v1.commands_pb2'
    # @@protoc_insertion_point(class_scope:v1.model.CommandMetadata.ParameterMetaEntry)
    })
  ,

  'TagsEntry' : _reflection.GeneratedProtocolMessageType('TagsEntry', (_message.Message,), {
    'DESCRIPTOR' : _COMMANDMETADATA_TAGSENTRY,
    '__module__' : 'protos.model.v1.commands_pb2'
    # @@protoc_insertion_point(class_scope:v1.model.CommandMetadata.TagsEntry)
    })
  ,
  'DESCRIPTOR' : _COMMANDMETADATA,
  '__module__' : 'protos.model.v1.commands_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.CommandMetadata)
  })
_sym_db.RegisterMessage(CommandMetadata)
_sym_db.RegisterMessage(CommandMetadata.ParameterMetaEntry)
_sym_db.RegisterMessage(CommandMetadata.TagsEntry)


DESCRIPTOR._options = None
_COMMANDMETADATA_PARAMETERMETAENTRY._options = None
_COMMANDMETADATA_TAGSENTRY._options = None
# @@protoc_insertion_point(module_scope)
