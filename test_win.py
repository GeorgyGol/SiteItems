# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_win.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(778, 423)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 771, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xLineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.xLineEdit.setObjectName("xLineEdit")
        self.verticalLayout.addWidget(self.xLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.xTableW = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(13)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xTableW.sizePolicy().hasHeightForWidth())
        self.xTableW.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.xTableW.setFont(font)
        self.xTableW.setTabKeyNavigation(True)
        self.xTableW.setAlternatingRowColors(True)
        self.xTableW.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.xTableW.setObjectName("xTableW")
        self.xTableW.setColumnCount(0)
        self.xTableW.setRowCount(0)
        self.xTableW.horizontalHeader().setVisible(True)
        self.xTableW.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.xTableW)
        spacerItem1 = QtWidgets.QSpacerItem(40, 2, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.btnExit = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btnExit.setObjectName("btnExit")
        self.verticalLayout.addWidget(self.btnExit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.xTableW.setSortingEnabled(True)
        self.btnExit.setText(_translate("Form", "Close"))

