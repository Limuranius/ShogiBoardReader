import os
from PyQt5.QtCore import QLibraryInfo
from GUI.views.CreateDataset import CreateDataset
from PyQt5.QtWidgets import QApplication

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = QApplication([])
    ui = CreateDataset()
    ui.show()
    app.exec()
