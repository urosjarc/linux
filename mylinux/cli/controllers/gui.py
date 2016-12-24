from cement.core.controller import expose
from mylinux.cli.controllers.base import BaseController
from mylinux import gui

class GuiController(BaseController):
	"""Server interface which access internals"""

	@expose(help='Start gui')
	def start(self):
		gui.start()
