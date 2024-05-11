# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BoardView.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_boardView(object):
    def setupUi(self, boardView):
        boardView.setObjectName("boardView")
        boardView.resize(416, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(boardView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.board_image_label = ImageLabel(boardView)
        self.board_image_label.setObjectName("board_image_label")
        self.verticalLayout.addWidget(self.board_image_label)
        self.frame = QtWidgets.QFrame(boardView)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_copy_sfen = QtWidgets.QPushButton(self.frame)
        self.pushButton_copy_sfen.setObjectName("pushButton_copy_sfen")
        self.horizontalLayout.addWidget(self.pushButton_copy_sfen)
        self.pushButton_to_lishogi = QtWidgets.QPushButton(self.frame)
        self.pushButton_to_lishogi.setObjectName("pushButton_to_lishogi")
        self.horizontalLayout.addWidget(self.pushButton_to_lishogi)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(boardView)
        self.pushButton_to_lishogi.clicked.connect(boardView.on_to_lishogi_clicked) # type: ignore
        self.pushButton_copy_sfen.clicked.connect(boardView.on_copy_sfen_clicked) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(boardView)

    def retranslateUi(self, boardView):
        _translate = QtCore.QCoreApplication.translate
        boardView.setWindowTitle(_translate("boardView", "BoardView"))
        self.board_image_label.setText(_translate("boardView", "TextLabel"))
        self.pushButton_copy_sfen.setText(_translate("boardView", "Copy SFEN"))
        self.pushButton_to_lishogi.setText(_translate("boardView", "To lishogi"))
from GUI.widgets.ImageLabel import ImageLabel
