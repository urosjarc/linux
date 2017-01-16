import os
from bitstring import ConstBitStream, pack, Bits, BitArray


class BinMsg(object):

	class Field(object):
		def __init__(self, place, form, data=None): # If (data==0) => data == None, so kwargs is needed
			self.place = place
			self.format = form
			self.value = None
			self.bits = None

			self.set(data)

		def set(self, data=None):
			if data is not None:
				self.value = data
				if isinstance(data, list):
					packArgs = (tuple([self.format]) + tuple(data))
					self.bits = Bits(pack(*packArgs))
				else:
					self.bits = Bits(pack(self.format, data))
			else:
				return self.value

	def __init__(self):
		self.package = None

	def get_fields(self):
		fields = []

		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				fields.append(label)

		return sorted(fields, key=lambda x: x.place)

	def serialize(self):
		package = BitArray()

		for field in self.get_fields():
			package.append(field.bits)

		self.package = package.bytes


	def deserialize(self, package):
		self.package = package
		bits = ConstBitStream(package)

		for field in self.get_fields():
			if ',' in field.format:
				field.set(data=bits.readlist(field.format))
			else:
				field.set(data=bits.read(field.format))

		return bits

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

