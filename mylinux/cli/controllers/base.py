from cement.core.controller import CementBaseController, expose

import mylinux

class BaseController(CementBaseController):
	class Meta:
		label = __name__.split('.')[-1]
		description = "{} - {}".format(
			mylinux.__name__,
			mylinux.__description__
		)

	@expose(hide=True)
	def default(self):
		self.app.args.print_help()
