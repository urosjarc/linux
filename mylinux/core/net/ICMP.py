from mylinux.core.utils import BinMessage
from bitstring import BitArray


class Echo(BinMessage):
	def __init__(self):
		super(Echo, self).__init__()

		# HEADER
		self.type = self.Field(1, 'uint:8', 8)
		self.code = self.Field(2, 'uint:8', 0)
		self.checksum = self.Field(3, 'uint:16', 0)
		self.identifier = self.Field(4, 'bin:16', b'\x02\x00')
		self.sequence_num = self.Field(5, 'bin:16', b'\x09\x00')

		# DATA
		self.data = self.Field(6, 'bin:16',
		                       b'\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x61\x62\x63\x64\x65\x66\x67\x68\x69'
		                       )

	def get_checksum(self):
		bits = BitArray()
		for label in self.__dict__.values():
			if isinstance(label, self.Field):
				bits.append(label.raw())
		return bits
