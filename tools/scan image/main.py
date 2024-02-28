import os
from PyQt5.QtCore import QLibraryInfo

import config.Paths
from config import GLOBAL_CONFIG
from extra.image_modes import ImageMode
from view import View
from PyQt5.QtWidgets import QApplication
import sys
import Elements

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    image_mode = ImageMode(GLOBAL_CONFIG.NeuralNetwork.image_mode)
    reader = Elements.ShogiBoardReader(
        image_mode=image_mode,
        board_splitter=Elements.BoardSplitter(
            image_getter=Elements.ImageGetters.Photo(),
            corner_getter=Elements.CoolCornerDetector()
        ),
        recognizer=Elements.RecognizerONNX(
            model_path=config.Paths.MODEL_ONNX_PATH,
            cell_img_size=GLOBAL_CONFIG.NeuralNetwork.cell_img_size
        )
    )
    ui = View(reader)
    ui.show()
    sys.exit(app.exec_())
