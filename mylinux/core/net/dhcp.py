import socket
import struct
from collections import namedtuple
from bitstring import BitArray, BitStream
import binascii


class DHCP_msg(object):
	Flags = namedtuple('Flags', ['BROADCAST', 'other'])

	def __init__(self):
		self.op = None  # (1 ocet)   Message type. 1=BOOTREQUEST, 2=BOOTREPLY
		self.htype = None  # (1 ocet)   Hardware address type.
		self.hlen = None  # (1 ocet)   Hardware address length.
		self.hops = None  # (1 ocet)   How many times was message relayed by relay agent. MAX=16
		self.xid = None  # (4 ocet)   Transaction id to associate messages and responses between a client and server.
		self.secs = None  # (2 ocet)   Seconds elapsed since client began address acqusition or renewal process.
		self.flags = None  # (2 ocet)   Flags.
		self.ciaddr = None  # (4 ocet)   Client ip address.
		self.yiaddr = None  # (4 ocet)   Your (clients) ip address from clients aspect.
		self.siaddr = None  # (4 ocet)   Ip address of next server to used in bootstrap: (DHCPOFFER, DHCPACK).
		self.giaddr = None  # (4 ocet)   Relay agent ip address, used in booting via relay agent.
		self.chaddr = None  # (16 ocet)  Client hardware address.
		self.sname = None  # (64 ocet)  Optional server host name.
		self.file = None  # (128 ocet) Boot file name used in DHCPOFFER.
		self.options = None  # (? ocet)   Optional parameters filed.

	def deserialize(self, package):
		pac = BitStream(package)
		self.op = pac.read('int:8')
		self.htype = pac.read('int:8')
		self.hlen = pac.read('int:8')
		self.hops = pac.read('int:8')
		self.xid = pac.read('bytes:4')
		# self.htype, self.hlen, self.hops = struct.unpack('!3B', pac.read(1 + 1 + 1 + 1))
		# self.xid = pac.read(4)
		# self.secs, flags, ciaddr = struct.unpack('!H2s4s', pac.read(2 + 2 + 4))
		# yiaddr, siaddr, giaddr = struct.unpack('!4s4s4s', pac.read(4 + 4 + 4))
		# chaddr = pac.read(16)
		# sname, self.file = struct.unpack('!64s128s', pac.read(64 + 128))
		# self.magic_cookie = struct.unpack('!4s', pac.read(4))
		#
		#
		# flagsBits = BitArray(flags)
		# self.flags = self.Flags(
		# 	BROADCAST=flagsBits[0],
		# 	other=flagsBits[1:].bin
		# )
		# self.ciaddr = struct.unpack('!4B', ciaddr)
		# self.yiaddr = struct.unpack('!4B', yiaddr)
		# self.siaddr = struct.unpack('!4B', siaddr)
		# self.giaddr = struct.unpack('!4B', giaddr)
		#
		# if self.htype == 1: # Ethernet type mac
		# 	chaddr = binascii.hexlify(chaddr[0:6])
		#
		# self.chaddr = tuple(chaddr[i:i+2] for i in range(0, len(chaddr), 2))
		# self.sname = binascii.hexlify(sname)


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
