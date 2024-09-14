_M='struct_time'
_L='initargs'
_K='builtin_type'
_J='protobuf'
_I='message'
_H='init_kwargs'
_G='init_args'
_F='Column'
_E='iso8601'
_D='utf-8'
_C='utf8'
_B='tuple'
_A=None
import builtins,json,time,typing
from base64 import b64decode,b64encode
from datetime import date,datetime,timedelta,timezone
from io import BytesIO
from typing import Any,Dict,Type
from uuid import UUID
import google.protobuf,google.protobuf.descriptor,google.protobuf.descriptor_pb2,google.protobuf.message,google.protobuf.reflection
from detail.client.logs import get_detail_logger
proto_pool=google.protobuf.descriptor._message.default_pool
psycopg2_types={_F:_A,'AsIs':_A,'QuotedString':_A,'Binary':_A}
try:import psycopg2.extensions
except ImportError:pass
else:
	for name in psycopg2_types:psycopg2_types[name]=getattr(psycopg2.extensions,name,_A)
TYPE_KEY='__detail_json_type__'
known_lossy_type_strs={"<class 'dateutil.tz.tz.tzutc'>","<class 'dateutil.tz.tz.tzlocal'>","<class 'dateutil.tz.tz.tzwinlocal'>"}
LOSSY_REPR='lossy-repr'
builtin_types={A for A in builtins.__dict__.values()if isinstance(A,type)}
logger=get_detail_logger(__name__)
def decode_bytes(obj):
	A=obj
	if _C in A:return A[_C].encode(_D)
	else:return b64decode(A['b64'])
def encode_bytes(obj):
	B=obj;A={}
	try:A[_C]=B.decode(_D)
	except UnicodeDecodeError:A['b64']=b64encode(B).decode(_D)
	A[TYPE_KEY]=str(B.__class__.__name__);return A
def encode_psycopg2_type(type,obj):
	A=obj;B=[];C={}
	if type==psycopg2_types[_F]:E=[A for A in dir(A)if not A.startswith('_')];C={B:getattr(A,B)for B in E}
	else:B=[A.adapted]
	D={_G:B,_H:C};D[TYPE_KEY]=f"psycopg2.extensions.{type.__name__}";return D
def encode_proto(message):A=message;B=google.protobuf.descriptor_pb2.DescriptorProto();A.DESCRIPTOR.CopyToProto(B);return{TYPE_KEY:_J,'proto':B.SerializeToString(),_I:A.SerializeToString()}
def decode_proto(obj):
	A=google.protobuf.descriptor_pb2.DescriptorProto();A.ParseFromString(obj['proto'])
	try:B=proto_pool.FindMessageTypeByName(A.name)
	except KeyError:B=google.protobuf.descriptor.MakeDescriptor(A)
	return google.protobuf.reflection.ParseMessage(B,obj[_I])
class DetailEncoder(json.JSONEncoder):
	def default(G,obj):
		F='repr';D='type';A=obj
		try:hash(A)
		except TypeError:pass
		else:
			if A in builtin_types:B={'name':A.__name__};B[TYPE_KEY]=_K;return B
		if isinstance(A,(datetime,date)):B={_E:A.isoformat()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timezone):assert hasattr(A,'__getinitargs__');B={_L:A.__getinitargs__()};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,timedelta):B={'days':A.days,'seconds':A.seconds,'microseconds':A.microseconds};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,bytes):return encode_bytes(A)
		if isinstance(A,UUID):B={'str':str(A)};B[TYPE_KEY]=str(A.__class__.__name__);return B
		if isinstance(A,google.protobuf.message.Message):return encode_proto(A)
		if isinstance(A,memoryview):return encode_bytes(A.tobytes())
		if isinstance(A,BytesIO):return encode_bytes(A.read())
		for C in psycopg2_types.values():
			if C is not _A and isinstance(A,C):return encode_psycopg2_type(C,A)
		try:E=super().default(A)
		except TypeError:
			B={D:str(type(A)),F:repr(A)};B[TYPE_KEY]=LOSSY_REPR
			if B[D]not in known_lossy_type_strs:logger.warning("encoding %s with lossy repr '%s'; add serilization support or add to known_lossy_type_strs",B[D],B[F],stack_info=True)
			return B
		assert isinstance(E,dict);return E
	def encode(A,obj):
		def B(item):
			A=item
			if isinstance(A,time.struct_time):C={_B:B(tuple(A))};C[TYPE_KEY]=_M;return C
			elif isinstance(A,tuple):return{TYPE_KEY:_B,'items':[B(A)for A in A]}
			elif isinstance(A,list):return[B(A)for A in A]
			elif isinstance(A,dict):return{A:B(C)for(A,C)in A.items()}
			else:return A
		return super().encode(B(obj))
class DetailDecoder(json.JSONDecoder):
	def __init__(A,*B,**C):json.JSONDecoder.__init__(A,*B,object_hook=A.object_hook,**C)
	def object_hook(E,obj):
		A=obj;B=A.pop(TYPE_KEY,_A)
		if B==_K:return builtins.__dict__[A['name']]
		if isinstance(B,str)and B.startswith('psycopg2.extensions'):D=B.rsplit('.')[-1];C=psycopg2_types[D];assert C is not _A,f"psycopg2 is required to deserialize {B}; was detail installed with the replay extras?";return C(*A[_G],**A[_H])
		if B==_B:return tuple(A['items'])
		if B=='datetime':return datetime.fromisoformat(A[_E])
		if B=='date':return date.fromisoformat(A[_E])
		if B=='timezone':return timezone(*A[_L])
		if B=='timedelta':return timedelta(**A)
		if B==_M:return time.struct_time(A[_B])
		if B=='bytes':return decode_bytes(A)
		if B=='UUID':return UUID(A['str'])
		if B==_J:return decode_proto(A)
		if B=='memoryview':return memoryview(decode_bytes(A))
		if B=='BytesIO':return BytesIO(decode_bytes(A))
		if B==LOSSY_REPR:A[TYPE_KEY]=B;return A
		return A