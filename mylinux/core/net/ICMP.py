from mylinux.core.utils import BinMessage
from bitstring import BitArray, Bits


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

	def ones_comp_add16(self, num1, num2):
		MOD = 1 << 16
		result = num1 + num2
		return result if result < MOD else (result + 1) % MOD

	def ones_complement(self, bits):
		return ''.join(['0' if x=='1' else '1' for x in bits])

	def get_checksum(self):
		bits = BitArray()

		# Structure whole message in bits
		for label in self.dict().values():
			print(label.raw())
			bits.append(label.raw())

		# Calculate sum of inverted 16 bits numbers
		sum = 0
		for part in bits.cut(16):
			sum += int(self.ones_complement(part.bin),2)

		# Invert once more
		return self.ones_complement("{0:b}".format(sum)[-15:])

