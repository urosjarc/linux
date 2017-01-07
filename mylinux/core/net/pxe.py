import socket
from bitstring import ConstBitStream
from mylinux.core.utils import Path

class DHCP(object):
	class Message(object):

		class Field(object):
			def __init__(self, place, form):
				self.place = place
				self.format = form
				self.data = None
			def __call__(self, *args, **kwargs):
				return self.data

		class Option(object):
			def __init__(self, num, length, data):
				self.num = num
				self.length = length
				self.data = data


		def __init__(self):
			self.op = self.Field(1, 'uint:8')
			self.htype = self.Field(2, 'uint:8')
			self.hlen = self.Field(3, 'uint:8')
			self.hops = self.Field(4, 'uint:8')
			self.xid = self.Field(5, 'bytes:4')
			self.secs = self.Field(6, 'uint:16')
			self.flag_BROADCAST = self.Field(7, '1')
			self.flag_NULL = self.Field(8, '15')
			self.ciaddr = self.Field(9, 'uint:8, uint:8, uint:8, uint:8')
			self.yiaddr = self.Field(10, 'uint:8, uint:8, uint:8, uint:8')
			self.siaddr = self.Field(11, 'uint:8, uint:8, uint:8, uint:8')
			self.giaddr = self.Field(12, 'uint:8, uint:8, uint:8, uint:8')
			self.chaddr = self.Field(13, ', '.join(['hex:8' for i in range(16)]))
			self.sname = self.Field(14, 'bytes:64')
			self.file = self.Field(15, 'bytes:128')
			self.magic_cookie = self.Field(16, 'uint:8, uint:8, uint:8, uint:8')
			self.options = {}

		def MAC(self):
			return {
				1: self.chaddr.data[0:6]
			}[self.htype.data]

		def deserialize(self, package):
			bits = ConstBitStream(package)
			labelsSort = {}

			for label in self.__dict__.values():
				if isinstance(label, self.Field):
					labelsSort[label.place] = label

			for label in labelsSort.values():
				if ',' in label.format:
					label.data = bits.readlist(label.format)
				else:
					label.data = bits.read(label.format)

			while True:
				optNum = bits.read('uint:8')
				optLen = bits.read('uint:8')
				optData = bits.read('bits:{}'.format(optLen*8))
				self.options[optNum] = self.Option(
					optNum, optLen, optData
				)

				if optNum == 255:
					break


	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(('0.0.0.0', 67))

	def DISCOVER(self):
		pass

	def OFFER(self):
		pass

	def REQUEST(self):
		pass

	def ACK(self):
		pass

	def listen(self):
		while True:
			package = self.socket.recv(590)
			if len(package) > 1:
				print('-------------------------')
				msg = self.Message()
				msg.deserialize(package)


if __name__ == "__main__":
	msg = DHCP.Message()
	with open(Path.join(__file__, '../../resources/DHCDISCOVER.bin'), 'rb') as file:
		msg.deserialize(file)
