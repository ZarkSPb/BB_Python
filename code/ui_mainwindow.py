# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1058, 866)
        self.actionOpen_File = QAction(MainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionRhytm_window = QAction(MainWindow)
        self.actionRhytm_window.setObjectName(u"actionRhytm_window")
        self.actionRhytm_window.setCheckable(True)
        self.actionControl_panel = QAction(MainWindow)
        self.actionControl_panel.setObjectName(u"actionControl_panel")
        self.actionControl_panel.setCheckable(True)
        self.actionControl_panel.setChecked(True)
        self.actionStart = QAction(MainWindow)
        self.actionStart.setObjectName(u"actionStart")
        self.actionStart.setEnabled(False)
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        self.actionStop.setEnabled(False)
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionDisconnect = QAction(MainWindow)
        self.actionDisconnect.setObjectName(u"actionDisconnect")
        self.actionDisconnect.setEnabled(False)
        self.actionStart_impedance = QAction(MainWindow)
        self.actionStart_impedance.setObjectName(u"actionStart_impedance")
        self.actionStart_impedance.setEnabled(False)
        self.actionStop_impedance = QAction(MainWindow)
        self.actionStop_impedance.setObjectName(u"actionStop_impedance")
        self.actionStop_impedance.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 0, 2, 2)
        self.WidgetControl = QWidget(self.centralwidget)
        self.WidgetControl.setObjectName(u"WidgetControl")
        self.WidgetControl.setMinimumSize(QSize(0, 0))
        self.WidgetControl.setMaximumSize(QSize(180, 16777215))
        self.verticalLayout = QVBoxLayout(self.WidgetControl)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.WidgetControl)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.LayoutControl = QVBoxLayout(self.groupBox_3)
        self.LayoutControl.setSpacing(2)
        self.LayoutControl.setObjectName(u"LayoutControl")
        self.LayoutControl.setContentsMargins(2, 2, 2, 2)
        self.ButtonConnect = QPushButton(self.groupBox_3)
        self.ButtonConnect.setObjectName(u"ButtonConnect")

        self.LayoutControl.addWidget(self.ButtonConnect)

        self.ButtonStart = QPushButton(self.groupBox_3)
        self.ButtonStart.setObjectName(u"ButtonStart")
        self.ButtonStart.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonStart)

        self.ButtonStop = QPushButton(self.groupBox_3)
        self.ButtonStop.setObjectName(u"ButtonStop")
        self.ButtonStop.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonStop)

        self.ButtonDisconnect = QPushButton(self.groupBox_3)
        self.ButtonDisconnect.setObjectName(u"ButtonDisconnect")
        self.ButtonDisconnect.setEnabled(False)

        self.LayoutControl.addWidget(self.ButtonDisconnect)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.WidgetControl)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.LayoutImpedance = QVBoxLayout(self.groupBox_2)
        self.LayoutImpedance.setSpacing(2)
        self.LayoutImpedance.setObjectName(u"LayoutImpedance")
        self.LayoutImpedance.setContentsMargins(2, 2, 2, 2)
        self.ButtonImpedanceStart = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStart.setObjectName(u"ButtonImpedanceStart")
        self.ButtonImpedanceStart.setEnabled(False)

        self.LayoutImpedance.addWidget(self.ButtonImpedanceStart)

        self.ButtonImpedanceStop = QPushButton(self.groupBox_2)
        self.ButtonImpedanceStop.setObjectName(u"ButtonImpedanceStop")
        self.ButtonImpedanceStop.setEnabled(False)

        self.LayoutImpedance.addWidget(self.ButtonImpedanceStop)

        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.LayoutImpedance.addWidget(self.widget)

        self.widget_4 = QWidget(self.groupBox_2)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setSpacing(4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.LabelCh0 = QLabel(self.widget_5)
        self.LabelCh0.setObjectName(u"LabelCh0")

        self.verticalLayout_4.addWidget(self.LabelCh0)

        self.LabelCh1 = QLabel(self.widget_5)
        self.LabelCh1.setObjectName(u"LabelCh1")

        self.verticalLayout_4.addWidget(self.LabelCh1)

        self.LabelCh2 = QLabel(self.widget_5)
        self.LabelCh2.setObjectName(u"LabelCh2")

        self.verticalLayout_4.addWidget(self.LabelCh2)

        self.LabelCh3 = QLabel(self.widget_5)
        self.LabelCh3.setObjectName(u"LabelCh3")

        self.verticalLayout_4.addWidget(self.LabelCh3)


        self.horizontalLayout_4.addWidget(self.widget_5)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_5 = QVBoxLayout(self.widget_6)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.ProgressBarCh0 = QProgressBar(self.widget_6)
        self.ProgressBarCh0.setObjectName(u"ProgressBarCh0")
        self.ProgressBarCh0.setMaximum(500)
        self.ProgressBarCh0.setValue(0)
        self.ProgressBarCh0.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.ProgressBarCh0)

        self.ProgressBarCh1 = QProgressBar(self.widget_6)
        self.ProgressBarCh1.setObjectName(u"ProgressBarCh1")
        self.ProgressBarCh1.setMaximum(500)
        self.ProgressBarCh1.setValue(0)
        self.ProgressBarCh1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.ProgressBarCh1)

        self.ProgressBarCh2 = QProgressBar(self.widget_6)
        self.ProgressBarCh2.setObjectName(u"ProgressBarCh2")
        self.ProgressBarCh2.setMaximum(500)
        self.ProgressBarCh2.setValue(0)
        self.ProgressBarCh2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.ProgressBarCh2)

        self.ProgressBarCh3 = QProgressBar(self.widget_6)
        self.ProgressBarCh3.setObjectName(u"ProgressBarCh3")
        self.ProgressBarCh3.setMaximum(500)
        self.ProgressBarCh3.setValue(0)
        self.ProgressBarCh3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.ProgressBarCh3)


        self.horizontalLayout_4.addWidget(self.widget_6)


        self.LayoutImpedance.addWidget(self.widget_4)

        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.LayoutImpedance.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.groupBox_2)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.LayoutImpedance.addWidget(self.widget_3)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.WidgetControl)
        self.groupBox.setObjectName(u"groupBox")
        self.LayoutChartSettings = QVBoxLayout(self.groupBox)
        self.LayoutChartSettings.setSpacing(2)
        self.LayoutChartSettings.setObjectName(u"LayoutChartSettings")
        self.LayoutChartSettings.setContentsMargins(2, 2, 2, 2)
        self.LabelDuration = QLabel(self.groupBox)
        self.LabelDuration.setObjectName(u"LabelDuration")

        self.LayoutChartSettings.addWidget(self.LabelDuration)

        self.SliderDuration = QSlider(self.groupBox)
        self.SliderDuration.setObjectName(u"SliderDuration")
        self.SliderDuration.setEnabled(True)
        self.SliderDuration.setMinimum(1)
        self.SliderDuration.setMaximum(20)
        self.SliderDuration.setValue(20)
        self.SliderDuration.setSliderPosition(20)
        self.SliderDuration.setOrientation(Qt.Horizontal)
        self.SliderDuration.setTickPosition(QSlider.TicksAbove)
        self.SliderDuration.setTickInterval(1)

        self.LayoutChartSettings.addWidget(self.SliderDuration)

        self.LabelAmplitude = QLabel(self.groupBox)
        self.LabelAmplitude.setObjectName(u"LabelAmplitude")

        self.LayoutChartSettings.addWidget(self.LabelAmplitude)

        self.SliderAmplitude = QSlider(self.groupBox)
        self.SliderAmplitude.setObjectName(u"SliderAmplitude")
        self.SliderAmplitude.setMinimum(20)
        self.SliderAmplitude.setMaximum(200)
        self.SliderAmplitude.setSingleStep(5)
        self.SliderAmplitude.setPageStep(20)
        self.SliderAmplitude.setValue(20)
        self.SliderAmplitude.setOrientation(Qt.Horizontal)
        self.SliderAmplitude.setInvertedAppearance(False)
        self.SliderAmplitude.setInvertedControls(False)
        self.SliderAmplitude.setTickPosition(QSlider.TicksAbove)
        self.SliderAmplitude.setTickInterval(5)

        self.LayoutChartSettings.addWidget(self.SliderAmplitude)

        self.CheckBoxFilterChart = QCheckBox(self.groupBox)
        self.CheckBoxFilterChart.setObjectName(u"CheckBoxFilterChart")
        self.CheckBoxFilterChart.setChecked(True)

        self.LayoutChartSettings.addWidget(self.CheckBoxFilterChart)

        self.CheckBoxDetrendChart = QCheckBox(self.groupBox)
        self.CheckBoxDetrendChart.setObjectName(u"CheckBoxDetrendChart")
        self.CheckBoxDetrendChart.setEnabled(False)
        self.CheckBoxDetrendChart.setChecked(False)

        self.LayoutChartSettings.addWidget(self.CheckBoxDetrendChart)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.WidgetControl)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.LayoutPatient = QVBoxLayout(self.groupBox_4)
        self.LayoutPatient.setSpacing(2)
        self.LayoutPatient.setObjectName(u"LayoutPatient")
        self.LayoutPatient.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.LayoutPatient.addWidget(self.label)

        self.LinePatientFirstName = QLineEdit(self.groupBox_4)
        self.LinePatientFirstName.setObjectName(u"LinePatientFirstName")

        self.LayoutPatient.addWidget(self.LinePatientFirstName)

        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")

        self.LayoutPatient.addWidget(self.label_2)

        self.LinePatientLastName = QLineEdit(self.groupBox_4)
        self.LinePatientLastName.setObjectName(u"LinePatientLastName")

        self.LayoutPatient.addWidget(self.LinePatientLastName)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.WidgetControl)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.LayoutSave = QVBoxLayout(self.groupBox_5)
        self.LayoutSave.setSpacing(2)
        self.LayoutSave.setObjectName(u"LayoutSave")
        self.LayoutSave.setContentsMargins(2, 2, 2, 2)
        self.CheckBoxAutosave = QCheckBox(self.groupBox_5)
        self.CheckBoxAutosave.setObjectName(u"CheckBoxAutosave")
        self.CheckBoxAutosave.setChecked(True)

        self.LayoutSave.addWidget(self.CheckBoxAutosave)

        self.CheckBoxSaveFiltered = QCheckBox(self.groupBox_5)
        self.CheckBoxSaveFiltered.setObjectName(u"CheckBoxSaveFiltered")
        self.CheckBoxSaveFiltered.setChecked(True)

        self.LayoutSave.addWidget(self.CheckBoxSaveFiltered)

        self.ButtonSave = QPushButton(self.groupBox_5)
        self.ButtonSave.setObjectName(u"ButtonSave")
        self.ButtonSave.setEnabled(False)

        self.LayoutSave.addWidget(self.ButtonSave)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.verticalSpacer = QSpacerItem(20, 269, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.WidgetControl, 0, 0, 1, 1)

        self.SliderChart = QSlider(self.centralwidget)
        self.SliderChart.setObjectName(u"SliderChart")
        self.SliderChart.setEnabled(False)
        self.SliderChart.setMaximum(200)
        self.SliderChart.setSingleStep(1)
        self.SliderChart.setOrientation(Qt.Horizontal)
        self.SliderChart.setTickPosition(QSlider.NoTicks)

        self.gridLayout.addWidget(self.SliderChart, 1, 0, 1, 2)

        self.WidgetCharts = QWidget(self.centralwidget)
        self.WidgetCharts.setObjectName(u"WidgetCharts")
        self.LayoutCharts = QVBoxLayout(self.WidgetCharts)
        self.LayoutCharts.setSpacing(0)
        self.LayoutCharts.setObjectName(u"LayoutCharts")
        self.LayoutCharts.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.WidgetCharts, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1058, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuDevice = QMenu(self.menubar)
        self.menuDevice.setObjectName(u"menuDevice")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.SliderDuration, self.SliderAmplitude)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuDevice.menuAction())
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuView.addAction(self.actionControl_panel)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionRhytm_window)
        self.menuDevice.addAction(self.actionConnect)
        self.menuDevice.addAction(self.actionStart)
        self.menuDevice.addAction(self.actionStop)
        self.menuDevice.addAction(self.actionDisconnect)
        self.menuDevice.addSeparator()
        self.menuDevice.addAction(self.actionStart_impedance)
        self.menuDevice.addAction(self.actionStop_impedance)

        self.retranslateUi(MainWindow)
        self.SliderDuration.valueChanged.connect(MainWindow._chart_redraw_request)
        self.SliderAmplitude.valueChanged.connect(MainWindow._chart_redraw_request)
        self.ButtonConnect.clicked.connect(MainWindow._connect)
        self.ButtonStart.clicked.connect(MainWindow._start_capture)
        self.ButtonStop.clicked.connect(MainWindow._stop_capture)
        self.ButtonDisconnect.clicked.connect(MainWindow._disconnect)
        self.ButtonImpedanceStart.clicked.connect(MainWindow._start_impedance)
        self.ButtonImpedanceStop.clicked.connect(MainWindow._stop_impedance)
        self.ButtonSave.clicked.connect(MainWindow._save_data)
        self.CheckBoxFilterChart.stateChanged.connect(MainWindow._checkBoxFilteredChart)
        self.CheckBoxSaveFiltered.stateChanged.connect(MainWindow.update_ui)
        self.CheckBoxAutosave.stateChanged.connect(MainWindow.update_ui)
        self.SliderChart.valueChanged.connect(MainWindow._slider_value_cnd)
        self.LinePatientFirstName.textEdited.connect(MainWindow._firstName_edit)
        self.LinePatientLastName.textEdited.connect(MainWindow._lastName_edit)
        self.CheckBoxDetrendChart.stateChanged.connect(MainWindow._checkBoxDetrendChart)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionOpen_File.triggered.connect(MainWindow._open_file)
        self.actionControl_panel.changed.connect(MainWindow._control_panel)
        self.actionConnect.triggered.connect(MainWindow._connect)
        self.actionDisconnect.triggered.connect(MainWindow._disconnect)
        self.actionStart.triggered.connect(MainWindow._start_capture)
        self.actionStop.triggered.connect(MainWindow._stop_capture)
        self.actionStop_impedance.triggered.connect(MainWindow._stop_impedance)
        self.actionStart_impedance.triggered.connect(MainWindow._start_impedance)
        self.actionRhytm_window.changed.connect(MainWindow._rhytms_window)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BrainBit", None))
        self.actionOpen_File.setText(QCoreApplication.translate("MainWindow", u"Open File...", None))
        self.actionOpen_File.setIconText(QCoreApplication.translate("MainWindow", u"Open File", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_File.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+X", None))
#endif // QT_CONFIG(shortcut)
        self.actionRhytm_window.setText(QCoreApplication.translate("MainWindow", u"Rhytm window", None))
#if QT_CONFIG(shortcut)
        self.actionRhytm_window.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionControl_panel.setText(QCoreApplication.translate("MainWindow", u"Control panel", None))
#if QT_CONFIG(shortcut)
        self.actionControl_panel.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+P", None))
#endif // QT_CONFIG(shortcut)
        self.actionStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(shortcut)
        self.actionStart.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+2", None))
#endif // QT_CONFIG(shortcut)
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(shortcut)
        self.actionStop.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+3", None))
#endif // QT_CONFIG(shortcut)
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
#if QT_CONFIG(shortcut)
        self.actionConnect.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+1", None))
#endif // QT_CONFIG(shortcut)
        self.actionDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
#if QT_CONFIG(shortcut)
        self.actionDisconnect.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+4", None))
#endif // QT_CONFIG(shortcut)
        self.actionStart_impedance.setText(QCoreApplication.translate("MainWindow", u"Start impedance", None))
#if QT_CONFIG(shortcut)
        self.actionStart_impedance.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+5", None))
#endif // QT_CONFIG(shortcut)
        self.actionStop_impedance.setText(QCoreApplication.translate("MainWindow", u"Stop impedance", None))
#if QT_CONFIG(shortcut)
        self.actionStop_impedance.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+6", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"BrainBit control", None))
        self.ButtonConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.ButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.ButtonDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Impedance", None))
        self.ButtonImpedanceStart.setText(QCoreApplication.translate("MainWindow", u"Start impedance", None))
        self.ButtonImpedanceStop.setText(QCoreApplication.translate("MainWindow", u"Stop impedance", None))
        self.LabelCh0.setText(QCoreApplication.translate("MainWindow", u"T3", None))
        self.LabelCh1.setText(QCoreApplication.translate("MainWindow", u"T4", None))
        self.LabelCh2.setText(QCoreApplication.translate("MainWindow", u"O1", None))
        self.LabelCh3.setText(QCoreApplication.translate("MainWindow", u"O2", None))
        self.ProgressBarCh0.setFormat(QCoreApplication.translate("MainWindow", u"%v kOhm", None))
        self.ProgressBarCh1.setFormat(QCoreApplication.translate("MainWindow", u"%v kOhm", None))
        self.ProgressBarCh2.setFormat(QCoreApplication.translate("MainWindow", u"%v kOhm", None))
        self.ProgressBarCh3.setFormat(QCoreApplication.translate("MainWindow", u"%v kOhm", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Chart settings", None))
        self.LabelDuration.setText(QCoreApplication.translate("MainWindow", u"Duration (sec): 20", None))
        self.LabelAmplitude.setText(QCoreApplication.translate("MainWindow", u"Amplitude (uV): 20", None))
        self.CheckBoxFilterChart.setText(QCoreApplication.translate("MainWindow", u"Signal filtering", None))
        self.CheckBoxDetrendChart.setText(QCoreApplication.translate("MainWindow", u"Signal detrend", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Patient data", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"First name:", None))
        self.LinePatientFirstName.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Last name:", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Save settings", None))
        self.CheckBoxAutosave.setText(QCoreApplication.translate("MainWindow", u"Auto save", None))
        self.CheckBoxSaveFiltered.setText(QCoreApplication.translate("MainWindow", u"Save filtered data", None))
        self.ButtonSave.setText(QCoreApplication.translate("MainWindow", u"Save...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuDevice.setTitle(QCoreApplication.translate("MainWindow", u"Device", None))
    # retranslateUi

