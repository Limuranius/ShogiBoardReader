import os
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtWidgets import QApplication
from GUI.views.ShogiVision import ShogiVision

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = QApplication([])
    sv = ShogiVision()
    sv.show()
    app.exec()
