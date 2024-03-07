from PyQt5.QtCore import pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtWidgets import QWidget
from GUI.UI.UI_DescriptiveComboBox import Ui_descriptiveComboBox


class DescriptiveComboBox(QWidget):
    element_changed = pyqtSignal(QVariant)

    # Text, Description, Value
    __values: list[tuple[str, str, object]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_descriptiveComboBox()
        self.ui.setupUi(self)

    def set_values(self, values: list[tuple[str, str, object]]):
        self.__values = values
        for text, _, _ in values:
            self.ui.comboBox.addItem(text)

    def set_name(self, name: str):
        self.ui.label_name.setText(name + ":")

    @pyqtSlot(int)
    def on_element_changed(self, index: int):
        text, description, value = self.__values[index]
        self.ui.label_description.setText(description)
        self.element_changed.emit(QVariant(value))
