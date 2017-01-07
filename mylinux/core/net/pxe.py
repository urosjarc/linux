import socket
from bitstring import BitStream
from mylinux.core.utils import Path

class DHCP(object):
	class Message(object):

		class Label(object):
			def __init__(self, form):
				self.form = form
				self.data = None

		op = Label('uint:8')
		htype = Label('uint:8')
		hlen = Label('uint:8')
		hops = Label('uint:8')
		xid = Label('bytes:4')
		secs = Label('uint:16')
		flags = Label('bin:16')
		ciaddr = Label('uint:8, uint:8, uint:8, uint:8')
		yiaddr = Label('uint:8, uint:8, uint:8, uint:8')
		siaddr = Label('uint:8, uint:8, uint:8, uint:8')
		giaddr = Label('uint:8, uint:8, uint:8, uint:8')
		chaddr = Label('bytes:16')
		sname = Label('bytes:64')
		file = Label('bytes:128')
		magic_cookie = Label('uint:8, uint:8, uint:8, uint:8')

		def __init__(self):
			labels = DHCP.Message.__dict__
			for name in labels:
				if isinstance(labels[name], self.Label):
					self.__dict__[name] = labels[name]

		def deserialize(self, package):
			bits = BitStream(package)
			labels = self.__dict__
			for name in labels:
				label = labels[name]
				if isinstance(label, self.Label):
					if ',' in label.form:
						label.data = bits.readlist(label.form)
					else:
						label.data = bits.read(label.form)


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
