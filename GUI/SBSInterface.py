# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SBSInterface.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SBSsystem(object):
    def setupUi(self, SBSsystem):
        SBSsystem.setObjectName("SBSsystem")
        SBSsystem.resize(2282, 1496)
        SBSsystem.setAnimated(False)
        self.centralWidget = QtWidgets.QWidget(SBSsystem)
        self.centralWidget.setObjectName("centralWidget")
        self.SBSFiltershape = QtWidgets.QGroupBox(self.centralWidget)
        self.SBSFiltershape.setGeometry(QtCore.QRect(1110, 10, 841, 311))
        self.SBSFiltershape.setMouseTracking(False)
        self.SBSFiltershape.setAcceptDrops(False)
        self.SBSFiltershape.setFlat(True)
        self.SBSFiltershape.setObjectName("SBSFiltershape")
        self.stateEqu = QtWidgets.QGroupBox(self.centralWidget)
        self.stateEqu.setGeometry(QtCore.QRect(40, 770, 221, 381))
        self.stateEqu.setCheckable(False)
        self.stateEqu.setChecked(False)
        self.stateEqu.setObjectName("stateEqu")
        self.layoutWidget = QtWidgets.QWidget(self.stateEqu)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 146, 293))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.AWG = QtWidgets.QLabel(self.layoutWidget)
        self.AWG.setObjectName("AWG")
        self.verticalLayout_2.addWidget(self.AWG)
        self.OSA = QtWidgets.QLabel(self.layoutWidget)
        self.OSA.setObjectName("OSA")
        self.verticalLayout_2.addWidget(self.OSA)
        self.DFB = QtWidgets.QLabel(self.layoutWidget)
        self.DFB.setObjectName("DFB")
        self.verticalLayout_2.addWidget(self.DFB)
        self.DC = QtWidgets.QLabel(self.layoutWidget)
        self.DC.setObjectName("DC")
        self.verticalLayout_2.addWidget(self.DC)
        self.EVNA = QtWidgets.QLabel(self.layoutWidget)
        self.EVNA.setObjectName("EVNA")
        self.verticalLayout_2.addWidget(self.EVNA)
        self.EDFA1 = QtWidgets.QLabel(self.layoutWidget)
        self.EDFA1.setObjectName("EDFA1")
        self.verticalLayout_2.addWidget(self.EDFA1)
        self.EDFA2 = QtWidgets.QLabel(self.layoutWidget)
        self.EDFA2.setObjectName("EDFA2")
        self.verticalLayout_2.addWidget(self.EDFA2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.AWGs = QtWidgets.QLineEdit(self.layoutWidget)
        self.AWGs.setMouseTracking(True)
        self.AWGs.setText("")
        self.AWGs.setFrame(False)
        self.AWGs.setObjectName("AWGs")
        self.verticalLayout.addWidget(self.AWGs)
        self.OSAs = QtWidgets.QLineEdit(self.layoutWidget)
        self.OSAs.setMouseTracking(True)
        self.OSAs.setText("")
        self.OSAs.setFrame(False)
        self.OSAs.setObjectName("OSAs")
        self.verticalLayout.addWidget(self.OSAs)
        self.DFBs = QtWidgets.QLineEdit(self.layoutWidget)
        self.DFBs.setMouseTracking(True)
        self.DFBs.setText("")
        self.DFBs.setFrame(False)
        self.DFBs.setObjectName("DFBs")
        self.verticalLayout.addWidget(self.DFBs)
        self.DCs = QtWidgets.QLineEdit(self.layoutWidget)
        self.DCs.setMouseTracking(True)
        self.DCs.setText("")
        self.DCs.setFrame(False)
        self.DCs.setObjectName("DCs")
        self.verticalLayout.addWidget(self.DCs)
        self.EVNAs = QtWidgets.QLineEdit(self.layoutWidget)
        self.EVNAs.setMouseTracking(True)
        self.EVNAs.setText("")
        self.EVNAs.setFrame(False)
        self.EVNAs.setObjectName("EVNAs")
        self.verticalLayout.addWidget(self.EVNAs)
        self.EDFA1s = QtWidgets.QLineEdit(self.layoutWidget)
        self.EDFA1s.setMouseTracking(True)
        self.EDFA1s.setText("")
        self.EDFA1s.setFrame(False)
        self.EDFA1s.setObjectName("EDFA1s")
        self.verticalLayout.addWidget(self.EDFA1s)
        self.EDFA2s = QtWidgets.QLineEdit(self.layoutWidget)
        self.EDFA2s.setMouseTracking(True)
        self.EDFA2s.setText("")
        self.EDFA2s.setFrame(False)
        self.EDFA2s.setObjectName("EDFA2s")
        self.verticalLayout.addWidget(self.EDFA2s)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.Echeck = QtWidgets.QPushButton(self.stateEqu)
        self.Echeck.setGeometry(QtCore.QRect(50, 330, 101, 41))
        self.Echeck.setObjectName("Echeck")
        self.DCpower = QtWidgets.QGroupBox(self.centralWidget)
        self.DCpower.setGeometry(QtCore.QRect(1110, 350, 841, 131))
        self.DCpower.setFlat(True)
        self.DCpower.setCheckable(False)
        self.DCpower.setObjectName("DCpower")
        self.layoutWidget1 = QtWidgets.QWidget(self.DCpower)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 796, 48))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DC_CH1 = QtWidgets.QLabel(self.layoutWidget1)
        self.DC_CH1.setObjectName("DC_CH1")
        self.horizontalLayout.addWidget(self.DC_CH1)
        self.DC1 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.DC1.setObjectName("DC1")
        self.horizontalLayout.addWidget(self.DC1)
        self.V1 = QtWidgets.QLabel(self.layoutWidget1)
        self.V1.setObjectName("V1")
        self.horizontalLayout.addWidget(self.V1)
        self.DC_CH1_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.DC_CH1_2.setObjectName("DC_CH1_2")
        self.horizontalLayout.addWidget(self.DC_CH1_2)
        self.DC2 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.DC2.setObjectName("DC2")
        self.horizontalLayout.addWidget(self.DC2)
        self.V2 = QtWidgets.QLabel(self.layoutWidget1)
        self.V2.setObjectName("V2")
        self.horizontalLayout.addWidget(self.V2)
        self.DC_CH1_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.DC_CH1_3.setObjectName("DC_CH1_3")
        self.horizontalLayout.addWidget(self.DC_CH1_3)
        self.DC3 = QtWidgets.QDoubleSpinBox(self.layoutWidget1)
        self.DC3.setObjectName("DC3")
        self.horizontalLayout.addWidget(self.DC3)
        self.V3 = QtWidgets.QLabel(self.layoutWidget1)
        self.V3.setObjectName("V3")
        self.horizontalLayout.addWidget(self.V3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.DCoutput = QtWidgets.QPushButton(self.layoutWidget1)
        self.DCoutput.setObjectName("DCoutput")
        self.horizontalLayout_2.addWidget(self.DCoutput)
        self.AWGpanel = QtWidgets.QGroupBox(self.centralWidget)
        self.AWGpanel.setGeometry(QtCore.QRect(1110, 500, 851, 231))
        self.AWGpanel.setMouseTracking(False)
        self.AWGpanel.setAcceptDrops(False)
        self.AWGpanel.setFlat(True)
        self.AWGpanel.setObjectName("AWGpanel")
        self.pushButton = QtWidgets.QPushButton(self.AWGpanel)
        self.pushButton.setGeometry(QtCore.QRect(10, 30, 81, 41))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.EVNAPanel = QtWidgets.QGroupBox(self.centralWidget)
        self.EVNAPanel.setGeometry(QtCore.QRect(1120, 750, 831, 261))
        self.EVNAPanel.setMouseTracking(False)
        self.EVNAPanel.setAcceptDrops(False)
        self.EVNAPanel.setFlat(True)
        self.EVNAPanel.setObjectName("EVNAPanel")
        self.layoutWidget2 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.layoutWidget3 = QtWidgets.QWidget(self.centralWidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralWidget)
        self.openGLWidget.setGeometry(QtCore.QRect(40, 170, 981, 561))
        self.openGLWidget.setObjectName("openGLWidget")
        SBSsystem.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(SBSsystem)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 2282, 37))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        SBSsystem.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(SBSsystem)
        self.mainToolBar.setObjectName("mainToolBar")
        SBSsystem.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(SBSsystem)
        self.statusBar.setObjectName("statusBar")
        SBSsystem.setStatusBar(self.statusBar)
        self.actionAWG = QtWidgets.QAction(SBSsystem)
        self.actionAWG.setObjectName("actionAWG")
        self.actionVNA = QtWidgets.QAction(SBSsystem)
        self.actionVNA.setObjectName("actionVNA")
        self.menu_2.addAction(self.actionAWG)
        self.menu_2.addAction(self.actionVNA)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(SBSsystem)
        QtCore.QMetaObject.connectSlotsByName(SBSsystem)

    def retranslateUi(self, SBSsystem):
        _translate = QtCore.QCoreApplication.translate
        SBSsystem.setWindowTitle(_translate("SBSsystem", "SBSsystem"))
        self.SBSFiltershape.setTitle(_translate("SBSsystem", "SBS Filter Control Panel"))
        self.stateEqu.setTitle(_translate("SBSsystem", "Equipment States"))
        self.AWG.setText(_translate("SBSsystem", "AWG"))
        self.OSA.setText(_translate("SBSsystem", "OSA"))
        self.DFB.setText(_translate("SBSsystem", "DFB"))
        self.DC.setText(_translate("SBSsystem", "DC"))
        self.EVNA.setText(_translate("SBSsystem", "EVNA"))
        self.EDFA1.setText(_translate("SBSsystem", "EDFA1"))
        self.EDFA2.setText(_translate("SBSsystem", "EDFA2"))
        self.Echeck.setText(_translate("SBSsystem", "Check"))
        self.DCpower.setTitle(_translate("SBSsystem", "DC Power panel"))
        self.DC_CH1.setText(_translate("SBSsystem", "DC_CH1"))
        self.V1.setText(_translate("SBSsystem", "V"))
        self.DC_CH1_2.setText(_translate("SBSsystem", "DC_CH2"))
        self.V2.setText(_translate("SBSsystem", "V"))
        self.DC_CH1_3.setText(_translate("SBSsystem", "DC_CH3"))
        self.V3.setText(_translate("SBSsystem", "V"))
        self.DCoutput.setText(_translate("SBSsystem", "Output ON"))
        self.AWGpanel.setTitle(_translate("SBSsystem", "AWG Control Panel"))
        self.pushButton.setText(_translate("SBSsystem", "ON/OFF"))
        self.EVNAPanel.setTitle(_translate("SBSsystem", "EVNA Control Panel"))
        self.menu.setTitle(_translate("SBSsystem", "文件"))
        self.menu_2.setTitle(_translate("SBSsystem", "设备检查"))
        self.actionAWG.setText(_translate("SBSsystem", "AWG"))
        self.actionVNA.setText(_translate("SBSsystem", "VNA"))
