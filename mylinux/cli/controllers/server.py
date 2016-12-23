from cement.core.controller import expose
from mylinux.cli.controllers.base import BaseController


class ServerController(BaseController):
	class Meta:
		label = __name__.split('.')[-1]
		description = 'Test packages'

		stacked_on = 'base'
		stacked_type = 'nested'
