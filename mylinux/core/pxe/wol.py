import socket
import struct


class WOL(object):
	def __init__(self, mac, ip='255.255.255.255', password=''):
		self.mac = mac.replace(':', '')
		self.password = password
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.connect((ip, 0))

	def send(self):
		msg = ('FF' * 6) + (self.mac * 16) + (self.password)
		package = ''
		for i in range(0, len(msg), 2):
			package += struct.pack(b'B', int(msg[i: i + 2], 16))
		self.socket.send(package)


if __name__ == '__main__':
	wol = WOL('00:24:81:C1:4D:4B')
	wol.send()
