import socket
from bitstring import ConstBitStream
from mylinux.core.utils import Path


class DHCP(object):

	BOOTREQUEST = 1
	BOOTREPLY = 2

	class Message(object):

		max_size = 576

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

		class Option(object):
			def __init__(self, num, length, data):
				self.num = num
				self.length = length
				self.data = data

		def __init__(self):
			self.raw = None

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
			return self.chaddr.data[:self.hlen.data]

		def deserialize(self, package):
			self.raw = package
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
				if optNum == 255:
					break
				optLen = bits.read('uint:8')
				optData = bits.read('bits:{}'.format(optLen * 8))
				self.options[optNum] = self.Option(
					optNum, optLen, optData
				)

	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(('0.0.0.0', 67))

	def OFFER(self, msg):
		'''
			DHCPOFFER defined in:
				- RFC2131, page 27
				- PXE specs, page 27
		'''
		msg.op(DHCP.BOOTREPLY)
		msg.hops(0)
		msg.secs(0)
		msg.ciaddr([0,0,0,0])
		msg.yiaddr(['''client new ip'''])
		msg.yiaddr(['''next bootstrap server ip'''])
		# msg.options['ip address lease time']
		msg.options['DHCP message type']
		msg.options['message']
		msg.options['server identifier']


	def REQUEST(self, msg):
		pass

	def ACK(self, msg):
		pass

	def listen(self):
		while True:
			package = self.socket.recv(
				self.Message.max_size
			)

			if len(package) > 0:
				msg = self.Message()
				msg.deserialize(package)

				if msg.op.data == DHCP.BOOTREQUEST:
					self.OFFER(msg)


if __name__ == "__main__":
	msg = DHCP()
