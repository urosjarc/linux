import socket
from bitstring import ConstBitStream
from mylinux.core.utils import BinMsg


class DHCP(object):
	BOOTREQUEST = 1
	BOOTREPLY = 2

	class Message(BinMsg):

		max_size = 576

		class Option(object):
			def __init__(self, num, length, data):
				self.num = num
				self.length = length
				self.data = data

		def __init__(self):
			super(DHCP.Message, self).__init__()

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
			self.chaddr = self.Field(13, ', '.join(['hex:8'] * 16))
			self.sname = self.Field(14, 'bytes:64')
			self.file = self.Field(15, 'bytes:128')
			self.magic_cookie = self.Field(16, 'uint:8, uint:8, uint:8, uint:8')

			self.mac = None

			self.options = {}

		def deserialize(self, binMessage):
			bits = super(DHCP.Message, self).deserialize(binMessage)

			self.mac = self.chaddr.value[:self.hlen.value]

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
		self.pxe_client_ip = [192, 168, 1, 101]
		self.tftp_ip = [192, 168, 1, 100]

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		self.socket.bind(('0.0.0.0', 67))

	def OFFER(self, msg):
		'''
			http://www.slideshare.net/PeterREgli/rarp-bootp-dhcp
			DHCPOFFER defined in:
				- DHCP specs, page 27, 37
				- PXE specs, page 27
		'''

		# HEADERS

		msg.op(DHCP.BOOTREPLY)
		# htype = DHCPDISCOVER
		# hlen = DHCPDISCOVER
		msg.hops(0)
		# xid = DHCPDISCOVER
		msg.secs(0)
		msg.ciaddr([0, 0, 0, 0])
		msg.yiaddr(self.pxe_client_ip)
		msg.siaddr(self.tftp_ip)
		# flags = DHCPDISCOVER
		# giaddr = DHCPDISCOVER
		# shaddr = DHCPDISCOVER
		# sname = DHCPDISCOVER = empty
		# file = DHCPDISCOVER = empty

		# OPTIONS

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

				if msg.op.value == DHCP.BOOTREQUEST:
					self.OFFER(msg)


if __name__ == "__main__":
	msg = DHCP()
