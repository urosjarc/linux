import os
from bitstring import ConstBitStream, pack, Bits, ConstBitArray


class BinMessage(object):

	class Field(object):
		def __init__(self, place, form, data=None):
			super(BinMessage.Field, self).__init__()

			self.place = place
			self.format = form
			self.data = None if data==None else ConstBitArray(pack(form, data))

		def __call__(self, data=None):
			if data:
				self.data = ConstBitArray(pack(self.format, data))
			else:
				return self.data

	def __init__(self):
		self.data = None

	def get_fields(self):
		fields = [None] * len(self.__dict__)

		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				fields[label.place - 1] = label

		return fields

	def deserialize(self, binMessage):
		self.data = binMessage
		bits = ConstBitStream(binMessage)
		fields = self.get_fields()

		for field in fields:
			if ',' in field.format:
				field.data = bits.readlist(field.format)
			else:
				field.data = bits.read(field.format)

		return bits

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

