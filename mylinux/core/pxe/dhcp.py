import socket

class DHCP(object):
	def __init__(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind(('0.0.0.0', 67))
		print(self.socket.getsockname())

	def listen(self):
		while True:
			print(self.socket.recv(1))

if __name__ == "__main__":
	dhcp = DHCP()
	dhcp.listen()
