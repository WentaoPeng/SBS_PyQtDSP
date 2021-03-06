#! encoding = utf-8
''' GUI Panels. '''

# import standard libraries
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QObject
import pyqtgraph as pg
import pyvisa
import time
import numpy as np
from GUI import SharedWidgets as Shared
from API import AWGapi as api_awg
from API import validators as api_val
from API import PNAapi as api_pna
from API import LightAPI as api_light
from API import EDFAAPI as api_edfa
from pyqtgraph import siEval
import SBS_DSP
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


class AWGStatus(QtWidgets.QGroupBox):
    '''
        AWG状态显示
    '''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle('AWG Status')
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setCheckable(True)
        self.setChecked(False)

        # 设定检测AWG状态信息，运行，输出通道等
        refreshButton = QtWidgets.QPushButton('Manual Refresh')
        moreInfoButton = QtWidgets.QPushButton('More Info.')
        self.addressText = QtWidgets.QLabel()
        self.InstEnable = QtWidgets.QLabel()
        self.ChannelNum = QtWidgets.QLabel()
        self.Amplitude = QtWidgets.QLabel()
        self.DACset = QtWidgets.QLabel()
        self.ShapeStatus = QtWidgets.QLabel()
        self.CWSet = QtWidgets.QLabel()
        self.BWSet = QtWidgets.QLabel()
        self.DFSet = QtWidgets.QLabel()
        self.errMsgLabel = QtWidgets.QLabel()
        errorMsgBtn = QtWidgets.QPushButton('Error MsgLog')

        # AWG波形设置信息框
        designGroup = QtWidgets.QGroupBox()
        designGroup.setTitle('AWG-PUMP DesignInfo')
        designGroup.setAlignment(QtCore.Qt.AlignLeft)
        designGroup.setCheckable(False)
        designGroupLayout = QtWidgets.QGridLayout()
        designGroupLayout.addWidget(QtWidgets.QLabel('Shape Status'), 0, 0)
        designGroupLayout.addWidget(QtWidgets.QLabel('CW'), 1, 0)
        designGroupLayout.addWidget(QtWidgets.QLabel('BW'), 2, 0)
        designGroupLayout.addWidget(QtWidgets.QLabel('DF'), 3, 0)
        designGroupLayout.addWidget(self.ShapeStatus, 0, 1)
        designGroupLayout.addWidget(self.CWSet, 1, 1)
        designGroupLayout.addWidget(self.BWSet, 2, 1)
        designGroupLayout.addWidget(self.DFSet, 3, 1)
        designGroup.setLayout(designGroupLayout)

        # AWGStatus整体布局
        mainLayout = QtWidgets.QGridLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        # top Buttons布局
        mainLayout.addWidget(refreshButton, 0, 0, 1, 2)
        mainLayout.addWidget(moreInfoButton, 0, 2, 1, 2)
        mainLayout.addWidget(QtWidgets.QLabel('Inst Name'), 1, 0)
        mainLayout.addWidget(self.addressText, 1, 1, 1, 3)
        # 基本状态信息
        mainLayout.addWidget(QtWidgets.QLabel('InstEnable'), 2, 0)
        mainLayout.addWidget(self.InstEnable, 2, 1, 1, 3)
        mainLayout.addWidget(QtWidgets.QLabel('ChannelNum'), 3, 0)
        mainLayout.addWidget(self.ChannelNum, 3, 1, 1, 3)
        mainLayout.addWidget(QtWidgets.QLabel('Amp'), 4, 0)
        mainLayout.addWidget(self.Amplitude, 4, 1, 1, 3)
        mainLayout.addWidget(QtWidgets.QLabel('DACset'), 5, 0)
        mainLayout.addWidget(self.DACset, 5, 1, 1, 3)
        #     AWG波形设置信息框
        mainLayout.addWidget(designGroup, 6, 0, 3, 4)
        mainLayout.addWidget(errorMsgBtn, 9, 0)
        mainLayout.addWidget(self.errMsgLabel, 9, 1, 1, 3)
        self.setLayout(mainLayout)
        #     点击事件触发
        refreshButton.clicked.connect(self.refresh_fun)
        moreInfoButton.clicked.connect(self.show_InstMoreInfo)
        errorMsgBtn.clicked.connect(self.err_msg)

        # 初始显示
        self.print_info()

        self.clicked.connect(self.check)

    def check(self):
        ''' Enable/disable this groupbox '''

        if (self.parent.testModeAction.isChecked() or self.parent.AWGHandle):
            self.setChecked(True)
            self.parent.AWGStatus.setChecked(True)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No AWG is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.AWGStatus.setChecked(False)

        self.parent.AWGStatus.print_info()

    def print_info(self):
        '''初始见面显示信息'''
        # self.addressText.setText(self.parent.)
        self.addressText.setText(self.parent.AWGInfo.instName)
        self.InstEnable.setText('ON' if self.parent.AWGInfo.AWG_Status else 'OFF')
        self.ChannelNum.setText(str(self.parent.AWGInfo.ChannelNum))
        self.DACset.setText(str(self.parent.AWGInfo.DAC_index))
        self.ShapeStatus.setText(self.parent.AWGInfo.mod_sel)
        self.CWSet.setText(str(self.parent.AWGInfo.CFFreq) + 'Hz')
        self.BWSet.setText(str(self.parent.AWGInfo.BWFreq) + 'Hz')
        self.DFSet.setText(str(self.parent.AWGInfo.DFFreq) + 'Hz')
        self.Amplitude.setText(str(self.parent.AWGInfo.AWGPower) + 'Mv')

    def refresh_fun(self):
        # if self.parent.testModeAction.isChecked() or  (not self.parent.AWGHandle):
        #     pass
        # else:
        self.addressText.setText(self.parent.AWGInfo.instName)
        self.InstEnable.setText('ON' if self.parent.AWGInfo.AWG_Status else 'OFF')
        self.ChannelNum.setText(str(self.parent.AWGInfo.ChannelNum))
        self.DACset.setText(str(self.parent.AWGInfo.DAC_index))
        self.ShapeStatus.setText(self.parent.AWGInfo.mod_sel)
        self.CWSet.setText(str(self.parent.AWGInfo.CFFreq) + 'Hz')
        self.BWSet.setText(str(self.parent.AWGInfo.BWFreq) + 'Hz')
        self.DFSet.setText(str(self.parent.AWGInfo.DFFreq) + 'Hz')
        self.Amplitude.setText(str(self.parent.AWGInfo.AWGPower) + 'Mv')

    def show_InstMoreInfo(self):
        # 待扩展
        return

    def err_msg(self):
        '''AWG反馈错误信息'''
        if self.parent.AWGHandle:
            self.parent.AWGInfo.errMsg = api_awg.M9502A.err_check()
            self.errMsgLabel.setText(self.parent.AWGInfo.errMsg)
        else:
            pass


class PNACtrl(QtWidgets.QGroupBox):
    '''
    VNA控制界面
    '''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle('PNA Control')
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setCheckable(True)
        self.setChecked(False)

        response = QtWidgets.QGroupBox()
        response.setTitle('RESPONSE')
        response.setFlat(True)
        response.setAlignment(QtCore.Qt.AlignTop)
        responseLayout = QtWidgets.QGridLayout()
        responseLayout.setAlignment(QtCore.Qt.AlignTop)
        # responseLayout.setSpacing(0)

        self.addressText = QtWidgets.QLabel()
        # self.InstEnable = QtWidgets.QLabel()
        self.AvgPoints = QtWidgets.QSpinBox()
        self.InitialBtu = QtWidgets.QPushButton('Initial')
        self.EnterBtu = QtWidgets.QPushButton('Enter')
        self.AllMeasBtu = QtWidgets.QPushButton('ALLMeas')

        self.ScaleSet = QtWidgets.QWidget()
        self.ScaleSetUnitSel = QtWidgets.QComboBox()
        self.ScaleSetUnitSel.addItems(['S11', 'S12', 'S21', 'S22'])
        self.ScaleSetUnitSel.setCurrentIndex(1)

        responseLayout.addWidget(QtWidgets.QLabel('Inst:'), 0, 0)
        responseLayout.addWidget(self.addressText, 0, 1, 1, 3)
        responseLayout.addWidget(QtWidgets.QLabel('Scale'), 1, 0)
        responseLayout.addWidget(self.ScaleSetUnitSel, 1, 1, 1, 3)
        responseLayout.addWidget(QtWidgets.QLabel('AvgPoints'), 2, 0)
        responseLayout.addWidget(self.AvgPoints, 2, 1, 1, 3)
        responseLayout.addWidget(self.InitialBtu, 3, 0, 1, 2)
        responseLayout.addWidget(self.AllMeasBtu, 3, 2, 1, 2)
        response.setLayout(responseLayout)

        stimulus = QtWidgets.QGroupBox()
        stimulus.setTitle('STIMULUS')
        stimulus.setFlat(True)
        stimulus.setAlignment(QtCore.Qt.AlignLeft)
        stimulusLayout = QtWidgets.QGridLayout()
        stimulusLayout.setSpacing(0)

        self.PointSet = QtWidgets.QWidget()
        self.SPoints = QtWidgets.QLineEdit()
        self.SPoints.setPlaceholderText('High sampling')
        SPointsLayout = QtWidgets.QGridLayout()
        SPointsLayout.addWidget(QtWidgets.QLabel('Sweep Points'), 0, 0)
        SPointsLayout.addWidget(self.SPoints, 0, 1, 1, 2)
        self.PointSet.setLayout(SPointsLayout)

        self.StartFset = QtWidgets.QWidget()
        self.StartFsetFill = QtWidgets.QLineEdit('10')
        self.StartFsetUnitSel = QtWidgets.QComboBox()
        self.StartFsetUnitSel.addItems(['Hz', 'KHz', 'MHz', 'GHz'])
        self.StartFsetUnitSel.setCurrentIndex(2)
        StartFLayout = QtWidgets.QHBoxLayout()
        StartFLayout.addWidget(QtWidgets.QLabel('StartFerq'))
        StartFLayout.addWidget(self.StartFsetFill)
        StartFLayout.addWidget(self.StartFsetUnitSel)
        self.StartFset.setLayout(StartFLayout)

        self.EndFset = QtWidgets.QWidget()
        self.EndFsetFill = QtWidgets.QLineEdit('20')
        self.EndFsetUnitSel = QtWidgets.QComboBox()
        self.EndFsetUnitSel.addItems(['Hz', 'KHz', 'MHz', 'GHz'])
        self.EndFsetUnitSel.setCurrentIndex(3)
        EndFsetLayout = QtWidgets.QHBoxLayout()
        EndFsetLayout.addWidget(QtWidgets.QLabel('EndFerq'))
        EndFsetLayout.addWidget(self.EndFsetFill)
        EndFsetLayout.addWidget(self.EndFsetUnitSel)
        self.EndFset.setLayout(EndFsetLayout)

        self.powerset = QtWidgets.QWidget()
        self.powersetFill = QtWidgets.QLineEdit('0')
        self.powersetUnitSel = QtWidgets.QComboBox()
        self.powersetUnitSel.addItems(['dBm', 'mW'])
        self.powersetUnitSel.setCurrentIndex(0)
        powersetLayout = QtWidgets.QHBoxLayout()
        powersetLayout.addWidget(QtWidgets.QLabel('Power'))
        powersetLayout.addWidget(self.powersetFill)
        powersetLayout.addWidget(self.powersetUnitSel)
        self.powerset.setLayout(powersetLayout)

        stimulusLayout.addWidget(self.StartFset, 2, 1, 1, 2)
        stimulusLayout.addWidget(self.EndFset, 3, 1, 1, 2)
        stimulusLayout.addWidget(self.PointSet, 1, 1, 1, 2)
        stimulusLayout.addWidget(self.powerset, 0, 1, 1, 2)
        stimulusLayout.addWidget(self.EnterBtu, 4, 1)
        stimulus.setLayout(stimulusLayout)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.addWidget(response)
        mainLayout.addWidget(stimulus)
        self.setLayout(mainLayout)

        # 信息同步，单位转换
        self.AvgPoints.valueChanged.connect(self.tune_mod_parameter)
        self.ScaleSetUnitSel.currentIndexChanged.connect(self.tune_mod_parameter)
        self.powersetFill.textChanged.connect(self.tune_mod_parameter)
        self.SPoints.textChanged.connect(self.tune_mod_parameter)
        self.StartFsetFill.textChanged.connect(self.tune_mod_parameter)
        self.EndFsetFill.textChanged.connect(self.tune_mod_parameter)

        self.InitialBtu.clicked.connect(self.InitialF)
        self.EnterBtu.clicked.connect(self.setPNA)
        self.AllMeasBtu.clicked.connect(self.AllDisplay)

        self.clicked.connect(self.check)

    def AllDisplay(self):
        if self.parent.testModeAction.isChecked() or self.parent.PNAHandle:
            self.parent.PNAHandle.allmeas()
            self.parent.Display = 1

    def InitialF(self):
        if self.parent.testModeAction.isChecked() or self.parent.PNAHandle:
            self.parent.PNAHandle.PNA_setup(measName=self.parent.PNAInfo.Scale)

    def setPNA(self):
        if self.parent.testModeAction.isChecked() or self.parent.PNAHandle:
            self.parent.PNAHandle.configure(startFreq=self.parent.PNAInfo.StartFerq,
                                            endFreq=self.parent.PNAInfo.EndFerq,
                                            numpoints=self.parent.PNAInfo.SweepPoints,
                                            avgpoints=self.parent.PNAInfo.AvgPoints,
                                            power=self.parent.PNAInfo.Power)

    def tune_mod_parameter(self):
        self.parent.PNAInfo.Scale = self.ScaleSetUnitSel.currentText()
        self.parent.PNAInfo.AvgPoints = int(self.AvgPoints.text())
        self.parent.PNAInfo.SweepPoints = int(self.SPoints.text())
        self.parent.PNAInfo.Power = int(self.powersetFill.text())
        SF_status, SF_value = api_val.val_PNA_F(self.StartFsetFill.text(),
                                                self.StartFsetUnitSel.currentText())
        EF_status, EF_value = api_val.val_PNA_F(self.EndFsetFill.text(),
                                                self.EndFsetUnitSel.currentText())

        self.parent.PNAInfo.StartFerq = SF_value
        self.parent.PNAInfo.EndFerq = EF_value

    def check(self):
        ''' Enable/disable this groupbox '''
        if (self.parent.testModeAction.isChecked() or self.parent.PNAHandle):
            self.setChecked(True)
            self.parent.PNACtrl.setChecked(True)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No PNAN5225A is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.PNACtrl.setChecked(False)

        # self.parent.PNACtrl.print_info()


class AWGCtrl(QtWidgets.QGroupBox):
    '''
    AWG控制界面
    '''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle('AWG Control')
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setCheckable(True)
        self.setChecked(False)

        #     AWG设置面板设置参量
        AWGWidget = QtWidgets.QWidget()
        self.DACset = QtWidgets.QSpinBox()
        self.channelNumset = Shared.AWGChannelBox()

        #     显示参量
        AWGLayout = QtWidgets.QGridLayout()
        AWGLayout.addWidget(QtWidgets.QLabel('DAC'), 0, 0)
        AWGLayout.addWidget(self.DACset, 0, 1, 1, 2)

        AWGLayout.addWidget(QtWidgets.QLabel('AWGChannel'), 1, 0)
        AWGLayout.addWidget(self.channelNumset, 1, 1, 1, 3)
        AWGWidget.setLayout(AWGLayout)

        #     AWG输出功率设置以及运行按钮
        self.AWGPowerSwitchBtu = QtWidgets.QPushButton('OFF')
        self.AWGPowerSwitchBtu.setCheckable(True)
        AWGPowerInput = QtWidgets.QPushButton('Set Power')

        AWGPowerLayout = QtWidgets.QHBoxLayout()
        AWGPowerLayout.setAlignment(QtCore.Qt.AlignLeft)
        AWGPowerLayout.addWidget(AWGPowerInput)
        AWGPowerLayout.addWidget(QtWidgets.QLabel('Pump Switch'))
        AWGPowerLayout.addWidget(self.AWGPowerSwitchBtu)
        AWGPowerCtrl = QtWidgets.QWidget()
        AWGPowerCtrl.setLayout(AWGPowerLayout)

        # self.powerSwitchTimer = QtCore.QTimer()
        # self.powerSwitchTimer.setInterval(500)
        # self.powerSwitchTimer.setSingleShot(True)
        # self.powerSwitchProgBar = QtWidgets.QProgressBar()
        # self.progDialog = QtWidgets.QDialog()
        # self.progDialog.setWindowTitle('AWG Running')
        # progDialogLayout = QtWidgets.QVBoxLayout()
        # progDialogLayout.addWidget(self.powerSwitchProgBar)
        # self.progDialog.setLayout(progDialogLayout)

        #     pump设计子界面
        PumpDesign = QtWidgets.QGroupBox()
        PumpDesign.setTitle('PUMPDesign_AWG')
        PumpDesign.setFlat(True)
        PumpDesign.setAlignment(QtCore.Qt.AlignLeft)
        PumpLayout = QtWidgets.QGridLayout()
        PumpLayout.setSpacing(0)

        self.PumpModeSel = QtWidgets.QComboBox()
        self.PumpModeSel.addItems(api_awg.Shape_MODE_LIST)

        self.CenterFreq = QtWidgets.QWidget()
        self.CenterFreqFill = QtWidgets.QLineEdit('10')
        self.CenterFreqUnitSel = QtWidgets.QComboBox()
        self.CenterFreqUnitSel.addItems(['Hz', 'KHz', 'MHz', 'GHz'])
        self.CenterFreqUnitSel.setCurrentIndex(3)
        CenterFreqLayout = QtWidgets.QHBoxLayout()
        CenterFreqLayout.addWidget(QtWidgets.QLabel('CenterFreq'))
        CenterFreqLayout.addWidget(self.CenterFreqFill)
        CenterFreqLayout.addWidget(self.CenterFreqUnitSel)
        self.CenterFreq.setLayout(CenterFreqLayout)

        self.BandWidth = QtWidgets.QWidget()
        self.BandWidthFill = QtWidgets.QLineEdit('200')
        self.BandWidthUnitSel = QtWidgets.QComboBox()
        self.BandWidthUnitSel.addItems(['Hz', 'KHz', 'MHz', 'GHz'])
        self.BandWidthUnitSel.setCurrentIndex(2)
        BandWidthLayout = QtWidgets.QHBoxLayout()
        BandWidthLayout.addWidget(QtWidgets.QLabel('BandWidth'))
        BandWidthLayout.addWidget(self.BandWidthFill)
        BandWidthLayout.addWidget(self.BandWidthUnitSel)
        self.BandWidth.setLayout(BandWidthLayout)

        self.CombFreq = QtWidgets.QWidget()
        self.CombFreqFill = QtWidgets.QLineEdit('10')
        self.CombFreqUnitSel = QtWidgets.QComboBox()
        self.CombFreqUnitSel.addItems(['Hz', 'KHz', 'MHz', 'GHz'])
        self.CombFreqUnitSel.setCurrentIndex(2)
        CombFreqLayout = QtWidgets.QHBoxLayout()
        CombFreqLayout.addWidget(QtWidgets.QLabel('Comb DF'))
        CombFreqLayout.addWidget(self.CombFreqFill)
        CombFreqLayout.addWidget(self.CombFreqUnitSel)
        self.CombFreq.setLayout(CombFreqLayout)

        self.PumpDesignDoneBtu = QtWidgets.QPushButton('Done')
        self.PumpDesignDoneBtu.setCheckable(True)

        PumpLayout.addWidget(QtWidgets.QLabel('Pump Shape :'), 0, 0)
        PumpLayout.addWidget(self.PumpDesignDoneBtu, 1, 0, 4, 1)
        PumpLayout.addWidget(self.PumpModeSel, 0, 1)
        PumpLayout.addWidget(self.CenterFreq, 1, 1, 2, 3)
        PumpLayout.addWidget(self.BandWidth, 2, 1, 2, 3)
        PumpLayout.addWidget(self.CombFreq, 3, 1, 2, 3)
        PumpDesign.setLayout(PumpLayout)

        #     设置主界面
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.addWidget(AWGPowerCtrl)
        mainLayout.addWidget(AWGWidget)
        mainLayout.addWidget(PumpDesign)
        self.setLayout(mainLayout)

        # 设计窗口若有改变，更改后台参数，滤波类型编号，中心波长，带宽，间隔等参数同步改变
        self.DACset.valueChanged.connect(self.tune_mod_parameter)
        self.channelNumset.currentIndexChanged.connect(self.tune_mod_parameter)
        self.PumpModeSel.currentIndexChanged.connect(self.tune_mod_parameter)
        self.CenterFreqFill.textChanged.connect(self.tune_mod_parameter)
        self.CenterFreqUnitSel.currentIndexChanged.connect(self.tune_mod_parameter)
        self.BandWidthFill.textChanged.connect(self.tune_mod_parameter)
        self.BandWidthUnitSel.currentIndexChanged.connect(self.tune_mod_parameter)
        self.CombFreqFill.textChanged.connect(self.tune_mod_parameter)
        self.CombFreqUnitSel.currentIndexChanged.connect(self.tune_mod_parameter)

        AWGPowerInput.clicked.connect(self.AWGRFPower)
        self.AWGPowerSwitchBtu.clicked.connect(self.AWGRFPowerSwitch_auto)
        self.AWGPowerSwitchBtu.toggled.connect(self.AWGPowerSwitch_Label)
        # self.powerSwitchTimer.timeout.connect(self.ramp_AWGRFPower)
        # 设计泵浦事件
        self.PumpDesignDoneBtu.clicked.connect(self.DesignPump)

        self.clicked.connect(self.check)

    def check(self):
        if (self.parent.testModeAction.isChecked() or self.parent.AWGHandle):
            self.setChecked(True)
            self.parent.AWGCtrl.setChecked(True)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No AWG is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.AWGCtrl.setChecked(False)

    def tune_mod_parameter(self):
        # 状态信息同步
        # 波形状态
        mod_index = self.PumpModeSel.currentIndex()
        self.parent.AWGInfo.mod_index = mod_index
        self.parent.AWGInfo.mod_sel = self.PumpModeSel.currentText()
        print(self.PumpModeSel.currentText())
        # DAC选择
        DAC_index = self.DACset.text()
        self.parent.AWGInfo.DAC_index = DAC_index
        print(DAC_index)
        # 通道选择
        Channel_N = api_val.AWGCHANNELSET[self.channelNumset.currentIndex()]
        self.parent.AWGInfo.ChannelNum = Channel_N
        print(Channel_N)
        CF_status, CF_freq = api_val.val_awgCW_mod_freq(self.CenterFreqFill.text(),
                                                        self.CenterFreqUnitSel.currentText())
        BW_status, BW_freq = api_val.val_awgBW_mod_freq(self.BandWidthFill.text(),
                                                        self.BandWidthUnitSel.currentText())
        DF_status, DF_freq = api_val.val_awgDF_mod_freq(self.CombFreqFill.text(),
                                                        self.CombFreqUnitSel.currentText())
        self.CenterFreqFill.setStyleSheet('border:1px solid {:s}'.format(Shared.msgcolor(CF_status)))
        self.BandWidthFill.setStyleSheet('border:1px solid {:s}'.format(Shared.msgcolor(BW_status)))
        self.CombFreqFill.setStyleSheet('border:1px solid {:s}'.format(Shared.msgcolor(DF_status)))

        self.parent.AWGInfo.CFFreq = CF_freq
        self.parent.AWGInfo.BWFreq = BW_freq
        self.parent.AWGInfo.DFFreq = DF_freq

    # def ramp_AWGRFPower(self):
    #     '''
    #
    #     :return: 成功状态
    #     '''
    #     try:
    #         this_power = next(self.ramper)
    #         if self.parent.testModeAction.isChecked():
    #             vCode = pyvisa.constants.StatusCode.success
    #         else:
    #             vCode = self.parent.AWGHandle.set_amplitude(amplitude=this_power,
    #                                                         channel=self.parent.AWGInfo.ChannelNum)
    #
    #         if vCode == pyvisa.constants.StatusCode.success:
    #             self.parent.AWGInfo.AWGPower = self.parent.AWGHandle.read_power_toggle()
    #             self.parent.AWGStatus.print_info()
    #             self.powerSwitchProgBar.setValue(self.powerSwitchProgBar.value()+1)
    #             # 开始timer
    #             self.powerSwitchTimer.start()
    #         else:
    #             self.powerSwitchTimer.stop()
    #             msg = Shared.InstStatus(self, vCode)
    #             msg.exec_()
    #     except StopIteration:
    #         self.powerSwitchTimer.stop()
    #         self.progDialog.accept()

    def AWGRFPower(self):
        if self.parent.testModeAction.isChecked():

            target_Power, okay = QtWidgets.QInputDialog.getDouble(self, 'RF POWER',
                                                                  'Manual Input (0mV to 1000mV)',
                                                                  self.parent.AWGInfo.AWGPower, 0, 1000, 0.01)
            self.parent.AWGInfo.AWGPower = 500

        else:
            target_Power, okay = QtWidgets.QInputDialog.getDouble(self, 'RF POWER',
                                                                  'Manual Input (0mV to 1000mV)', 500, 0, 1000, 0.01)
            self.parent.AWGInfo.AWGPower = target_Power / 1000

        if okay:
            if self.parent.testModeAction.isChecked():
                pass
            else:
                self.parent.AWGHandle.set_amplitude(amplitude=self.parent.AWGInfo.AWGPower,
                                                    channel=self.parent.AWGInfo.ChannelNum)
        else:
            pass

    def AWGRFPowerSwitch_auto(self, status):
        '''自动打开关闭RF输出'''
        if status:
            if self.parent.testModeAction.isChecked():
                pass
            else:
                # 设置波形np.array，并检验，以及下载波形，Running
                # ys = np.ones(len(self.parent.AWGInfo.ys))*self.parent.AWGInfo.ys
                self.parent.AWGHandle.clear_all_wfm()
                wfmID = self.parent.AWGHandle.download_wfm(wfmData=self.parent.AWGInfo.AWGwave,
                                                           ch=self.parent.AWGInfo.ChannelNum)
                self.parent.AWGHandle.play(wfmID=wfmID, ch=self.parent.AWGInfo.ChannelNum)
                self.parent.AWGHandle.err_check()
                self.parent.AWGInfo.AWG_Status = True
        else:
            self.parent.AWGHandle.stop(ch=self.parent.AWGInfo.ChannelNum)
            self.parent.AWGHandle.delete_segment(ch=self.parent.AWGInfo.ChannelNum)
            self.parent.AWGInfo.AWG_Status = False

        self.parent.AWGStatus.print_info()

    def AWGPowerSwitch_Label(self, toggle_state):
        '''更换按键文本'''
        if toggle_state:
            self.AWGPowerSwitchBtu.setText('ON')
        else:
            self.AWGPowerSwitchBtu.setText('OFF')

    def DesignPump(self):

        AWG_framerate = 64e9  # AWG采样率
        Df = 1 * 10 ** 6
        # FM_AWG = AWG_framerate / 2.56   # AWG最高分析频率
        N_AWG = int(AWG_framerate / Df)
        t_AWG = N_AWG * (1 / AWG_framerate)
        CF = self.parent.AWGInfo.CFFreq
        BW = self.parent.AWGInfo.BWFreq
        DF = self.parent.AWGInfo.DFFreq

        if self.parent.AWGInfo.mod_index == 0:
            f_list, amp_list, phase_list = SBS_DSP.square_filter(CF, BW, DF)
        elif self.parent.AWGInfo.mod_index == 1:
            f_list, amp_list, phase_list = SBS_DSP.triangle_filter(CF, BW, DF)
        elif self.parent.AWGInfo.mod_index == 2:
            f_list, amp_list, phase_list = SBS_DSP.Band_stop_filter(CF, BW, DF, signal_BW=1 * 10 ** 9)
        elif self.parent.AWGInfo.mod_index == 3:
            f_list, amp_list, phase_list = SBS_DSP.Guass_filter(CF, BW, DF)
        else:
            amp_list = []
            f_list = []
            phase_list = []

        ts = np.linspace(0, t_AWG, N_AWG, endpoint=False)
        ys = SBS_DSP.synthesize1(amp_list, f_list, ts, phase_list)
        self.parent.AWGInfo.f_list = f_list
        self.parent.AWGInfo.amp_list = amp_list
        self.parent.AWGInfo.phase_list = phase_list
        self.parent.AWGInfo.ts = ts
        self.parent.AWGInfo.ys = ys
        wavefile = (ys - min(ys)) / (max(ys) - min(ys)) - 0.5
        self.parent.AWGInfo.AWGwave = np.ones(len(wavefile)) * wavefile
        FFT_y, Fre = SBS_DSP.get_fft(ys, AWG_framerate)
        self.parent.AWGInfo.FFT_y = FFT_y
        self.parent.AWGInfo.Fre = Fre
        # Lorenz拟合
        Tb = 20 * 10 ** 6  # 10~30Mhz布里渊线宽
        omega_sbs = 9.7e9  # 布里渊平移量
        f_measure = np.arange(CF - 2 * BW - omega_sbs, CF + 2 * BW - omega_sbs, 10 ** 6)
        self.parent.AWGInfo.f_measure = f_measure
        total_lorenz = SBS_DSP.add_lorenz(f_measure, amp_list * 0.008, f_list, Tb)

        self.parent.AWGInfo.gb = total_lorenz
        # 初始化AWG采样率set_fs
        self.parent.AWGHandle.set_fs(fs=AWG_framerate)
        # plt.figure()
        # plt.plot(f_measure,total_lorenz,'b')
        # plt.show()


class ADisplay(QtWidgets.QGroupBox):
    def __init__(self, parent):
        # super(ADisplay, self).__init__()
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        #
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        #
        self.pw = pg.MultiPlotWidget()
        self.plot_data = self.pw.addPlot(left='Amp', bottom='Time/s', title='Pump')
        #
        self.plot_btn = QtWidgets.QPushButton('Replot', self)
        self.plot_btn.clicked.connect(self.plot1)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        self.v_layout.addWidget(self.plot_btn)
        self.setLayout(self.v_layout)

    def plot1(self):
        self.plot_data.clear()
        x = self.parent.AWGInfo.ts
        y = self.parent.AWGInfo.ys
        r_symbol = np.random.choice(['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star'])
        r_color = np.random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
        self.plot_data.plot(x, y, pen=r_color)
        self.plot_data.showGrid(x=True, y=True)


class FcombDisplay(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent

        pg.setConfigOptions(leftButtonPan=False, antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.pw = pg.MultiPlotWidget()
        self.plot_data = self.pw.addPlot(left='Amp', bottom='Freq(Hz)', title='FreqCombs&LorenzSBSGain')

        #
        self.plot_btn = QtWidgets.QPushButton('Replot', self)
        self.plot_btn.clicked.connect(self.plot2)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        self.v_layout.addWidget(self.plot_btn)
        self.setLayout(self.v_layout)

    def plot2(self):
        self.plot_data.clear()
        z = self.parent.AWGInfo.Fre
        w = self.parent.AWGInfo.FFT_y
        gb = self.parent.AWGInfo.gb
        f_measure = self.parent.AWGInfo.f_measure
        r_symbol = np.random.choice(['o', 's', 't', 't1', 't2', 't3', 'd', '+', 'x', 'p', 'h', 'star'])
        r_color1 = np.random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
        r_color2 = np.random.choice(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'd', 'l', 's'])
        self.plot_data.plot(z, w, pen=r_color1)
        self.plot_data.plot(f_measure, gb, pen=r_color2)
        self.plot_data.showGrid(x=True, y=True)


class LightCtrl(QtWidgets.QGroupBox):
    '''
    激光器控制模块
    '''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle('LightWave Ctrl')
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setCheckable(True)
        self.setChecked(False)

        # 激光器控制面板
        LightWidget = QtWidgets.QGroupBox()
        LightWidget.setFlat(True)
        LightWidget.setAlignment(QtCore.Qt.AlignLeft)

        self.StartWave = QtWidgets.QLineEdit()
        self.StartWave.setPlaceholderText('Start_C Band')
        StartCalidator = QtGui.QDoubleValidator(self)
        StartCalidator.setRange(1530, 1630)
        StartCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        StartCalidator.setDecimals(4)
        self.StartWave.setValidator(StartCalidator)

        self.EndWave=QtWidgets.QLineEdit()
        self.EndWave.setPlaceholderText('End_C Band')
        EndCalidator=QtGui.QDoubleValidator(self)
        EndCalidator.setRange(1530,1630)
        EndCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        EndCalidator.setDecimals(4)
        self.EndWave.setValidator(EndCalidator)

        self.StartFreq=QtWidgets.QLineEdit()
        self.StartFreq.setPlaceholderText('Start_Freq_193414.489GHz')
        SFCalidator=QtGui.QDoubleValidator(self)
        SFCalidator.setRange(183921.753,195942.783) #GHz,精确到1MHz
        SFCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        SFCalidator.setDecimals(3)
        self.StartFreq.setValidator(SFCalidator)

        self.EndFreq=QtWidgets.QLineEdit()
        self.EndFreq.setPlaceholderText('End_Freq_addBW')
        EFCalidator=QtGui.QDoubleValidator(self)
        EFCalidator.setRange(183921.753,195942.783) #GHz,精确到1MHz
        EFCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        EFCalidator.setDecimals(3)
        self.EndFreq.setValidator(EFCalidator)

        self.BWFreq=QtWidgets.QLineEdit()
        self.BWFreq.setPlaceholderText('Freq_BW')
        BWCalidator=QtGui.QDoubleValidator(self)
        BWCalidator.setRange(0.3,8) #GHz
        BWCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        BWCalidator.setDecimals(3)
        self.BWFreq.setValidator(BWCalidator)


        self.Power = QtWidgets.QLineEdit()
        self.Power.setPlaceholderText('0~20dBm')
        PowerCalidator = QtGui.QDoubleValidator(self)
        PowerCalidator.setRange(0, 30)
        PowerCalidator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        # PowerCalidator.setDecimals(2)
        self.Power.setValidator(PowerCalidator)
        self.ActiveBtu = QtWidgets.QPushButton('Active')
        self.ActiveBtu.setStyleSheet(
            '''QPushButton{background:rgb(170,200,50);}QPushButton:hover{background:yellow;}''')
        self.ActiveBtu.setMaximumSize(200, 200)
        self.ActiveBtu.setCheckable(True)
        self.enterBtu = QtWidgets.QPushButton('Enter')
        self.enterBtu.setChecked(False)

        LightLayout = QtWidgets.QGridLayout()
        # LightLayout.setSpacing(0)
        LightLayout.addWidget(QtWidgets.QLabel('StartWave：'), 0, 0)
        LightLayout.addWidget(self.StartWave, 0, 1)
        LightLayout.addWidget(QtWidgets.QLabel('nm  '), 0, 2)
        LightLayout.addWidget(QtWidgets.QLabel('EndWave: '),0,3)
        LightLayout.addWidget(self.EndWave,0,4)
        LightLayout.addWidget(QtWidgets.QLabel('nm '),0,5)
        LightLayout.addWidget(QtWidgets.QLabel('StartFreq: '),1,0)
        LightLayout.addWidget(self.StartFreq,1,1)
        LightLayout.addWidget(QtWidgets.QLabel('GHz '),1,2)
        LightLayout.addWidget(QtWidgets.QLabel('EndFreq: '),1,3)
        LightLayout.addWidget(self.EndFreq,1,4)
        LightLayout.addWidget(QtWidgets.QLabel('GHz '),1,5)
        LightLayout.addWidget(QtWidgets.QLabel('Freq_BW: '),2,0)
        LightLayout.addWidget(self.BWFreq,2,1)
        LightLayout.addWidget(QtWidgets.QLabel('GHz '),2,2)
        LightLayout.addWidget(QtWidgets.QLabel('Power:'), 2, 3)
        LightLayout.addWidget(self.Power, 2, 4)
        LightLayout.addWidget(QtWidgets.QLabel('dBm  '), 2, 5)

        LightLayout.addWidget(self.enterBtu, 3, 0,1,2)
        LightLayout.addWidget(self.ActiveBtu, 3, 3,1,2)
        LightWidget.setLayout(LightLayout)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.addWidget(LightWidget)
        self.setLayout(mainLayout)

        self.clicked.connect(self.check)
        self.enterBtu.clicked.connect(self.setupLight)
        self.ActiveBtu.clicked.connect(self.activeF)

        self.StartWave.textChanged.connect(self.setupWaveFill)
        # self.StartFreq.textChanged.connect(self.setupFreqFill)
        self.EndWave.textChanged.connect(self.setupEF)
        # self.EndFreq.textChanged.connect(self.setupEW)
        self.BWFreq.textChanged.connect(self.setupAll)


    def check(self):
        ''' Enable/disable this groupbox '''

        if (self.parent.testModeAction.isChecked() or self.parent.LightHandle):
            self.setChecked(True)
            self.parent.LightCtrl.setCheckable(True)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No LightWave is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.LightCtrl.setChecked(False)

    def setupAll(self):
        C_speed = 299792458  # m/s
        BW=siEval(self.BWFreq.text())
        self.StartWave.setText(str(1550))
        self.EndWave.setText(str(round(C_speed/(BW+C_speed/1550),4)))

    def setupEF(self):
        C_speed=299792458  # m/s
        EndW=siEval(self.EndWave.text())
        SFreq=siEval(self.StartFreq.text())
        EFreq=siEval(self.EndFreq.text())
        self.EndFreq.setText(str(round(C_speed/EndW,3)))


    def setupWaveFill(self):
        C_speed=299792458  # m/s
        # wave='nm'
        # freq='GHz'
        SWave=siEval(self.StartWave.text())
        self.EndWave.setText(str(SWave))
        self.StartFreq.setText(str(round(C_speed/SWave,3)))
        self.EndFreq.setText(str(round(C_speed/SWave,3)))


    def setupLight(self):
        if (self.parent.testModeAction.isChecked() or self.parent.LightHandle):
            self.setChecked(True)
            self.parent.LightCtrl.setCheckable(True)
            if siEval(self.BWFreq.text())==0:
                self.parent.LightHandle.setupLight(power=float(self.Power.text()), wavelength=float(self.StartWave.text()))
            else:
                self.parent.LightHandle.sweepLight(waveStart=float(self.StartWave.text()),
                                                   waveEnd=float(self.EndWave.text()),
                                                   speed=200)

        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No LightWave is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.LightCtrl.setChecked(False)

    def activeF(self):
        api_light.LightSCPI.active(self)


class EDFACtrl(QtWidgets.QGroupBox):
    '''光信号EDFA控制栏'''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent
        self.setTitle('EDFA Ctrl')
        self.setAlignment(QtCore.Qt.AlignLeft)
        self.setCheckable(True)
        self.setChecked(False)

        EDFA1 = QtWidgets.QGroupBox()
        EDFA1.setTitle('EDFA1')
        EDFA1.setFlat(True)
        EDFA1.setAlignment(QtCore.Qt.AlignTop)
        EDFA1Layout = QtWidgets.QGridLayout()
        EDFA1Layout.setAlignment(QtCore.Qt.AlignTop)

        self.addressEDFA1 = QtWidgets.QLabel()

        self.setPower1 = QtWidgets.QWidget()
        self.setPower1Fill = QtWidgets.QLineEdit('5')
        self.setPower1UnitSel = QtWidgets.QComboBox()
        self.setPower1UnitSel.addItems(['dBm', 'mW'])
        self.setPower1UnitSel.setCurrentIndex(0)

        setPower1Layout = QtWidgets.QHBoxLayout()
        setPower1Layout.addWidget(QtWidgets.QLabel('SetPower'))
        setPower1Layout.addWidget(self.setPower1Fill)
        setPower1Layout.addWidget(self.setPower1UnitSel)
        self.setPower1.setLayout(setPower1Layout)

        self.P1slider = QtWidgets.QSlider()
        self.P1slider.setOrientation(QtCore.Qt.Horizontal)
        self.P1slider.setMaximum(20)
        self.P1slider.setMinimum(0)
        self.P1slider.setValue(5)
        # self.P1slider.setSingleStep(0.01)
        self.P1slider.setTickInterval(0.01)
        self.enterBtu1 = QtWidgets.QPushButton('Enter')
        self.activeBtu1 = QtWidgets.QPushButton('Active')
        self.activeBtu1.setCheckable(True)
        self.activeBtu1.setStyleSheet('''QPushButton{background:rgb(170,200,50);}QPushButton:hover{background:red;}''')

        EDFA1Layout.addWidget(QtWidgets.QLabel('Inst_COM:'), 0, 0)
        EDFA1Layout.addWidget(self.addressEDFA1, 0, 1, 1, 3)
        EDFA1Layout.addWidget(self.setPower1, 1, 0, 1, 3)
        EDFA1Layout.addWidget(self.P1slider, 3, 0, 1, 3)
        EDFA1Layout.addWidget(self.enterBtu1, 4, 0, 1, 1)
        EDFA1Layout.addWidget(self.activeBtu1, 4, 2, 1, 1)
        EDFA1.setLayout(EDFA1Layout)

        EDFA2 = QtWidgets.QGroupBox()
        EDFA2.setTitle('EDFA2')
        EDFA2.setFlat(True)
        EDFA2.setAlignment(QtCore.Qt.AlignTop)
        EDFA2Layout = QtWidgets.QGridLayout()
        EDFA2Layout.setAlignment(QtCore.Qt.AlignTop)

        self.addressEDFA2 = QtWidgets.QLabel()

        self.setPower2 = QtWidgets.QWidget()
        self.setPower2Fill = QtWidgets.QLineEdit('5')
        self.setPower2UnitSel = QtWidgets.QComboBox()
        self.setPower2UnitSel.addItems(['dBm', 'mW'])
        self.setPower2UnitSel.setCurrentIndex(0)

        setPower2Layout = QtWidgets.QHBoxLayout()
        setPower2Layout.addWidget(QtWidgets.QLabel('SetPower'))
        setPower2Layout.addWidget(self.setPower2Fill)
        setPower2Layout.addWidget(self.setPower2UnitSel)
        self.setPower2.setLayout(setPower2Layout)

        self.P2slider = QtWidgets.QSlider()
        self.P2slider.setOrientation(QtCore.Qt.Horizontal)
        self.P2slider.setMaximum(20)
        self.P2slider.setMinimum(0)
        self.P2slider.setValue(5)
        self.P2slider.setTickInterval(0.01)

        self.enterBtu2 = QtWidgets.QPushButton('Enter')
        self.activeBtu2 = QtWidgets.QPushButton('Active')
        self.activeBtu2.setCheckable(True)
        self.activeBtu2.setStyleSheet('''QPushButton{background:rgb(170,200,50);}QPushButton:hover{background:red;}''')

        EDFA2Layout.addWidget(QtWidgets.QLabel('Inst_COM:'), 0, 0)
        EDFA2Layout.addWidget(self.addressEDFA2, 0, 1, 1, 3)
        EDFA2Layout.addWidget(self.setPower2, 1, 0, 1, 3)
        EDFA2Layout.addWidget(self.P2slider, 3, 0, 1, 3)
        EDFA2Layout.addWidget(self.enterBtu2, 4, 0, 1, 1)
        EDFA2Layout.addWidget(self.activeBtu2, 4, 2, 1, 1)
        EDFA2.setLayout(EDFA2Layout)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignTop)
        mainLayout.addWidget(EDFA1)
        mainLayout.addWidget(EDFA2)
        self.setLayout(mainLayout)

        self.setPower1Fill.textChanged.connect(self.EDFAChangeFun)
        self.P1slider.valueChanged.connect(self.EDFAChangeFun)
        self.setPower2Fill.textChanged.connect(self.EDFAFillChangeFun)
        self.P2slider.valueChanged.connect(self.EDFAChangeFun)
        self.clicked.connect(self.check)
        self.enterBtu1.clicked.connect(self.enterFun1)
        self.enterBtu2.clicked.connect(self.enterFun2)
        self.activeBtu1.clicked.connect(self.activeFun1)
        self.activeBtu2.clicked.connect(self.activeFun2)

    def check(self):
        if (self.parent.testModeAction.isChecked() or self.parent.EDFA1Handle or self.parent.EDFA2Handle):
            self.setChecked(True)
            self.parent.EDFACtrl.setChecked(True)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No EDFA is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.EDFACtrl.setChecked(False)
        # self.parent.EDFACtrl.print_info()

    def EDFAChangeFun(self):

        self.setPower1Fill.setText(str(self.P1slider.value()))
        self.setPower2Fill.setText(str(self.P2slider.value()))
        EDFA1_status, EDFA1_Power = api_val.val_edfa1power(self.setPower1Fill.text(),
                                                           self.setPower1UnitSel.currentText())
        EDFA2_status, EDFA2_Power = api_val.val_edfa2power(self.setPower2Fill.text(),
                                                           self.setPower2UnitSel.currentText())
        self.parent.EDFAInfo.EDFA1power = EDFA1_Power
        self.parent.EDFAInfo.EDFA2power = EDFA2_Power

    def EDFAFillChangeFun(self):
        self.P1slider.setValue(int(self.setPower1Fill.text()))
        self.P2slider.setValue(int(self.setPower2Fill.text()))
        EDFA1_status, EDFA1_Power = api_val.val_edfa1power(self.setPower1Fill.text(),
                                                           self.setPower1UnitSel.currentText())
        EDFA2_status, EDFA2_Power = api_val.val_edfa2power(self.setPower2Fill.text(),
                                                           self.setPower2UnitSel.currentText())
        self.parent.EDFAInfo.EDFA1power = EDFA1_Power
        self.parent.EDFAInfo.EDFA2power = EDFA2_Power

    def enterFun1(self):
        api_edfa.EDFA1Set(EDFA1Handle=self.parent.EDFA1Handle, power=self.parent.EDFAInfo.EDFA1power)

    def activeFun1(self):
        if (self.parent.testModeAction.isChecked or self.parent.EDFA1Handle or self.parent.EDFA2Handle):
            self.setChecked(True)
            api_edfa.Active1(self.parent.EDFA1Handle)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No EDFA is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.EDFACtrl.setChecked(False)

    def enterFun2(self):
        api_edfa.EDFA2Set(EDFA2Handle=self.parent.EDFA2Handle, power=self.parent.EDFAInfo.EDFA2power)

    def activeFun2(self):
        if (self.parent.testModeAction.isChecked or self.parent.EDFA1Handle or self.parent.EDFA2Handle):
            self.setChecked(True)
            api_edfa.Active2(self.parent.EDFA2Handle)
        else:
            msg = Shared.MsgError(self, 'No Instrument!', 'No EDFA is connected!')
            msg.exec_()
            self.setChecked(False)
            self.parent.EDFACtrl.setChecked(False)


class Feedback(QtWidgets.QGroupBox):
    '''
    反馈算法
    1.带内平整度计算显示:目标带宽内，最大最小差值
    2.均方误差：与目标波形均方误差
    4.收敛方式：
        反馈次数
        均方误差
    '''

    def __init__(self, parent):
        QtWidgets.QGroupBox.__init__(self, parent)
        self.parent = parent

        self.setTitle('FB_Algorithm')
        self.setAlignment(QtCore.Qt.AlignLeft)

        # 反馈算法监控系数
        FBWidget = QtWidgets.QGroupBox()
        FBWidget.setFlat(True)
        FBWidget.setAlignment(QtCore.Qt.AlignLeft)

        # 需要显示收敛方式，均方误差实时显示（颜色标记升降）；反馈次数显示
        self.MSE = QtWidgets.QLineEdit()
        self.MSE.setPlaceholderText('MSEDisplay')
        self.FBnum = QtWidgets.QLineEdit()
        self.FBnum.setPlaceholderText('FB_Number')
        self.activeBtu = QtWidgets.QPushButton('Run')
        self.activeBtu.setStyleSheet('''QPushButton{background:rgb(170,200,50);}QPushButton:hover{background:red;}''')
        self.activeBtu.setMaximumSize(400, 400)
        self.activeBtu.setCheckable(True)
        self.backBtu = QtWidgets.QPushButton('Original')
        self.back = QtWidgets.QLineEdit()
        self.back.setPlaceholderText('NONE_PUMP')
        self.bfsBtu = QtWidgets.QPushButton('BFS')
        self.bfs = QtWidgets.QLineEdit()
        self.bfs.setPlaceholderText('Single_Comb')

        self.modFB = QtWidgets.QComboBox()
        self.modFB.addItems(api_val.FB_modList)
        self.modFBDispaly = QtWidgets.QLineEdit()

        FBLayout = QtWidgets.QGridLayout()
        FBLayout.setAlignment(QtCore.Qt.AlignLeft)
        FBLayout.addWidget(QtWidgets.QLabel('MSE:'), 0, 0, 1, 1)
        FBLayout.addWidget(self.MSE, 0, 1, 1, 1)
        FBLayout.addWidget(QtWidgets.QLabel('FB_Num:'), 1, 0, 1, 1)
        FBLayout.addWidget(self.FBnum, 1, 1, 1, 1)
        FBLayout.addWidget(self.backBtu, 0, 4, 1, 1)
        FBLayout.addWidget(self.back, 1, 4, 1, 1)
        FBLayout.addWidget(self.bfsBtu, 0, 5, 1, 1)
        FBLayout.addWidget(self.bfs, 1, 5, 1, 1)
        FBLayout.addWidget(self.activeBtu, 0, 6, 2, 1)
        FBLayout.addWidget(QtWidgets.QLabel('Mod_Switch:'), 0, 2)
        FBLayout.addWidget(self.modFB, 0, 3)
        FBLayout.addWidget(self.modFBDispaly, 1, 2, 1, 2)
        self.setLayout(FBLayout)

        self.modFB.currentIndexChanged[int].connect(self.switch_mod)
        self.backBtu.clicked.connect(self.getBack)
        self.activeBtu.clicked.connect(self.FB_Function)
        self.bfsBtu.clicked.connect(self.getBFS)

        self.BGS_freq = []
        self.BGS_amp = []
        self.bfs_value = 7.15e3

    def search_index(self, f_seq, f_measure):
        f_index = np.zeros(f_seq.size, dtype=int)
        f_resolution = (f_measure[-1] - f_measure[0]) / f_measure.size
        index_bef = 0
        for i in range(f_seq.size):
            for j in range(index_bef, f_measure.size):
                if abs(f_measure[j] - f_seq[i]) < .51 * f_resolution:
                    f_index[i] = j
                    index_bef = j
                    break
        return f_index

    def expected_gain(self, f_index, measure_brian, type_filter):
        # 3db带宽范围：fmax - fmin + FWHM（半峰全宽）
        # 2版：均值取fmax - fmin范围内，最后算泵浦对应位置
        len_seq = len(f_index)
        brian_measure_sam = np.array([measure_brian[i] for i in f_index])  # 最接近频梳频率的采样点增益

        if type_filter == 'Rectangle':
            # expected_gain_sam = np.ones(len_seq) * np.mean(brian_measure_sam)
            expected_gain_sam = np.ones(len_seq) * np.mean(measure_brian[f_index[0]:f_index[-1]])
        elif type_filter == 'Triangle':
            mb_min = max(np.min(measure_brian), 0)
            mb_max = np.max(measure_brian)
            if len_seq % 2 == 0:
                expected_seq1 = np.linspace(mb_min, mb_max, len_seq // 2)
                expected_seq2 = np.linspace(mb_max, mb_min, len_seq // 2)
            else:
                expected_seq1 = np.linspace(mb_min, mb_max, len_seq // 2 + 1)
                expected_seq2 = np.linspace(mb_max, mb_min, len_seq // 2 + 1)
                expected_seq2 = np.delete(expected_seq2, 0)
            expected_gain_sam = np.hstack((expected_seq1, expected_seq2))
        else:
            print('非法字符，请检查type_filter')
            expected_gain_sam = None
        return expected_gain_sam

    def lorenz(self, omega, omega_B, gamma_B):
        # 系数简化版
        # 输入：频率-omega；omega_B-布里渊增益最大点（BFS）；gamma_B-布里渊线宽
        # 输出：Lorenz型的增益因子g_B * g_0 * L_eff/A_eff
        gain_max = 10
        gamma_b22 = (gamma_B / 2) ** 2
        gain_lorenz = gain_max * gamma_b22 / ((omega - omega_B) ** 2 + gamma_b22)
        return gain_lorenz

    def corre_filter(self, measure_brian, gamma_B):
        # 功能：洛伦兹互相关去噪，修改线宽gamma_B影响分辨率
        x = np.linspace(-3 * 10 ** 3, 3 * 10 ** 3, 1000)  # 扫频范围，单位MHz
        ref_brian = self.lorenz(x, 0, gamma_B)
        corr = np.correlate(measure_brian, ref_brian, 'same')
        index_max = measure_brian.argmax()
        corr_refine = corr / corr.max() * np.mean(measure_brian[index_max - 5:index_max + 5])
        return corr_refine

    def bfs_correct(self, f_seq, f_measure, measure_brian, gamma_B=15):
        # 功能：洛伦兹互相关滤波取最值得到较准确整体BFS(单位：MHz)，精度取决于f_measure
        # 前提：观察窗口内有SBS增益且只有一个最大值)
        f_resolution = f_measure[1] - f_measure[0]
        amp_measure = self.corre_filter(measure_brian, gamma_B / f_resolution)
        cfp = np.median(f_seq)
        cf = f_measure[amp_measure.argmax()]
        bfs = cfp - cf
        return bfs

    def getBack(self):
        if (self.parent.testModeAction.isChecked()):
            self.back.clear()
            self.back.setPlaceholderText('Test!!! NONE')
        else:
            if (self.parent.PNAHandle):
                freq_BG_Signal, amp_BG_Signal = self.parent.PNAHandle.pna_acquire(measName=self.parent.PNAInfo.Scale)
                self.BGS_freq = freq_BG_Signal
                self.BGS_amp = amp_BG_Signal
                # self.BGS_amp=savgol_filter(amp_BG_Signal,51, 3, mode='nearest')
                self.back.clear()
                self.back.setPlaceholderText('Well Done!!!')
            else:
                self.back.clear()
                self.back.setPlaceholderText('Check PNA!')

    def getBFS(self):
        if (self.parent.testModeAction.isChecked()):
            self.back.clear()
            self.back.setPlaceholderText('Test!!! NONE')
        else:
            if (self.parent.PNAHandle):
                freq_single_comb, amp_single_comb = self.parent.PNAHandle.pna_acquire(
                    measName=self.parent.PNAInfo.Scale)
                freq_design_seq = self.parent.AWGInfo.f_list
                amp_single_comb = amp_single_comb - self.BGS_amp
                f_resolution = (freq_single_comb[1] - freq_single_comb[0]) / 1e6
                amp_single_comb = self.corre_filter(amp_single_comb, gamma_B=30 / f_resolution)
                self.bfs_value = self.bfs_correct(freq_design_seq / 1e6, freq_single_comb / 1e6, amp_single_comb,
                                                  30)  # 单位MHz(前提：观察窗口内有SBS增益且只有一个最大值)
                self.bfs.clear()
                self.bfs.setPlaceholderText(str(self.bfs_value / 1e3) + 'GHz')
            else:
                self.bfs.clear()
                self.bfs.setPlaceholderText('Check PNA!')

    def FB_Function(self, status):
        mod_index = self.modFB.currentIndex()

        mod_shape = self.parent.AWGInfo.mod_sel
        if status:
            if (self.parent.testModeAction.isChecked()):
                self.activeBtu.setCheckable(True)
            else:
                # 仿真反馈触发
                self.activeBtu.setCheckable(True)
                # mod_index=2,以反馈次数作为收敛量
                if mod_index == 2:
                    FB_num = int(self.modFBDispaly.text())
                    print(FB_num)
                    i = 1
                    for _ in range(FB_num):
                        freq_design_seq = self.parent.AWGInfo.f_list
                        amp_design_seq = self.parent.AWGInfo.amp_list
                        freq_measure, amp_measure = self.parent.PNAHandle.pna_acquire(
                            measName=self.parent.PNAInfo.Scale)
                        amp_measure = amp_measure - self.BGS_amp
                        f_index = self.search_index(freq_design_seq - self.bfs_value * 1e6, freq_measure)  # 搜索时减去BFS
                        f_resolution = (freq_measure[1] - freq_measure[0]) / 1e6  # 单位MHz
                        amp_measure = self.corre_filter(amp_measure, gamma_B=30 / f_resolution)  # 单位MHz；互相关平滑去噪

                        expected_amp_sam = self.expected_gain(f_index, amp_measure, mod_shape)
                        amp_measure_sam = np.array([amp_measure[i] for i in f_index])  # 最接近频梳频率的采样点增益
                        amp_design_seq_new = np.sqrt(
                            expected_amp_sam / amp_measure_sam) * amp_design_seq  # （3-7）-->边界收敛不一致
                        self.parent.AWGInfo.amp_list = amp_design_seq_new
                        print(amp_design_seq_new)

                        ys = SBS_DSP.synthesize1(amp_design_seq_new,
                                                 self.parent.AWGInfo.f_list,
                                                 self.parent.AWGInfo.ts,
                                                 self.parent.AWGInfo.phase_list)
                        self.parent.AWGInfo.ys = ys
                        wavefile = (ys - min(ys)) / (max(ys) - min(ys)) - 0.5
                        self.parent.AWGInfo.AWGwave = np.ones(len(wavefile)) * wavefile
                        self.parent.AWGHandle.clear_all_wfm()
                        wfmID = self.parent.AWGHandle.download_wfm(wfmData=self.parent.AWGInfo.AWGwave,
                                                                   ch=self.parent.AWGInfo.ChannelNum)
                        self.parent.AWGHandle.play(wfmID=wfmID, ch=self.parent.AWGInfo.ChannelNum)
                        self.FBnum.setText(str(i))
                        # 预留设备设置时间10ms
                        time.sleep(10)
                        i += 1
                    self.FBnum.setText(str(i - 1) + '  Done !!!')
                    # self.activeBtu.setCheckable(False)
                elif mod_index == 1:
                    # 范围在0-1
                    '''
                    1.PNA抽取数据与目标波形（自身均值作为等长度数列）
                    2.离线对50组数据进行GA或TS迭代
                    3.与最开始的目标波形做均方误差
                    4.直到收敛
                    '''
                    MES = float(self.modFBDispaly.text())
                    print(MES)
                    ant_Num=50
                    freq_measure=[]
                    amp_measure=[]
                    for a in range(ant_Num):
                        freq_measure[a], amp_measure[a]=self.parent.PNAHandle.pna_acquire()



                else:
                    pass

    def switch_mod(self):
        mod_index = self.modFB.currentIndex()

        if mod_index == 1:
            self.modFBDispaly.clear()
            self.modFBDispaly.setPlaceholderText('MSE')

        elif mod_index == 2:
            self.modFBDispaly.clear()
            self.modFBDispaly.setPlaceholderText('FB_Num.')


class VNAMonitor(QtWidgets.QGroupBox):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.parent = parent
        pg.setConfigOptions(leftButtonPan=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # self.pgPlot = pg.PlotWidget(title='PNA Monitor')
        self.pgPlot = pg.MultiPlotWidget()
        self.plot_data = self.pgPlot.addPlot(left='RF_Power(dB)', bottom='Freq(Hz)', title='RF_Spectrum')
        self.plot_btn = QtWidgets.QPushButton('Replot', self)
        self.plot_btn.clicked.connect(self.plot)

        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.addWidget(self.pgPlot)
        self.v_layout.addWidget(self.plot_btn)
        self.setLayout(self.v_layout)
        # self.data=np.empty()
        # # self.timer_start()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)
        self.timer.start(1500)

    def timer_start(self):
        if self.parent.PNAHandle:
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.plot)
            self.timer.start(1000)
        else:
            pass

    def plot(self):
        self.plot_data.clear()
        if self.parent.Display == 1:
            freq, result = self.parent.PNAHandle.pna_acquire(measName=self.parent.PNAInfo.Scale)
            self.plot_data.plot(freq, result, pen='b')
        else:
            pass

    def off(self):
        self.pgPlot.clearMouse()
