# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProgressWorker.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_progressWorker(object):
    def setupUi(self, progressWorker):
        progressWorker.setObjectName("progressWorker")
        progressWorker.resize(369, 88)
        self.gridLayout = QtWidgets.QGridLayout(progressWorker)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_cancel = QtWidgets.QPushButton(progressWorker)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 1, 1, 1, 1)
        self.label_progress = QtWidgets.QLabel(progressWorker)
        self.label_progress.setText("")
        self.label_progress.setObjectName("label_progress")
        self.gridLayout.addWidget(self.label_progress, 1, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(progressWorker)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 2)

        self.retranslateUi(progressWorker)
        self.pushButton_cancel.clicked.connect(progressWorker.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(progressWorker)

    def retranslateUi(self, progressWorker):
        _translate = QtCore.QCoreApplication.translate
        progressWorker.setWindowTitle(_translate("progressWorker", "Loading..."))
        self.pushButton_cancel.setText(_translate("progressWorker", "Cancel"))