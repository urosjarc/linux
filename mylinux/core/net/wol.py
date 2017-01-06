import socket
import binascii


class WOL(object):
	def __init__(self, mac, ip='<broadcast>', password=''):
		self.mac = mac.replace(':', '')
		self.password = password
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.socket.connect((ip, 0))

	def send(self):
		package = binascii.unhexlify(
			('FF' * 6) + (self.mac * 16) + self.password
		)
		self.socket.send(package)


if __name__ == '__main__':
	wol = WOL('00:24:81:C1:4D:4B')
	wol.send()
