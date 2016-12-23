from cement.core.controller import expose
from mylinux.cli.controllers.base import BaseController
from mylinux import server

class ServerController(BaseController):
	"""Server interface which access internals"""

	@expose(help='Start server')
	def start(self):
		server.start()
