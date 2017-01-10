import os
from bitstring import ConstBitStream, pack, Bits


class BinMessage(object):

	class Field(object):
		def __init__(self, place, form, data=None):
			super(BinMessage.Field, self).__init__()

			self.place = place
			self.format = form
			self.data = data

		def raw(self):
			try:
				return pack(self.format, self.data)
			except TypeError:
				return self.data

		def __call__(self, data=None):
			if data:
				self.data = data
			else:
				return self.data

	def __init__(self):
		self.data = None

	def dict(self):
		labelsSort = {}

		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				labelsSort[label.place] = label

		return labelsSort

	def deserialize(self, binMessage):
		self.data = binMessage
		bits = ConstBitStream(binMessage)
		labelsSort = self.dict()

		for label in labelsSort.values():
			if ',' in label.format:
				label.data = bits.readlist(label.format)
			else:
				label.data = bits.read(label.format)

		return bits

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

