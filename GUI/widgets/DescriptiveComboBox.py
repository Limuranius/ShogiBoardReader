from PyQt5.QtCore import pyqtSignal, pyqtSlot, QVariant
from PyQt5.QtWidgets import QWidget
from GUI.UI.UI_DescriptiveComboBox import Ui_descriptiveComboBox
import copy


class DescriptiveComboBox(QWidget):
    element_changed = pyqtSignal(QVariant)

    # Text, Description, Value
    __values: list[tuple[str, str, object]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_descriptiveComboBox()
        self.ui.setupUi(self)
        self.__values = []

    def set_values(self, values: list[tuple[str, str, object]]):
        self.__values = values
        for text, _, _ in values:
            self.ui.comboBox.addItem(text)

    def set_name(self, name: str):
        self.ui.label_name.setText(name + ":")

    @pyqtSlot(int)
    def on_element_changed(self, index: int):
        text, description, value = self.__values[index]
        value_copy = copy.copy(value)
        self.ui.label_description.setText(description)
        self.element_changed.emit(QVariant(value_copy))

    def switch_to_same_class(self, obj: object, emit_signal: bool = True):
        for i, (_, _, value) in enumerate(self.__values):
            if type(obj) is type(value):  # Have same class
                if emit_signal:
                    self.ui.comboBox.setCurrentIndex(i)
                else:
                    self.ui.comboBox.blockSignals(True)
                    self.ui.comboBox.setCurrentIndex(i)
                    self.ui.comboBox.blockSignals(False)
