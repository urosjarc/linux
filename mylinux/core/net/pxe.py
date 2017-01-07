import socket
from bitstring import BitStream
from mylinux.core.utils import Path

class DHCP(object):
	class Message(object):

		class Label(object):
			def __init__(self, place, form):
				self.place = place
				self.format = form
				self.data = None
			def __call__(self, *args, **kwargs):
				return self.data

		op = Label(1, 'uint:8')
		htype = Label(2, 'uint:8')
		hlen = Label(3, 'uint:8')
		hops = Label(4, 'uint:8')
		xid = Label(5, 'bytes:4')
		secs = Label(6, 'uint:16')
		flag_BROADCAST = Label(7, '1')
		flag_NULL = Label(8, '15')
		ciaddr = Label(9, 'uint:8, uint:8, uint:8, uint:8')
		yiaddr = Label(10, 'uint:8, uint:8, uint:8, uint:8')
		siaddr = Label(11, 'uint:8, uint:8, uint:8, uint:8')
		giaddr = Label(12, 'uint:8, uint:8, uint:8, uint:8')
		chaddr = Label(13, ', '.join(['hex:8' for i in range(16)]))
		sname = Label(14, 'bytes:64')
		file = Label(15, 'bytes:128')
		magic_cookie = Label(16, 'uint:8, uint:8, uint:8, uint:8')

		def __init__(self):
			labels = DHCP.Message.__dict__
			for name in labels:
				if isinstance(labels[name], self.Label):
					self.__dict__[name] = labels[name]

		def MAC(self):
			return {
				1: self.chaddr.data[0:6]
			}[self.htype.data]

		def deserialize(self, package):
			bits = BitStream(package)
			labelsSort = {}

			for label in self.__dict__.values():
				if isinstance(label, self.Label):
					labelsSort[label.place] = label

			for label in labelsSort.values():
				if ',' in label.format:
					label.data = bits.readlist(label.format)
				else:
					label.data = bits.read(label.format)


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
