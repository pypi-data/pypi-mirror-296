# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: corvic/ingest/v2/resource.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from buf.validate import validate_pb2 as buf_dot_validate_dot_validate__pb2
from corvic_generated.status.v1 import event_pb2 as corvic_dot_status_dot_v1_dot_event__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x63orvic/ingest/v2/resource.proto\x12\x10\x63orvic.ingest.v2\x1a\x1b\x62uf/validate/validate.proto\x1a\x1c\x63orvic/status/v1/event.proto\"\xe8\x02\n\x10ResourceMetadata\x12\x1b\n\x04name\x18\x01 \x01(\tB\x07\xbaH\x04r\x02\x10\x01R\x04name\x12\x1b\n\tmime_type\x18\x02 \x01(\tR\x08mimeType\x12y\n\x07room_id\x18\x03 \x01(\tB`\xbaH]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')R\x06roomId\x12#\n\roriginal_path\x18\x05 \x01(\tR\x0coriginalPath\x12 \n\x0b\x64\x65scription\x18\x06 \x01(\tR\x0b\x64\x65scription\x12;\n\ttype_hint\x18\x04 \x01(\x0e\x32\x1e.corvic.ingest.v2.ResourceTypeR\x08typeHint\x12\x1b\n\x04size\x18\x07 \x01(\x03\x42\x07\xbaH\x04\"\x02 \x00R\x04size\"\xd6\x02\n\rResourceEntry\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1b\n\x04name\x18\x02 \x01(\tB\x07\xbaH\x04r\x02\x10\x01R\x04name\x12\x1b\n\tmime_type\x18\x03 \x01(\tR\x08mimeType\x12\x10\n\x03md5\x18\x05 \x01(\tR\x03md5\x12\x17\n\x07room_id\x18\x06 \x01(\tR\x06roomId\x12\x12\n\x04size\x18\x07 \x01(\x04R\x04size\x12#\n\roriginal_path\x18\t \x01(\tR\x0coriginalPath\x12 \n\x0b\x64\x65scription\x18\x0b \x01(\tR\x0b\x64\x65scription\x12\x37\n\x18referenced_by_source_ids\x18\n \x03(\tR\x15referencedBySourceIds\x12<\n\rrecent_events\x18\x08 \x03(\x0b\x32\x17.corvic.status.v1.EventR\x0crecentEvents\"p\n\x16\x43reateUploadURLRequest\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".corvic.ingest.v2.ResourceMetadataR\x08metadata\x12\x16\n\x06origin\x18\x02 \x01(\tR\x06origin\"A\n\x17\x43reateUploadURLResponse\x12\x10\n\x03url\x18\x01 \x01(\tR\x03url\x12\x14\n\x05token\x18\x02 \x01(\tR\x05token\"s\n\x15UploadURLTokenPayload\x12>\n\x08metadata\x18\x01 \x01(\x0b\x32\".corvic.ingest.v2.ResourceMetadataR\x08metadata\x12\x1a\n\x08\x66ilename\x18\x02 \x01(\tR\x08\x66ilename\"0\n\x18\x46inalizeUploadURLRequest\x12\x14\n\x05token\x18\x01 \x01(\tR\x05token\"R\n\x19\x46inalizeUploadURLResponse\x12\x35\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x1f.corvic.ingest.v2.ResourceEntryR\x05\x65ntry\"\x89\x01\n\x15\x44\x65leteResourceRequest\x12p\n\x02id\x18\x01 \x01(\tB`\xbaH]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')R\x02id\"\x18\n\x16\x44\x65leteResourceResponse\"\x86\x01\n\x12GetResourceRequest\x12p\n\x02id\x18\x01 \x01(\tB`\xbaH]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')R\x02id\"L\n\x13GetResourceResponse\x12\x35\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x1f.corvic.ingest.v2.ResourceEntryR\x05\x65ntry\"\x94\x01\n\x14ListResourcesRequest\x12|\n\x07room_id\x18\x01 \x01(\tBc\xbaH`\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')\xd0\x01\x01R\x06roomId\"N\n\x15ListResourcesResponse\x12\x35\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x1f.corvic.ingest.v2.ResourceEntryR\x05\x65ntry\"\x85\x01\n\x0cResourceList\x12u\n\x02id\x18\x01 \x03(\tBe\xbaHb\x92\x01_\"]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')R\x02id\"\xd4\x01\n\x15WatchResourcesRequest\x12{\n\x07room_id\x18\x01 \x01(\tB`\xbaH]\xba\x01Z\n\x0estring.pattern\x12\x16value must be a number\x1a\x30this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')H\x00R\x06roomId\x12\x32\n\x03ids\x18\x02 \x01(\x0b\x32\x1e.corvic.ingest.v2.ResourceListH\x00R\x03idsB\n\n\x08selector\"d\n\x16WatchResourcesResponse\x12J\n\x10updated_resource\x18\x01 \x01(\x0b\x32\x1f.corvic.ingest.v2.ResourceEntryR\x0fupdatedResource*\xab\x01\n\x0cResourceType\x12\x1d\n\x19RESOURCE_TYPE_UNSPECIFIED\x10\x00\x12\x1b\n\x13RESOURCE_TYPE_TABLE\x10\x01\x1a\x02\x08\x01\x12!\n\x1dRESOURCE_TYPE_DIMENSION_TABLE\x10\x02\x12\x1c\n\x18RESOURCE_TYPE_FACT_TABLE\x10\x03\x12\x1e\n\x1aRESOURCE_TYPE_PDF_DOCUMENT\x10\x04\x32\xff\x04\n\x0fResourceService\x12h\n\x0f\x43reateUploadURL\x12(.corvic.ingest.v2.CreateUploadURLRequest\x1a).corvic.ingest.v2.CreateUploadURLResponse\"\x00\x12n\n\x11\x46inalizeUploadURL\x12*.corvic.ingest.v2.FinalizeUploadURLRequest\x1a+.corvic.ingest.v2.FinalizeUploadURLResponse\"\x00\x12\x65\n\x0e\x44\x65leteResource\x12\'.corvic.ingest.v2.DeleteResourceRequest\x1a(.corvic.ingest.v2.DeleteResourceResponse\"\x00\x12\\\n\x0bGetResource\x12$.corvic.ingest.v2.GetResourceRequest\x1a%.corvic.ingest.v2.GetResourceResponse\"\x00\x12\x64\n\rListResources\x12&.corvic.ingest.v2.ListResourcesRequest\x1a\'.corvic.ingest.v2.ListResourcesResponse\"\x00\x30\x01\x12g\n\x0eWatchResources\x12\'.corvic.ingest.v2.WatchResourcesRequest\x1a(.corvic.ingest.v2.WatchResourcesResponse\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'corvic.ingest.v2.resource_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RESOURCETYPE'].values_by_name["RESOURCE_TYPE_TABLE"]._options = None
  _globals['_RESOURCETYPE'].values_by_name["RESOURCE_TYPE_TABLE"]._serialized_options = b'\010\001'
  _globals['_RESOURCEMETADATA'].fields_by_name['name']._options = None
  _globals['_RESOURCEMETADATA'].fields_by_name['name']._serialized_options = b'\272H\004r\002\020\001'
  _globals['_RESOURCEMETADATA'].fields_by_name['room_id']._options = None
  _globals['_RESOURCEMETADATA'].fields_by_name['room_id']._serialized_options = b'\272H]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_RESOURCEMETADATA'].fields_by_name['size']._options = None
  _globals['_RESOURCEMETADATA'].fields_by_name['size']._serialized_options = b'\272H\004\"\002 \000'
  _globals['_RESOURCEENTRY'].fields_by_name['name']._options = None
  _globals['_RESOURCEENTRY'].fields_by_name['name']._serialized_options = b'\272H\004r\002\020\001'
  _globals['_DELETERESOURCEREQUEST'].fields_by_name['id']._options = None
  _globals['_DELETERESOURCEREQUEST'].fields_by_name['id']._serialized_options = b'\272H]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_GETRESOURCEREQUEST'].fields_by_name['id']._options = None
  _globals['_GETRESOURCEREQUEST'].fields_by_name['id']._serialized_options = b'\272H]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_LISTRESOURCESREQUEST'].fields_by_name['room_id']._options = None
  _globals['_LISTRESOURCESREQUEST'].fields_by_name['room_id']._serialized_options = b'\272H`\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')\320\001\001'
  _globals['_RESOURCELIST'].fields_by_name['id']._options = None
  _globals['_RESOURCELIST'].fields_by_name['id']._serialized_options = b'\272Hb\222\001_\"]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_WATCHRESOURCESREQUEST'].fields_by_name['room_id']._options = None
  _globals['_WATCHRESOURCESREQUEST'].fields_by_name['room_id']._serialized_options = b'\272H]\272\001Z\n\016string.pattern\022\026value must be a number\0320this.matches(\'^[0-9]+$\') && !this.endsWith(\'\\n\')'
  _globals['_RESOURCETYPE']._serialized_start=2318
  _globals['_RESOURCETYPE']._serialized_end=2489
  _globals['_RESOURCEMETADATA']._serialized_start=113
  _globals['_RESOURCEMETADATA']._serialized_end=473
  _globals['_RESOURCEENTRY']._serialized_start=476
  _globals['_RESOURCEENTRY']._serialized_end=818
  _globals['_CREATEUPLOADURLREQUEST']._serialized_start=820
  _globals['_CREATEUPLOADURLREQUEST']._serialized_end=932
  _globals['_CREATEUPLOADURLRESPONSE']._serialized_start=934
  _globals['_CREATEUPLOADURLRESPONSE']._serialized_end=999
  _globals['_UPLOADURLTOKENPAYLOAD']._serialized_start=1001
  _globals['_UPLOADURLTOKENPAYLOAD']._serialized_end=1116
  _globals['_FINALIZEUPLOADURLREQUEST']._serialized_start=1118
  _globals['_FINALIZEUPLOADURLREQUEST']._serialized_end=1166
  _globals['_FINALIZEUPLOADURLRESPONSE']._serialized_start=1168
  _globals['_FINALIZEUPLOADURLRESPONSE']._serialized_end=1250
  _globals['_DELETERESOURCEREQUEST']._serialized_start=1253
  _globals['_DELETERESOURCEREQUEST']._serialized_end=1390
  _globals['_DELETERESOURCERESPONSE']._serialized_start=1392
  _globals['_DELETERESOURCERESPONSE']._serialized_end=1416
  _globals['_GETRESOURCEREQUEST']._serialized_start=1419
  _globals['_GETRESOURCEREQUEST']._serialized_end=1553
  _globals['_GETRESOURCERESPONSE']._serialized_start=1555
  _globals['_GETRESOURCERESPONSE']._serialized_end=1631
  _globals['_LISTRESOURCESREQUEST']._serialized_start=1634
  _globals['_LISTRESOURCESREQUEST']._serialized_end=1782
  _globals['_LISTRESOURCESRESPONSE']._serialized_start=1784
  _globals['_LISTRESOURCESRESPONSE']._serialized_end=1862
  _globals['_RESOURCELIST']._serialized_start=1865
  _globals['_RESOURCELIST']._serialized_end=1998
  _globals['_WATCHRESOURCESREQUEST']._serialized_start=2001
  _globals['_WATCHRESOURCESREQUEST']._serialized_end=2213
  _globals['_WATCHRESOURCESRESPONSE']._serialized_start=2215
  _globals['_WATCHRESOURCESRESPONSE']._serialized_end=2315
  _globals['_RESOURCESERVICE']._serialized_start=2492
  _globals['_RESOURCESERVICE']._serialized_end=3131
# @@protoc_insertion_point(module_scope)
