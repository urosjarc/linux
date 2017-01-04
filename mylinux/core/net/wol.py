import socket


class WOL(object):
	def __init__(self, mac, ip='0.0.0.0', password=''):
		self.mac = mac.replace(':', '')
		self.password = password
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.connect((ip, 0))

	def send(self):
		print((b'FF' * 6) + (self.mac * 16) + self.password)
		self.socket.send(
			(b'FF' * 6) + (self.mac * 16) + self.password
		)


if __name__ == '__main__':
	wol = WOL(
		'00:00:00'
	)
	wol.send()
