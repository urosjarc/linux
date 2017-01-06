import socket
from bitstring import BitArray, BitStream


class DHCP_msg(object):

	class Label(object):
		def __init__(self, *form):
			self.data = None
			self.format = form
		def deserialize(self, bitStream):
			if len(self.format) > 1:
				self.data = bitStream.readlist(*self.format)
			else:
				self.data = bitStream.read(self.format)


	class FlagsLabel(Label):
		def __init__(self, *form):
			super(DHCP_msg.FlagsLabel, self).__init__(*form)
			self.BROADCAST = None

	def __init__(self):
		self.op = self.Label('uint:8')  # (1 ocet)   Message type. 1=BOOTREQUEST, 2=BOOTREPLY
		self.htype = self.Label('uint:8')# (1 ocet)   Hardware address type.
		self.hlen = self.Label('uint:8')  # (1 ocet)   Hardware address length.
		self.hops = self.Label('uint:8')  # (1 ocet)   How many times was message relayed by relay agent. MAX=16
		self.xid = self.Label('bin:32')  # (4 ocet)   Transaction id to associate messages and responses between a client and server.
		self.secs = self.Label('uint:16') # (2 ocet)   Seconds elapsed since client began address acqusition or renewal process.
		self.flags = self.FlagsLabel('bool')# (2 ocet)   Flags.
		self.ciaddr = self.Label('uint:8','uint:8', 'uint:8', 'uint:8')  # (4 ocet)   Client ip address.
		self.yiaddr = self.Label('uint:8','uint:8', 'uint:8', 'uint:8')  # (4 ocet)   Your (clients) ip address from clients aspect.
		self.siaddr = self.Label('uint:8','uint:8', 'uint:8', 'uint:8')  # (4 ocet)   Ip address of next server to used in bootstrap: (DHCPOFFER, DHCPACK).
		self.giaddr = self.Label('uint:8','uint:8', 'uint:8', 'uint:8')  # (4 ocet)   Relay agent ip address, used in booting via relay agent.
		self.chaddr = self.Label('uint:8','uint:8', 'uint:8', 'uint:8','uint:8','uint:8')  # (16 ocet)  Client hardware address.
		self.sname = self. Label('bytes:64') # (64 ocet)  Optional server host name.
		self.file = self.Label('bytes:128')  # (128 ocet) Boot file name used in DHCPOFFER.
		self.magic_cookie = self.Label('uint:8','uint:8','uint:8','uint:8')  # (4 ocet)
		self.options = None  # (? ocet)   Optional parameters filed.

	def getMAC(self):
		return BitArray(self.chaddr).unpack(
			['hex:8' for i in range(16)]
		)[0:6]

	def deserialize(self, package):
		bits = BitStream(package)
		for name, object in self.__dict__.iteritems():
			if isinstance(object, self.Label):
				object.deserialize(bits)

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
