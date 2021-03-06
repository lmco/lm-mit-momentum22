# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: viz.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='viz.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\tviz.proto\"L\n\x08Location\x12\r\n\x05msgId\x18\x01 \x01(\r\x12\x10\n\x08latitude\x18\x02 \x01(\x01\x12\x11\n\tlongitude\x18\x03 \x01(\x01\x12\x0c\n\x04time\x18\x04 \x01(\x04\"D\n\x13LandingNotification\x12\r\n\x05msgId\x18\x01 \x01(\r\x12\x10\n\x08isLanded\x18\x02 \x01(\x08\x12\x0c\n\x04time\x18\x03 \x01(\x04\"F\n\x13TakeoffNotification\x12\r\n\x05msgId\x18\x01 \x01(\r\x12\x12\n\nisTakenOff\x18\x02 \x01(\x08\x12\x0c\n\x04time\x18\x03 \x01(\x04\"\x17\n\x06ReqAck\x12\r\n\x05msgId\x18\x01 \x01(\x04\x32\xa3\x01\n\rMomentum22Viz\x12\x33\n\x10SetLandingStatus\x12\x14.LandingNotification\x1a\x07.ReqAck\"\x00\x12\x33\n\x10SetTakeoffStatus\x12\x14.TakeoffNotification\x1a\x07.ReqAck\"\x00\x12(\n\x10SetDroneLocation\x12\t.Location\x1a\x07.ReqAck\"\x00\x62\x06proto3'
)




_LOCATION = _descriptor.Descriptor(
  name='Location',
  full_name='Location',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgId', full_name='Location.msgId', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='Location.latitude', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='Location.longitude', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='Location.time', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=13,
  serialized_end=89,
)


_LANDINGNOTIFICATION = _descriptor.Descriptor(
  name='LandingNotification',
  full_name='LandingNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgId', full_name='LandingNotification.msgId', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isLanded', full_name='LandingNotification.isLanded', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='LandingNotification.time', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=91,
  serialized_end=159,
)


_TAKEOFFNOTIFICATION = _descriptor.Descriptor(
  name='TakeoffNotification',
  full_name='TakeoffNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgId', full_name='TakeoffNotification.msgId', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='isTakenOff', full_name='TakeoffNotification.isTakenOff', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='time', full_name='TakeoffNotification.time', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=161,
  serialized_end=231,
)


_REQACK = _descriptor.Descriptor(
  name='ReqAck',
  full_name='ReqAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='msgId', full_name='ReqAck.msgId', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=233,
  serialized_end=256,
)

DESCRIPTOR.message_types_by_name['Location'] = _LOCATION
DESCRIPTOR.message_types_by_name['LandingNotification'] = _LANDINGNOTIFICATION
DESCRIPTOR.message_types_by_name['TakeoffNotification'] = _TAKEOFFNOTIFICATION
DESCRIPTOR.message_types_by_name['ReqAck'] = _REQACK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), {
  'DESCRIPTOR' : _LOCATION,
  '__module__' : 'viz_pb2'
  # @@protoc_insertion_point(class_scope:Location)
  })
_sym_db.RegisterMessage(Location)

LandingNotification = _reflection.GeneratedProtocolMessageType('LandingNotification', (_message.Message,), {
  'DESCRIPTOR' : _LANDINGNOTIFICATION,
  '__module__' : 'viz_pb2'
  # @@protoc_insertion_point(class_scope:LandingNotification)
  })
_sym_db.RegisterMessage(LandingNotification)

TakeoffNotification = _reflection.GeneratedProtocolMessageType('TakeoffNotification', (_message.Message,), {
  'DESCRIPTOR' : _TAKEOFFNOTIFICATION,
  '__module__' : 'viz_pb2'
  # @@protoc_insertion_point(class_scope:TakeoffNotification)
  })
_sym_db.RegisterMessage(TakeoffNotification)

ReqAck = _reflection.GeneratedProtocolMessageType('ReqAck', (_message.Message,), {
  'DESCRIPTOR' : _REQACK,
  '__module__' : 'viz_pb2'
  # @@protoc_insertion_point(class_scope:ReqAck)
  })
_sym_db.RegisterMessage(ReqAck)



_MOMENTUM22VIZ = _descriptor.ServiceDescriptor(
  name='Momentum22Viz',
  full_name='Momentum22Viz',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=259,
  serialized_end=422,
  methods=[
  _descriptor.MethodDescriptor(
    name='SetLandingStatus',
    full_name='Momentum22Viz.SetLandingStatus',
    index=0,
    containing_service=None,
    input_type=_LANDINGNOTIFICATION,
    output_type=_REQACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetTakeoffStatus',
    full_name='Momentum22Viz.SetTakeoffStatus',
    index=1,
    containing_service=None,
    input_type=_TAKEOFFNOTIFICATION,
    output_type=_REQACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetDroneLocation',
    full_name='Momentum22Viz.SetDroneLocation',
    index=2,
    containing_service=None,
    input_type=_LOCATION,
    output_type=_REQACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MOMENTUM22VIZ)

DESCRIPTOR.services_by_name['Momentum22Viz'] = _MOMENTUM22VIZ

# @@protoc_insertion_point(module_scope)
