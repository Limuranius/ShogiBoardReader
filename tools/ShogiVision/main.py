import os
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtWidgets import QApplication
from GUI.views.ShogiVision import ShogiVision
from GUI.components.error_mesage_box import error_message_box
from config.Paths import MODEL_ONNX_PATH

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = QApplication([])
    if not os.path.exists(MODEL_ONNX_PATH):
        error_message_box(
            "ShogiVision/_internal/model.onnx not found!")
    else:
        sv = ShogiVision()
        sv.show()
        app.exec()
