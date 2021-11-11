# from ui_mainwindow import Ui_MainWindow as ui


def connect_0(ui):
    ui.ButtonConnect.setEnabled(False)

    ui.actionConnect.setEnabled(False)
    ui.actionOpen_File.setEnabled(False)
    ui.LinePatientFirstName.setEnabled(True)
    ui.LinePatientLastName.setEnabled(True)
    ui.LinePatientFirstName.setText('')
    ui.LinePatientLastName.setText('')
    ui.CheckBoxFilterChart.setChecked(True)
    ui.CheckBoxAutosave.setEnabled(True)
    ui.CheckBoxSaveFiltered.setEnabled(True)
    ui.CheckBoxFilterChart.setEnabled(True)


def connect_1(ui):
    ui.ButtonConnect.setEnabled(True)
    ui.actionConnect.setEnabled(True)


def connect_2(ui):
    ui.ButtonStart.setEnabled(True)
    ui.ButtonDisconnect.setEnabled(True)
    ui.ButtonImpedanceStart.setEnabled(True)
    ui.ButtonSave.setEnabled(False)

    ui.actionStart.setEnabled(True)
    ui.actionDisconnect.setEnabled(True)
    ui.actionStart_impedance.setEnabled(True)
    ui.actionSave_File.setEnabled(False)


def start(ui):
    ui.ButtonStart.setEnabled(False)
    ui.ButtonDisconnect.setEnabled(False)
    ui.ButtonStop.setEnabled(True)
    ui.ButtonImpedanceStart.setEnabled(False)
    ui.ButtonSave.setEnabled(False)

    ui.actionStart.setEnabled(False)
    ui.actionDisconnect.setEnabled(False)
    ui.actionStop.setEnabled(True)
    ui.actionStart_impedance.setEnabled(False)
    ui.actionSave_File.setEnabled(False)
    
    ui.CheckBoxAutosave.setEnabled(False)
    ui.CheckBoxSaveFiltered.setEnabled(False)
    ui.LinePatientFirstName.setEnabled(False)
    ui.LinePatientLastName.setEnabled(False)
    ui.SliderChart.setEnabled(False)


def stop(ui):
    ui.ButtonStart.setEnabled(True)
    ui.ButtonDisconnect.setEnabled(True)
    ui.ButtonStop.setEnabled(False)
    ui.ButtonImpedanceStart.setEnabled(True)
    ui.ButtonSave.setEnabled(True)

    ui.actionStart.setEnabled(True)
    ui.actionDisconnect.setEnabled(True)
    ui.actionStop.setEnabled(False)
    ui.actionStart_impedance.setEnabled(True)
    ui.actionSave_File.setEnabled(True)


    ui.CheckBoxAutosave.setEnabled(True)
    ui.CheckBoxSaveFiltered.setEnabled(True)
    ui.LinePatientFirstName.setEnabled(True)
    ui.LinePatientLastName.setEnabled(True)
    ui.SliderChart.setEnabled(True)


def disconnect(ui):
    ui.ButtonDisconnect.setEnabled(False)
    ui.ButtonConnect.setEnabled(True)
    ui.ButtonImpedanceStart.setEnabled(False)
    ui.ButtonStart.setEnabled(False)

    ui.actionDisconnect.setEnabled(False)
    ui.actionConnect.setEnabled(True)
    ui.actionStart_impedance.setEnabled(False)
    ui.actionStart.setEnabled(False)
    ui.actionOpen_File.setEnabled(True)


def start_impedance(ui):
    ui.ButtonImpedanceStart.setEnabled(False)
    ui.ButtonImpedanceStop.setEnabled(True)
    ui.ButtonStart.setEnabled(False)
    ui.ButtonDisconnect.setEnabled(False)
    ui.ButtonSave.setEnabled(False)

    ui.actionControl_panel.setChecked(True)
    ui.actionStart_impedance.setEnabled(False)
    ui.actionStop_impedance.setEnabled(True)
    ui.actionStart.setEnabled(False)
    ui.actionDisconnect.setEnabled(False)
    ui.actionSave_File.setEnabled(False)


def stop_impedance(ui):
    ui.ButtonImpedanceStart.setEnabled(True)
    ui.ButtonImpedanceStop.setEnabled(False)
    ui.ButtonStart.setEnabled(True)
    ui.ButtonDisconnect.setEnabled(True)

    ui.actionStart_impedance.setEnabled(True)
    ui.actionStop_impedance.setEnabled(False)
    ui.actionStart.setEnabled(True)
    ui.actionDisconnect.setEnabled(True)


def open_file(ui):
    ui.CheckBoxFilterChart.setChecked(True)
    ui.LinePatientFirstName.setEnabled(False)
    ui.LinePatientLastName.setEnabled(False)
    ui.CheckBoxAutosave.setEnabled(False)
    ui.CheckBoxSaveFiltered.setEnabled(False)
    ui.SliderChart.setEnabled(True)