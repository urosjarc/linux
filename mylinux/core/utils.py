import os
def pathJoin(*paths):
	return os.path.normpath(
		os.path.join(*paths)
	)

