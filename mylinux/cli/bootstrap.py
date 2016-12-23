"""mylinux bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as BaseController.

import inspect
import re

from mylinux.cli import controllers

def load(app):
	for name, obj in inspect.getmembers(controllers):
		if inspect.isclass(obj) and re.match('mylinux\.cli\.controllers\.[a-z]+',obj.__module__):
			app.handler.register(obj)
