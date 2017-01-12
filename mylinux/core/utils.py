import os
from bitstring import ConstBitStream, pack, Bits, BitArray


class BinMsg(object):

	class Field(object):
		def __init__(self, place, form, data=None): # If (data==0) => data == None, so kwargs is needed
			self.place = place
			self.format = form
			self.value = None
			self.raw = None

			self.set(data)

		def set(self, value=None):
			if value is not None:
				self.value = value
				if isinstance(value, list):
					packArgs = (tuple([self.format]) + tuple(value))
					self.raw = Bits(pack(*packArgs))
				else:
					self.raw = Bits(pack(self.format, value))
			else:
				return self.value

	@staticmethod
	def ones_comp_add(num1, num2, length=16):
		MOD = 1 << length
		result = num1 + num2
		return result if result < MOD else (result + 1) % MOD

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
			package.append(field.raw)

		self.package = package.bytes


	def deserialize(self, binMessage):
		self.package = binMessage
		bits = ConstBitStream(binMessage)

		for field in self.get_fields():
			if ',' in field.format:
				field.set(value=bits.readlist(field.format))
			else:
				field.set(value=bits.read(field.format))

		return bits

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

