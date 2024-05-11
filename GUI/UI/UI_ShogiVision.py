# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShogiVision.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(727, 798)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_scan_image = QtWidgets.QWidget()
        self.tab_scan_image.setObjectName("tab_scan_image")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab_scan_image)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scan_image = ScanImage(self.tab_scan_image)
        self.scan_image.setObjectName("scan_image")
        self.horizontalLayout.addWidget(self.scan_image)
        self.tabWidget.addTab(self.tab_scan_image, "")
        self.tab_scan_book = QtWidgets.QWidget()
        self.tab_scan_book.setObjectName("tab_scan_book")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_scan_book)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scan_book = ScanBook(self.tab_scan_book)
        self.scan_book.setObjectName("scan_book")
        self.horizontalLayout_2.addWidget(self.scan_book)
        self.tabWidget.addTab(self.tab_scan_book, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_cat = ImageLabel(self.tab)
        self.label_cat.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cat.setObjectName("label_cat")
        self.verticalLayout_2.addWidget(self.label_cat)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ShogiVision"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_scan_image), _translate("MainWindow", "Scan Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_scan_book), _translate("MainWindow", "Scan Book"))
        self.label_cat.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Cat"))
from GUI.views.ScanBook import ScanBook
from GUI.views.ScanImage import ScanImage
from GUI.widgets.ImageLabel import ImageLabel
