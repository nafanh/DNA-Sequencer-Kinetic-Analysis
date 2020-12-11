# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skip_align.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow6(object):
    def setupUi(self, MainWindow6):
        MainWindow6.setObjectName("MainWindow6")
        MainWindow6.resize(480, 286)
        self.centralwidget = QtWidgets.QWidget(MainWindow6)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 80, 197, 55))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow6.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow6)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 26))
        self.menubar.setObjectName("menubar")
        MainWindow6.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow6)
        self.statusbar.setObjectName("statusbar")
        MainWindow6.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow6)
        self.actionExit.setObjectName("actionExit")

        self.retranslateUi(MainWindow6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow6)

    def retranslateUi(self, MainWindow6):
        _translate = QtCore.QCoreApplication.translate
        MainWindow6.setWindowTitle(_translate("MainWindow6", "Skip Alignment?"))
        self.label.setText(_translate("MainWindow6", "Skip Peak Alignment?"))
        self.pushButton.setText(_translate("MainWindow6", "Yes"))
        self.pushButton_2.setText(_translate("MainWindow6", "No"))
        self.actionExit.setText(_translate("MainWindow6", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow6 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow6()
    ui.setupUi(MainWindow6)
    MainWindow6.show()
    sys.exit(app.exec_())
