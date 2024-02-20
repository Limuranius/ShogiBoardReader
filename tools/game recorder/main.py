from PyQt5.QtWidgets import QApplication
from view import View
import os

os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")


if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()
