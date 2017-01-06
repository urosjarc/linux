import socket
import struct
from collections import namedtuple
from bitstring import BitArray, BitStream
import binascii


class DHCP_msg(object):

	class Label(object):
		def __init__(self, *form):
			self.data = None
			self.format = form

	def __init__(self):
		self.op = self.Label('uint:8')  # (1 ocet)   Message type. 1=BOOTREQUEST, 2=BOOTREPLY
		self.htype = self.Label('uint:8')# (1 ocet)   Hardware address type.
		self.hlen = self.Label('uint:8')  # (1 ocet)   Hardware address length.
		self.hops = self.Label('uint:8')  # (1 ocet)   How many times was message relayed by relay agent. MAX=16
		self.xid = self.Label('bin:32')  # (4 ocet)   Transaction id to associate messages and responses between a client and server.
		self.secs = None  # (2 ocet)   Seconds elapsed since client began address acqusition or renewal process.
		self.flags = None  # (2 ocet)   Flags.
		self.ciaddr = None  # (4 ocet)   Client ip address.
		self.yiaddr = None  # (4 ocet)   Your (clients) ip address from clients aspect.
		self.siaddr = None  # (4 ocet)   Ip address of next server to used in bootstrap: (DHCPOFFER, DHCPACK).
		self.giaddr = None  # (4 ocet)   Relay agent ip address, used in booting via relay agent.
		self.chaddr = None  # (16 ocet)  Client hardware address.
		self.sname = None  # (64 ocet)  Optional server host name.
		self.file = None  # (128 ocet) Boot file name used in DHCPOFFER.
		self.magic_cookie = None  # (4 ocet)
		self.options = None  # (? ocet)   Optional parameters filed.

	def getMAC(self):
		return BitArray(self.chaddr).unpack(
			['hex:8' for i in range(16)]
		)[0:6]

	def deserialize(self, package):
		bits = BitStream(package)
		self.op = bits.read(8).int
		self.htype = bits.read(8).int
		self.hlen = bits.read(8).int
		self.hops = bits.read(8).int
		self.xid = bits.read(32)
		self.secs = bits.read(16).int
		self.flags = self.Flags(BROADCAST=bits.read(1).bool, other=bits.read(15).bin)
		self.ciaddr = bits.readlist(['uint:8' for i in range(4)])
		self.yiaddr = bits.readlist(['uint:8' for i in range(4)])
		self.siaddr = bits.readlist(['uint:8' for i in range(4)])
		self.giaddr = bits.readlist(['uint:8' for i in range(4)])
		self.chaddr = bits.read(128).bytes
		self.sname = binascii.hexlify(bits.read(512).bytes)
		self.file = bits.read(1024).bytes
		self.magic_cookie = bits.readlist(['uint:8' for i in range(4)])


class DHCP(object):
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
				msg = DHCP_msg()
				msg.deserialize(package)


if __name__ == "__main__":
	dhcp = DHCP()
	dhcp.listen()
