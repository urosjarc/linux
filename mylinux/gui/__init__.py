import sys
from PyQt5.QtWidgets import QApplication
from .main import MainWindow

def start():
	app = QApplication(sys.argv)

	mainWindow = MainWindow()
	mainWindow.show()

	sys.exit(app.exec_())
