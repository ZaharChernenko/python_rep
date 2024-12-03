from WeatherWindow import WeatherWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/app_icon.ico"))

    screen = QMainWindow()
    ui = WeatherWindow(screen)
    screen.show()

    sys.exit(app.exec())
