from mylinux.core.utils import BinMsg
from bitstring import BitArray, Bits


class Echo(BinMsg):
	def __init__(self):
		super(Echo, self).__init__()

		# HEADER
		self.type = self.Field(1, 'uint:8', 0x08)
		self.code = self.Field(2, 'uint:8', 0x00)
		self.checksum = self.Field(3, 'bytes:2', b'\x00\x00')
		self.identifier = self.Field(4, 'bytes:2', b'\x02\x00')
		self.sequence_num = self.Field(5, 'bytes:2', b'\x09\x00')

		# DATA
		self.data = self.Field(6, 'bytes:32', b'abcdefghijklmnopqrstuvwabcdefghi')

		self._init_checksum()

	def _init_checksum(self):
		bits = BitArray()

		# Throw error if data length is not divided by 16
		dataLen = len(self.data.raw)
		if dataLen % 16 != 0:
			raise Exception('Echo "data" field length({}) is not divided by 16'.format(dataLen))

		# Structure whole message in bits
		for field in self.get_fields():
			bits.append(field.raw)

		# Calculate sum of inverted 16 bits numbers
		compSum = 0
		for part in bits.cut(16):
			compSum = self.ones_comp_add(compSum, part.int)

		# Invert once more
		compSumBits = BitArray(bin=format(compSum, '016b'))
		for i in range(len(compSumBits)):
			compSumBits[i] = True if compSumBits[i] == False else False

		# Set cheksum data
		self.checksum.set(compSumBits.bytes)
