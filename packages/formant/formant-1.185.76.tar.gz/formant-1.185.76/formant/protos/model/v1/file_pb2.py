# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/model/v1/file.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protos/model/v1/file.proto',
  package='v1.model',
  syntax='proto3',
  serialized_options=b'Z)github.com/FormantIO/genproto/go/v1/model',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1aprotos/model/v1/file.proto\x12\x08v1.model\"D\n\x04\x46ile\x12\r\n\x03url\x18\x01 \x01(\tH\x00\x12\r\n\x03raw\x18\x02 \x01(\x0cH\x00\x12\x10\n\x08\x66ilename\x18\x03 \x01(\tB\x06\n\x04\x64\x61taJ\x04\x08\x04\x10\x05\x42+Z)github.com/FormantIO/genproto/go/v1/modelb\x06proto3'
)




_FILE = _descriptor.Descriptor(
  name='File',
  full_name='v1.model.File',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='url', full_name='v1.model.File.url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='raw', full_name='v1.model.File.raw', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filename', full_name='v1.model.File.filename', index=2,
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
    _descriptor.OneofDescriptor(
      name='data', full_name='v1.model.File.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=40,
  serialized_end=108,
)

_FILE.oneofs_by_name['data'].fields.append(
  _FILE.fields_by_name['url'])
_FILE.fields_by_name['url'].containing_oneof = _FILE.oneofs_by_name['data']
_FILE.oneofs_by_name['data'].fields.append(
  _FILE.fields_by_name['raw'])
_FILE.fields_by_name['raw'].containing_oneof = _FILE.oneofs_by_name['data']
DESCRIPTOR.message_types_by_name['File'] = _FILE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'protos.model.v1.file_pb2'
  # @@protoc_insertion_point(class_scope:v1.model.File)
  })
_sym_db.RegisterMessage(File)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
