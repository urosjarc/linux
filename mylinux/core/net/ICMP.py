from mylinux.core.utils import BinMessage
from bitstring import BitArray, Bits


class Echo(BinMessage):
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

	def _ones_comp_add16(self, num1, num2):
		MOD = 1 << 16
		result = num1 + num2
		return result if result < MOD else (result + 1) % MOD

	def _ones_comp(self, bits):
		return ''.join(['0' if x == '1' else '1' for x in bits])

	def get_checksum(self):
		bits = BitArray()

		# Throw error if data length is not divided by 16
		dataLen = len(self.data.raw)
		if dataLen % 16 != 0:
			raise Exception('Echo "data" field length({}) is not divided by 16'.format(dataLen))

		# Structure whole message in bits
		for field in self.get_fields():
			print(field.raw.bytes)
			bits.append(field.raw)

		# Calculate sum of inverted 16 bits numbers
		compSum = 0
		for part in bits.cut(16):
			compSum = self._ones_comp_add16(compSum, int(self._ones_comp(part.bin),2))

		# Invert once more
		return Bits(uint=compSum, length=15)
