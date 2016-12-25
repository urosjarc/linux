import sys
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from mylinux.core import exc

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		loadUi(path.join(path.dirname(__file__), 'main.ui'), self)

app = QApplication(sys.argv)

def main():

	try:
		mainWindow = MainWindow()
		mainWindow.show()
		sys.exit(app.exec_())

	except exc.Error as e:
		# Catch our application errors and exit 1 (error)
		print('Error > %s' % e)
		app.exit_code = 1

if __name__ == '__main__':
	main()
