import os
from bitstring import ConstBitStream, pack, Bits


class BinMessage(object):

	class Field(object):
		def __init__(self, place, form, data=None): # If (data==0) => data == None, so kwargs is needed
			self.place = place
			self.format = form
			self._data = data
			self.raw = None

			self._set_raw(data)

		def _set_raw(self, data):
			if data is not None:
				if isinstance(data, list):
					packArgs = (tuple([self.format]) + tuple(data))
					self.raw = Bits(pack(*packArgs))
				else:
					self.raw = Bits(pack(self.format, data))

		def __call__(self, **kwargs):
			if 'data' in kwargs:
				self._data = kwargs.get('data')
				self._set_raw(self._data)
			else:
				return self._data

	def __init__(self):
		self.data = None

	def get_fields(self):
		fields = []

		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				fields.append(label)

		return sorted(fields, key=lambda x: x.place)

	def deserialize(self, binMessage):
		self.data = binMessage
		bits = ConstBitStream(binMessage)

		for field in self.get_fields():
			if ',' in field.format:
				field(data=bits.readlist(field.format))
			else:
				field(data=bits.read(field.format))

		return bits

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

