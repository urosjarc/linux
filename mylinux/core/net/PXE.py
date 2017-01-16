import socket
from bitstring import Bits, pack
from mylinux.core.utils import BinMsg


class DHCProxy(object):
	class Msg(BinMsg):
		BOOTREQUEST = 1
		BOOTREPLY = 2

		DHCPDISCOVER = 1
		DHCPOFFER = 2
		DHCPREQUEST = 3
		DHCPDECLINE = 4
		DHCPACK = 5
		DHCPNAK = 6
		DHCPRELEASE = 7
		DHCPINFORM = 8

		PXE_DISCOVERY_CONTROL = 6
		PXE_BOOT_SERVERS = 8
		PXE_BOOT_MENU = 9
		PXE_MENU_PROMPT = 10

		max_size = 576

		class TAG(object):
			message_type = 53

		class Option(object):
			def __init__(self, tag, length, data):
				self.tag = tag
				self.length = length
				self.data = data
				self.bits = Bits(bytes=data)

		def __init__(self):
			super(DHCProxy.Msg, self).__init__()

			self.mac = None

			# Message type (BOOTREQUEST, BOOTREPLY)
			self.op = self.Field(1, 'uint:8')
			# Hardware type
			self.htype = self.Field(2, 'uint:8')
			# Hardware address length
			self.hlen = self.Field(3, 'uint:8')
			# Gateway hops
			self.hops = self.Field(4, 'uint:8')
			# Transaction ID
			self.xid = self.Field(5, 'bytes:4')
			# Seconds elapsed since client started trying to boot, filled by client
			self.secs = self.Field(6, 'uint:16')
			self.flag_BROADCAST = self.Field(7, '1')
			self.flag_NULL = self.Field(8, '15')
			# Clients ip address
			self.ciaddr = self.Field(9, 'uint:8, uint:8, uint:8, uint:8')
			# `Your` clients address
			self.yiaddr = self.Field(10, 'uint:8, uint:8, uint:8, uint:8')
			# Server ip address, returned in bootreply by server
			self.siaddr = self.Field(11, 'uint:8, uint:8, uint:8, uint:8')
			# gateway IP address, used in optional cross-gateway booting
			self.giaddr = self.Field(12, 'uint:8, uint:8, uint:8, uint:8')
			# Clients hardware address, filed in by client
			self.chaddr = self.Field(13, ', '.join(['hex:8'] * 16))
			# Optional server host name
			self.sname = self.Field(14, 'bytes:64')
			# Boot file name
			self.file = self.Field(15, 'bytes:128')

			# Vendor specific area
			self.magic_cookie = self.Field(16, 'uint:8, uint:8, uint:8, uint:8')
			self._options = {}

		def deserialize(self, package):
			bits = super(DHCProxy.Msg, self).deserialize(package)

			self.mac = self.chaddr.value[:self.hlen.value]

			while True:
				optNum = bits.read('uint:8')
				if optNum == 255:
					break
				optLen = bits.read('uint:8')
				optData = bits.read('bytes:{}'.format(optLen))
				self._options[optNum] = self.Option(
					optNum, optLen, optData
				)

		def type(self, type=None):
			if type is None:
				return self._options[self.TAG.message_type].bits.int
			else:
				self._options[self.TAG.message_type] = self.Option(
					self.TAG.message_type, 1, pack('int:8', type)
				)

		def __getitem__(self, item):
			return self._options[item]

		def __setitem__(self, key, value):
			if key == self.TAG.message_type:
				raise Exception('Set message type with Msg.type method')

			if isinstance(value, self.Option):
				self._options[key] = value
			else:
				self._options[key] = self.Option(
					key, len(value) * 8, value
				)

	def __init__(self, ip, tftp_ip):

		self.ip = ip  # Server ip 192.168.1.2
		self.tftp_ip = tftp_ip  # Tfpt ip 192.168.1.9

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
		self.socket.bind((self.ip, 67))

	def send(self, package):
		self.socket.sendto(package, ('<broadcast>', 68))

	def OFFER(self, msg):
		'''
			DHCPOFFER defined in:
				- PXE specs, page 27, 21
		'''

		# HEADERS
		msg.op.set(msg.BOOTREPLY)
		msg.ciaddr.set([0, 0, 0, 0])
		msg.yiaddr.set([0, 0, 0, 0])
		msg.siaddr.set(self.tftp_ip.split('.'))

		# OPTIONS
		oldOpts = msg._options
		msg._options = {}

		msg.type(self.Msg.DHCPOFFER)
		msg[67] = b'PXEClient'
		msg[54] = socket.inet_aton(self.ip)
		msg[97] = oldOpts[97]

		PXE_DISCOVERY_CONTROL = pack(
			'int:8, int:8, bin:8',
			self.Msg.PXE_DISCOVERY_CONTROL,
			1, '0b01000000' # Disable multicast discovery
		)

		PXE_BOOT_SERVERS = pack(
			'int:8, int:16, bytes:2',
			self.Msg.PXE_BOOT_SERVERS,
			2, b'\x00\x00'
		)

		desc = Bits(bytes=b'Linux default installation')
		msg_menu = Bits(bytes=(b'\x00' + Bits(bytes=str(len(desc)).encode()).bytes + desc.bytes))
		PXE_BOOT_MENU = pack(
			'int:8, int:16, bytes:{}'.format(int(len(msg_menu)/8)),
			self.Msg.PXE_BOOT_MENU,
			int(len(msg_menu)/8), msg_menu.bytes
		)

		PXE_MENU_PROMPT = pack(
			'int:8, int:8, bytes:1',
			self.Msg.PXE_MENU_PROMPT,
			1, b'\x00'
		)

		vendorOpt = (
			PXE_DISCOVERY_CONTROL +
			PXE_BOOT_SERVERS +
			PXE_BOOT_MENU +
			PXE_MENU_PROMPT
		)

		msg[43] = vendorOpt.bytes
		self.send(msg.package)

	def listen(self):
		while True:
			package = self.socket.recv(
				self.Msg.max_size
			)

			if len(package) > 0:
				msg = self.Msg()
				msg.deserialize(package)

				if msg.type() == msg.DHCPDISCOVER:
					self.OFFER(msg)

if __name__ == "__main__":
	server = DHCProxy(
		'192.168.1.15', '192.168.1.111'
	)
	server.listen()
