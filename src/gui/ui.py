# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Sat Oct 24 11:26:09 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_dialgEasySub(object):
    def setupUi(self, dialgEasySub):
        dialgEasySub.setObjectName(_fromUtf8("dialgEasySub"))
        dialgEasySub.resize(522, 332)
        dialgEasySub.setMinimumSize(QtCore.QSize(522, 332))
        self.verticalLayoutWidget = QtGui.QWidget(dialgEasySub)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 311))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblFiles = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblFiles.setFont(font)
        self.lblFiles.setObjectName(_fromUtf8("lblFiles"))
        self.verticalLayout.addWidget(self.lblFiles)
        self.lstwFiles = QtGui.QListWidget(self.verticalLayoutWidget)
        self.lstwFiles.setObjectName(_fromUtf8("lstwFiles"))
        self.verticalLayout.addWidget(self.lstwFiles)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnBrowse = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.horizontalLayout.addWidget(self.btnBrowse)
        self.btnDirectory = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnDirectory.setObjectName(_fromUtf8("btnDirectory"))
        self.horizontalLayout.addWidget(self.btnDirectory)
        self.btnDownload = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnDownload.setObjectName(_fromUtf8("btnDownload"))
        self.horizontalLayout.addWidget(self.btnDownload)
        self.btnClear = QtGui.QPushButton(self.verticalLayoutWidget)
        self.btnClear.setObjectName(_fromUtf8("btnClear"))
        self.horizontalLayout.addWidget(self.btnClear)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dialgEasySub)
        QtCore.QMetaObject.connectSlotsByName(dialgEasySub)

    def retranslateUi(self, dialgEasySub):
        dialgEasySub.setWindowTitle(_translate("dialgEasySub", "EasySub - Easiet Subtitles Downloader", None))
        self.lblFiles.setText(_translate("dialgEasySub", "Media Files", None))
        self.btnBrowse.setText(_translate("dialgEasySub", "Browse Files", None))
        self.btnDirectory.setText(_translate("dialgEasySub", "Browse Directory", None))
        self.btnDownload.setText(_translate("dialgEasySub", "Download Subtitles", None))
        self.btnClear.setText(_translate("dialgEasySub", "Clear", None))

