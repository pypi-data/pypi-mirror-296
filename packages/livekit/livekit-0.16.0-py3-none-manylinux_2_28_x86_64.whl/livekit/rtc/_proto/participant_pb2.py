# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: participant.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import handle_pb2 as handle__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11participant.proto\x12\rlivekit.proto\x1a\x0chandle.proto\"\xf5\x01\n\x0fParticipantInfo\x12\x0b\n\x03sid\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08identity\x18\x03 \x01(\t\x12\x10\n\x08metadata\x18\x04 \x01(\t\x12\x42\n\nattributes\x18\x05 \x03(\x0b\x32..livekit.proto.ParticipantInfo.AttributesEntry\x12,\n\x04kind\x18\x06 \x01(\x0e\x32\x1e.livekit.proto.ParticipantKind\x1a\x31\n\x0f\x41ttributesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"o\n\x10OwnedParticipant\x12-\n\x06handle\x18\x01 \x01(\x0b\x32\x1d.livekit.proto.FfiOwnedHandle\x12,\n\x04info\x18\x02 \x01(\x0b\x32\x1e.livekit.proto.ParticipantInfo*\xa1\x01\n\x0fParticipantKind\x12\x1d\n\x19PARTICIPANT_KIND_STANDARD\x10\x00\x12\x1c\n\x18PARTICIPANT_KIND_INGRESS\x10\x01\x12\x1b\n\x17PARTICIPANT_KIND_EGRESS\x10\x02\x12\x18\n\x14PARTICIPANT_KIND_SIP\x10\x03\x12\x1a\n\x16PARTICIPANT_KIND_AGENT\x10\x04\x42\x10\xaa\x02\rLiveKit.Protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'participant_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\rLiveKit.Proto'
  _globals['_PARTICIPANTINFO_ATTRIBUTESENTRY']._options = None
  _globals['_PARTICIPANTINFO_ATTRIBUTESENTRY']._serialized_options = b'8\001'
  _globals['_PARTICIPANTKIND']._serialized_start=412
  _globals['_PARTICIPANTKIND']._serialized_end=573
  _globals['_PARTICIPANTINFO']._serialized_start=51
  _globals['_PARTICIPANTINFO']._serialized_end=296
  _globals['_PARTICIPANTINFO_ATTRIBUTESENTRY']._serialized_start=247
  _globals['_PARTICIPANTINFO_ATTRIBUTESENTRY']._serialized_end=296
  _globals['_OWNEDPARTICIPANT']._serialized_start=298
  _globals['_OWNEDPARTICIPANT']._serialized_end=409
# @@protoc_insertion_point(module_scope)
