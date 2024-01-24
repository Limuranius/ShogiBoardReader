"""
Читаем снимки
Показываем по одному с выделенными углами
Показываем предсказанные типы клеток, которые можно изменить, если они не правильные
Сохраняем правильную доску в pkl файл в формате (полного изображения? отдельных клеток?)
"""
import os
from PyQt5.QtCore import QLibraryInfo
from view import View
from PyQt5.QtWidgets import QApplication
import sys

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = View()
    ui.show()
    sys.exit(app.exec_())
