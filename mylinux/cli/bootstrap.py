"""mylinux bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as BaseController.

import inspect
import re

from mylinux.cli import controllers

def load(app):
	for name, obj in inspect.getmembers(controllers):
		if inspect.isclass(obj) and re.match('mylinux\.cli\.controllers\.[a-z]+', obj.__module__):
			module = obj.__module__.split('.')[-1]

			if re.match('(?!base)', module):
				obj.Meta = controllers.BaseController.Meta()
				obj.Meta.description = obj.__doc__
				obj.Meta.stacked_on = 'base'
				obj.Meta.stacked_type = 'nested'

			obj.Meta.label = module

			app.handler.register(obj)
