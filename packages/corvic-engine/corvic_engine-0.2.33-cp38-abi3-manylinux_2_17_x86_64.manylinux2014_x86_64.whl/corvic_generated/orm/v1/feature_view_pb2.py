# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: corvic/orm/v1/feature_view.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n corvic/orm/v1/feature_view.proto\x12\rcorvic.orm.v1\x1a\x1b\x62uf/validate/validate.proto\"\x93\x01\n\x0cOutputSource\x12}\n\tsource_id\x18\x02 \x01(\tB`\xbaH]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')R\x08sourceIdJ\x04\x08\x01\x10\x02\"]\n\x11\x46\x65\x61tureViewOutput\x12\x42\n\x0eoutput_sources\x18\x02 \x03(\x0b\x32\x1b.corvic.orm.v1.OutputSourceR\routputSourcesJ\x04\x08\x01\x10\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'corvic.orm.v1.feature_view_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_OUTPUTSOURCE'].fields_by_name['source_id']._options = None
  _globals['_OUTPUTSOURCE'].fields_by_name['source_id']._serialized_options = b'\272H]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_OUTPUTSOURCE']._serialized_start=81
  _globals['_OUTPUTSOURCE']._serialized_end=228
  _globals['_FEATUREVIEWOUTPUT']._serialized_start=230
  _globals['_FEATUREVIEWOUTPUT']._serialized_end=323
# @@protoc_insertion_point(module_scope)
