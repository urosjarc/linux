import os
from bitstring import ConstBitStream

class BinMessage(object):

	class Field(object):
		def __init__(self, place, form):
			self.place = place
			self.format = form
			self.data = None

		def __call__(self, data=None):
			if data:
				self.data = data
			else:
				return self.data

	def __init__(self):
		self.data = None

	def deserialize(self, binMessage):
		self.data = binMessage
		bits = ConstBitStream(binMessage)
		labelsSort = {}

		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				labelsSort[label.place] = label

		for label in labelsSort.values():
			if ',' in label.format:
				label.data = bits.readlist(label.format)
			else:
				label.data = bits.read(label.format)

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

