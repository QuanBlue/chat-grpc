# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import user_pb2 as user__pb2
import share_type_pb2 as share__type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\x1a\nuser.proto\x1a\x10share_type.proto\"?\n\x07Message\x12\x15\n\x06sender\x18\x01 \x01(\x0b\x32\x05.User\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x0c\n\x04time\x18\x03 \x01(\t\"9\n\x0bLikeRequest\x12\x15\n\x06sender\x18\x01 \x01(\x0b\x32\x05.User\x12\x13\n\x0breceiver_id\x18\x02 \x01(\t\" \n\x0cLikeResponse\x12\x10\n\x08response\x18\x01 \x01(\t\"&\n\x13SendMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x96\x01\n\x0b\x43hatService\x12/\n\x0bSendMessage\x12\x08.Message\x1a\x14.SendMessageResponse\"\x00\x12&\n\x0eReceiveMessage\x12\x06.Empty\x1a\x08.Message\"\x00\x30\x01\x12.\n\rHandleLikeMsg\x12\x0c.LikeRequest\x1a\r.LikeResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MESSAGE._serialized_start=44
  _MESSAGE._serialized_end=107
  _LIKEREQUEST._serialized_start=109
  _LIKEREQUEST._serialized_end=166
  _LIKERESPONSE._serialized_start=168
  _LIKERESPONSE._serialized_end=200
  _SENDMESSAGERESPONSE._serialized_start=202
  _SENDMESSAGERESPONSE._serialized_end=240
  _CHATSERVICE._serialized_start=243
  _CHATSERVICE._serialized_end=393
# @@protoc_insertion_point(module_scope)
