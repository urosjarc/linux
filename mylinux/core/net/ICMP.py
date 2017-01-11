from mylinux.core.utils import BinMessage
from bitstring import BitArray, Bits


class Echo(BinMessage):
	def __init__(self):
		super(Echo, self).__init__()

		# HEADER
		self.type = self.Field(1, 'uint:8', 8)
		self.code = self.Field(2, 'uint:8', 0)
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
		'''
			bits.cut(16) naredi zadnji element 1 stopnjo manjsega zato ni pravi rezultat.
		'''
		bits = BitArray()

		# Structure whole message in bits
		for field in self.get_fields():
			bits.append(field.data)

		# Calculate sum of inverted 16 bits numbers
		sum = 0
		for part in bits.cut(16):
			sum = self._ones_comp_add16(sum, part.int)

		# Invert once more
		return self._ones_comp("{0:b}".format(sum)[-15:])
