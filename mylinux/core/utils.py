import os

class Path(object):
	def join(*paths):
		return os.path.normpath(
			os.path.join(*paths)
		)

