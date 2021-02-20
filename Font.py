from PyQt5 import QtCore, QtGui, QtWidgets


class Font(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Font Options")
        Dialog.resize(353, 89)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(240, 20, 80, 51))
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.setObjectName("buttonBox")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(175, 36, 42, 22))
        self.spinBox.setObjectName("FontSize")
        self.fontComboBox = QtWidgets.QFontComboBox(Dialog)
        self.fontComboBox.setGeometry(QtCore.QRect(35, 36, 131, 22))
        self.fontComboBox.setObjectName("fontComboBox")
        QtCore.QMetaObject.connectSlotsByName(Dialog)
