# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan_image.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_scan_image(object):
    def setupUi(self, scan_image):
        scan_image.setObjectName("scan_image")
        scan_image.resize(1281, 583)
        self.horizontalLayout = QtWidgets.QHBoxLayout(scan_image)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(scan_image)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_images_select = QtWidgets.QFrame(self.frame)
        self.frame_images_select.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_images_select.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_images_select.setObjectName("frame_images_select")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_images_select)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.image_getter_select = DescriptiveComboBox(self.frame_images_select)
        self.image_getter_select.setObjectName("image_getter_select")
        self.verticalLayout_3.addWidget(self.image_getter_select)
        self.photo_drop = FileDragDrop(self.frame_images_select)
        self.photo_drop.setObjectName("photo_drop")
        self.verticalLayout_3.addWidget(self.photo_drop)
        self.video_drop = FileDragDrop(self.frame_images_select)
        self.video_drop.setObjectName("video_drop")
        self.verticalLayout_3.addWidget(self.video_drop)
        self.cam_id_select = DescriptiveComboBox(self.frame_images_select)
        self.cam_id_select.setObjectName("cam_id_select")
        self.verticalLayout_3.addWidget(self.cam_id_select)
        self.verticalLayout_6.addWidget(self.frame_images_select)
        self.corner_and_inventory_select = VisualCornerSelect(self.frame)
        self.corner_and_inventory_select.setObjectName("corner_and_inventory_select")
        self.verticalLayout_6.addWidget(self.corner_and_inventory_select)
        self.frame_config = QtWidgets.QFrame(self.frame)
        self.frame_config.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_config.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_config.setObjectName("frame_config")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_config)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.frame_config)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.checkBox_recognize = QtWidgets.QCheckBox(self.frame_config)
        self.checkBox_recognize.setChecked(True)
        self.checkBox_recognize.setObjectName("checkBox_recognize")
        self.verticalLayout_5.addWidget(self.checkBox_recognize)
        self.checkBox_view_mode = QtWidgets.QCheckBox(self.frame_config)
        self.checkBox_view_mode.setObjectName("checkBox_view_mode")
        self.verticalLayout_5.addWidget(self.checkBox_view_mode)
        self.verticalLayout_6.addWidget(self.frame_config)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_4 = QtWidgets.QFrame(scan_image)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.board_view = BoardView(self.frame_4)
        self.board_view.setObjectName("board_view")
        self.verticalLayout.addWidget(self.board_view)
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_mem_kif = QtWidgets.QFrame(scan_image)
        self.frame_mem_kif.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_mem_kif.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_mem_kif.setObjectName("frame_mem_kif")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_mem_kif)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_memorizer = QtWidgets.QFrame(self.frame_mem_kif)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_memorizer.sizePolicy().hasHeightForWidth())
        self.frame_memorizer.setSizePolicy(sizePolicy)
        self.frame_memorizer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_memorizer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_memorizer.setObjectName("frame_memorizer")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_memorizer)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame_memorizer)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.memorizer_select = DescriptiveComboBox(self.frame_memorizer)
        self.memorizer_select.setObjectName("memorizer_select")
        self.verticalLayout_4.addWidget(self.memorizer_select)
        self.checkBox_lower_moves_first = QtWidgets.QCheckBox(self.frame_memorizer)
        self.checkBox_lower_moves_first.setChecked(True)
        self.checkBox_lower_moves_first.setObjectName("checkBox_lower_moves_first")
        self.verticalLayout_4.addWidget(self.checkBox_lower_moves_first)
        self.checkBox_siren = QtWidgets.QCheckBox(self.frame_memorizer)
        self.checkBox_siren.setStyleSheet("color: rgb(224, 27, 36);")
        self.checkBox_siren.setObjectName("checkBox_siren")
        self.verticalLayout_4.addWidget(self.checkBox_siren)
        self.label_turn_status = QtWidgets.QLabel(self.frame_memorizer)
        self.label_turn_status.setObjectName("label_turn_status")
        self.verticalLayout_4.addWidget(self.label_turn_status)
        self.verticalLayout_2.addWidget(self.frame_memorizer)
        self.kif_recorder = KifRecorder(self.frame_mem_kif)
        self.kif_recorder.setObjectName("kif_recorder")
        self.verticalLayout_2.addWidget(self.kif_recorder)
        self.horizontalLayout.addWidget(self.frame_mem_kif)

        self.retranslateUi(scan_image)
        self.image_getter_select.element_changed['QVariant'].connect(scan_image.on_image_getter_changed) # type: ignore
        self.photo_drop.received_content['QVariant'].connect(scan_image.on_photo_input) # type: ignore
        self.video_drop.received_content['QVariant'].connect(scan_image.on_video_input) # type: ignore
        self.memorizer_select.element_changed['QVariant'].connect(scan_image.on_memorizer_changed) # type: ignore
        self.checkBox_siren.clicked['bool'].connect(scan_image.on_alarm_switched) # type: ignore
        self.checkBox_recognize.clicked['bool'].connect(scan_image.on_recognize_board_switched) # type: ignore
        self.corner_and_inventory_select.corner_detector_changed['QVariant'].connect(scan_image.on_corner_detector_changed) # type: ignore
        self.corner_and_inventory_select.inventory_detector_changed['QVariant'].connect(scan_image.on_inventory_detector_changed) # type: ignore
        self.checkBox_lower_moves_first.clicked['bool'].connect(scan_image.on_lower_moves_first_switched) # type: ignore
        self.cam_id_select.element_changed['QVariant'].connect(scan_image.on_cam_id_changed) # type: ignore
        self.checkBox_view_mode.clicked['bool'].connect(scan_image.on_view_mode_changed) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(scan_image)

    def retranslateUi(self, scan_image):
        _translate = QtCore.QCoreApplication.translate
        scan_image.setWindowTitle(_translate("scan_image", "scan_image"))
        self.label_3.setText(_translate("scan_image", "Config"))
        self.checkBox_recognize.setText(_translate("scan_image", "Recognize board"))
        self.checkBox_view_mode.setText(_translate("scan_image", "View mode"))
        self.label_4.setText(_translate("scan_image", "Memorizer"))
        self.checkBox_lower_moves_first.setText(_translate("scan_image", "Lower moves  first"))
        self.checkBox_siren.setText(_translate("scan_image", "Use siren (LOUD)"))
        self.label_turn_status.setText(_translate("scan_image", "Turn status"))
from GUI.widgets.BoardView import BoardView
from GUI.widgets.DescriptiveComboBox import DescriptiveComboBox
from GUI.widgets.FileDragDrop import FileDragDrop
from GUI.widgets.KifRecorder import KifRecorder
from GUI.widgets.VisualCornerSelect import VisualCornerSelect
