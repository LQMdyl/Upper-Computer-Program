# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PLCtestForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PlcTestForm(object):
    def setupUi(self, PlcTestForm):
        PlcTestForm.setObjectName("PlcTestForm")
        PlcTestForm.resize(408, 404)
        self.groupBox_3 = QtWidgets.QGroupBox(PlcTestForm)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 379, 169))
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_3)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 351, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lbPlcAddress = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.lbPlcAddress.setFont(font)
        self.lbPlcAddress.setObjectName("lbPlcAddress")
        self.gridLayout_3.addWidget(self.lbPlcAddress, 0, 0, 1, 1)
        self.lbPlcholdaddress = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.lbPlcholdaddress.setFont(font)
        self.lbPlcholdaddress.setObjectName("lbPlcholdaddress")
        self.gridLayout_3.addWidget(self.lbPlcholdaddress, 1, 0, 1, 1)
        self.lePlcHold = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.lePlcHold.setFont(font)
        self.lePlcHold.setObjectName("lePlcHold")
        self.gridLayout_3.addWidget(self.lePlcHold, 1, 1, 1, 1)
        self.lePlcColi = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.lePlcColi.setObjectName("lePlcColi")
        self.gridLayout_3.addWidget(self.lePlcColi, 0, 1, 1, 1)
        self.lbValue = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.lbValue.setObjectName("lbValue")
        self.gridLayout_3.addWidget(self.lbValue, 2, 0, 1, 1)
        self.leWrite = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.leWrite.setObjectName("leWrite")
        self.gridLayout_3.addWidget(self.leWrite, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pbtCoilRead = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.pbtCoilRead.setFont(font)
        self.pbtCoilRead.setObjectName("pbtCoilRead")
        self.horizontalLayout_2.addWidget(self.pbtCoilRead)
        self.pbtColiWrite = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.pbtColiWrite.setFont(font)
        self.pbtColiWrite.setObjectName("pbtColiWrite")
        self.horizontalLayout_2.addWidget(self.pbtColiWrite)
        self.pbtHoldRead = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.pbtHoldRead.setFont(font)
        self.pbtHoldRead.setObjectName("pbtHoldRead")
        self.horizontalLayout_2.addWidget(self.pbtHoldRead)
        self.pbtHoldWrite = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("华文中宋")
        self.pbtHoldWrite.setFont(font)
        self.pbtHoldWrite.setObjectName("pbtHoldWrite")
        self.horizontalLayout_2.addWidget(self.pbtHoldWrite)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.textBrowser = QtWidgets.QTextBrowser(PlcTestForm)
        self.textBrowser.setGeometry(QtCore.QRect(10, 190, 381, 192))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(PlcTestForm)
        QtCore.QMetaObject.connectSlotsByName(PlcTestForm)

    def retranslateUi(self, PlcTestForm):
        _translate = QtCore.QCoreApplication.translate
        PlcTestForm.setWindowTitle(_translate("PlcTestForm", "plc测试窗口"))
        self.groupBox_3.setTitle(_translate("PlcTestForm", "PLC"))
        self.lbPlcAddress.setText(_translate("PlcTestForm", "线圈地址："))
        self.lbPlcholdaddress.setText(_translate("PlcTestForm", "保持寄存器地址："))
        self.lbValue.setText(_translate("PlcTestForm", "写入值"))
        self.pbtCoilRead.setText(_translate("PlcTestForm", "读取线圈"))
        self.pbtColiWrite.setText(_translate("PlcTestForm", "写入线圈"))
        self.pbtHoldRead.setText(_translate("PlcTestForm", "读取寄存器"))
        self.pbtHoldWrite.setText(_translate("PlcTestForm", "写入寄存器"))
