class Error(Exception):
	"""Generic errors."""

	def __init__(self, msg):
		Exception.__init__(self)
		self.msg = msg

	def __str__(self):
		return self.msg


class ConfigError(Error):
	"""Config related errors."""
	pass


class RuntimeError(Error):
	"""Generic runtime errors."""
	pass


class ArgumentError(Error):
	"""Argument related errors."""
	pass


class PathTraversalException(Error):
	pass

