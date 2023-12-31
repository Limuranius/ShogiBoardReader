# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1448, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.checkBox_img_original = QtWidgets.QCheckBox(self.frame)
        self.checkBox_img_original.setObjectName("checkBox_img_original")
        self.verticalLayout_6.addWidget(self.checkBox_img_original)
        self.checkBox_img_no_perspective = QtWidgets.QCheckBox(self.frame)
        self.checkBox_img_no_perspective.setObjectName("checkBox_img_no_perspective")
        self.verticalLayout_6.addWidget(self.checkBox_img_no_perspective)
        self.checkBox_img_predicted_board = QtWidgets.QCheckBox(self.frame)
        self.checkBox_img_predicted_board.setObjectName("checkBox_img_predicted_board")
        self.verticalLayout_6.addWidget(self.checkBox_img_predicted_board)
        self.horizontalLayout_2.addWidget(self.frame)
        self.groupBox_corner_detector = QtWidgets.QGroupBox(self.frame_2)
        self.groupBox_corner_detector.setObjectName("groupBox_corner_detector")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_corner_detector)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.radioButton_cd_hsv = QtWidgets.QRadioButton(self.groupBox_corner_detector)
        self.radioButton_cd_hsv.setChecked(False)
        self.radioButton_cd_hsv.setObjectName("radioButton_cd_hsv")
        self.verticalLayout_5.addWidget(self.radioButton_cd_hsv)
        self.radioButton_cd_cool = QtWidgets.QRadioButton(self.groupBox_corner_detector)
        self.radioButton_cd_cool.setChecked(True)
        self.radioButton_cd_cool.setObjectName("radioButton_cd_cool")
        self.verticalLayout_5.addWidget(self.radioButton_cd_cool)
        self.horizontalLayout_2.addWidget(self.groupBox_corner_detector)
        self.groupBox_image_getter = QtWidgets.QGroupBox(self.frame_2)
        self.groupBox_image_getter.setObjectName("groupBox_image_getter")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_image_getter)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.radioButton_ig_photo = QtWidgets.QRadioButton(self.groupBox_image_getter)
        self.radioButton_ig_photo.setObjectName("radioButton_ig_photo")
        self.verticalLayout_4.addWidget(self.radioButton_ig_photo)
        self.radioButton_ig_video = QtWidgets.QRadioButton(self.groupBox_image_getter)
        self.radioButton_ig_video.setObjectName("radioButton_ig_video")
        self.verticalLayout_4.addWidget(self.radioButton_ig_video)
        self.radioButton_ig_photo_2 = QtWidgets.QRadioButton(self.groupBox_image_getter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_ig_photo_2.sizePolicy().hasHeightForWidth())
        self.radioButton_ig_photo_2.setSizePolicy(sizePolicy)
        self.radioButton_ig_photo_2.setChecked(True)
        self.radioButton_ig_photo_2.setObjectName("radioButton_ig_photo_2")
        self.verticalLayout_4.addWidget(self.radioButton_ig_photo_2)
        self.horizontalLayout_2.addWidget(self.groupBox_image_getter)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_ig_photo = QtWidgets.QFrame(self.frame_4)
        self.frame_ig_photo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ig_photo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ig_photo.setObjectName("frame_ig_photo")
        self.formLayout_3 = QtWidgets.QFormLayout(self.frame_ig_photo)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_ig_photo)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_photo_path = QtWidgets.QLineEdit(self.frame_ig_photo)
        self.lineEdit_photo_path.setObjectName("lineEdit_photo_path")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_photo_path)
        self.verticalLayout.addWidget(self.frame_ig_photo)
        self.frame_ig_video = QtWidgets.QFrame(self.frame_4)
        self.frame_ig_video.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ig_video.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ig_video.setObjectName("frame_ig_video")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_ig_video)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.frame_ig_video)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit_video_path = QtWidgets.QLineEdit(self.frame_ig_video)
        self.lineEdit_video_path.setObjectName("lineEdit_video_path")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_video_path)
        self.verticalLayout.addWidget(self.frame_ig_video)
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBox_use_memorizer = QtWidgets.QCheckBox(self.frame_5)
        self.checkBox_use_memorizer.setObjectName("checkBox_use_memorizer")
        self.verticalLayout_7.addWidget(self.checkBox_use_memorizer)
        self.checkBox_alarm = QtWidgets.QCheckBox(self.frame_5)
        self.checkBox_alarm.setObjectName("checkBox_alarm")
        self.verticalLayout_7.addWidget(self.checkBox_alarm)
        self.comboBox_first_side = QtWidgets.QComboBox(self.frame_5)
        self.comboBox_first_side.setObjectName("comboBox_first_side")
        self.comboBox_first_side.addItem("")
        self.comboBox_first_side.addItem("")
        self.verticalLayout_7.addWidget(self.comboBox_first_side)
        self.label_memorizer_status = QtWidgets.QLabel(self.frame_5)
        self.label_memorizer_status.setObjectName("label_memorizer_status")
        self.verticalLayout_7.addWidget(self.label_memorizer_status)
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_start = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout_3.addWidget(self.pushButton_start)
        self.pushButton_save_kifu = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_save_kifu.setObjectName("pushButton_save_kifu")
        self.verticalLayout_3.addWidget(self.pushButton_save_kifu)
        self.horizontalLayout_2.addWidget(self.frame_7)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_img_original = QtWidgets.QLabel(self.frame_3)
        self.label_img_original.setText("")
        self.label_img_original.setObjectName("label_img_original")
        self.horizontalLayout.addWidget(self.label_img_original)
        self.label_img_no_perspective = QtWidgets.QLabel(self.frame_3)
        self.label_img_no_perspective.setText("")
        self.label_img_no_perspective.setObjectName("label_img_no_perspective")
        self.horizontalLayout.addWidget(self.label_img_no_perspective)
        self.label_img_predicted = QtWidgets.QLabel(self.frame_3)
        self.label_img_predicted.setText("")
        self.label_img_predicted.setObjectName("label_img_predicted")
        self.horizontalLayout.addWidget(self.label_img_predicted)
        self.verticalLayout_2.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox_img_original.setText(_translate("MainWindow", "Original image"))
        self.checkBox_img_no_perspective.setText(_translate("MainWindow", "No perspective"))
        self.checkBox_img_predicted_board.setText(_translate("MainWindow", "Predicted board"))
        self.groupBox_corner_detector.setTitle(_translate("MainWindow", "Corner Detector"))
        self.radioButton_cd_hsv.setText(_translate("MainWindow", "HSV"))
        self.radioButton_cd_cool.setText(_translate("MainWindow", "Cool"))
        self.groupBox_image_getter.setTitle(_translate("MainWindow", "Image Getter"))
        self.radioButton_ig_photo.setText(_translate("MainWindow", "Photo"))
        self.radioButton_ig_video.setText(_translate("MainWindow", "Video"))
        self.radioButton_ig_photo_2.setText(_translate("MainWindow", "Camera"))
        self.label_2.setText(_translate("MainWindow", "Photo Path"))
        self.label.setText(_translate("MainWindow", "Video Path"))
        self.checkBox_use_memorizer.setText(_translate("MainWindow", "Use Memorizer"))
        self.checkBox_alarm.setText(_translate("MainWindow", "Alarm"))
        self.comboBox_first_side.setItemText(0, _translate("MainWindow", "Moves first: Lower"))
        self.comboBox_first_side.setItemText(1, _translate("MainWindow", "Moves first: Upper"))
        self.label_memorizer_status.setText(_translate("MainWindow", "Status: "))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.pushButton_save_kifu.setText(_translate("MainWindow", "Save kifu"))
