from settings import RHYTMS

def rhytms_param_cnd(ui):
    ui.SpinBox1_1.setMinimum(RHYTMS['delta'][0]) # <-----------------------------------------------
    ui.SpinBox1_1.setMaximum(ui.SpinBox1_2.value() - 1)
    ui.SpinBox1_2.setMinimum(ui.SpinBox1_1.value() + 1)
    ui.SpinBox1_2.setMaximum(ui.SpinBox2_1.value())

    ui.SpinBox2_1.setMinimum(ui.SpinBox1_2.value())
    ui.SpinBox2_1.setMaximum(ui.SpinBox2_2.value() - 1)
    ui.SpinBox2_2.setMinimum(ui.SpinBox2_1.value() + 1)
    ui.SpinBox2_2.setMaximum(ui.SpinBox3_1.value())

    ui.SpinBox3_1.setMinimum(ui.SpinBox2_2.value())
    ui.SpinBox3_1.setMaximum(ui.SpinBox3_2.value() - 1)
    ui.SpinBox3_2.setMinimum(ui.SpinBox3_1.value() + 1)
    ui.SpinBox3_2.setMaximum(ui.SpinBox4_1.value())

    ui.SpinBox4_1.setMinimum(ui.SpinBox3_2.value())
    ui.SpinBox4_1.setMaximum(ui.SpinBox4_2.value() - 1)
    ui.SpinBox4_2.setMinimum(ui.SpinBox4_1.value() + 1)
    ui.SpinBox4_2.setMaximum(ui.SpinBox5_1.value())

    ui.SpinBox5_1.setMinimum(ui.SpinBox4_2.value())
    ui.SpinBox5_1.setMaximum(ui.SpinBox5_2.value() - 1)
    ui.SpinBox5_2.setMinimum(ui.SpinBox5_1.value() + 1)
    ui.SpinBox5_2.setMaximum(100)

    return {
        'delta': [
            ui.SpinBox1_1.value(),
            ui.SpinBox1_2.value(),
            ui.CheckBox1.isChecked()
        ],
        'theta': [
            ui.SpinBox2_1.value(),
            ui.SpinBox2_2.value(),
            ui.CheckBox2.isChecked()
        ],
        'alpha': [
            ui.SpinBox3_1.value(),
            ui.SpinBox3_2.value(),
            ui.CheckBox3.isChecked()
        ],
        'betha': [
            ui.SpinBox4_1.value(),
            ui.SpinBox4_2.value(),
            ui.CheckBox4.isChecked()
        ],
        'gamma': [
            ui.SpinBox5_1.value(),
            ui.SpinBox5_2.value(),
            ui.CheckBox5.isChecked()
        ],
    }


def reset(ui):
    ui.SpinBox1_1.setValue(RHYTMS['delta'][0])
    ui.SpinBox2_1.setValue(RHYTMS['theta'][0])
    ui.SpinBox3_1.setValue(RHYTMS['alpha'][0])
    ui.SpinBox4_1.setValue(RHYTMS['betha'][0])
    ui.SpinBox5_1.setValue(RHYTMS['gamma'][0])
    ui.SpinBox1_2.setValue(RHYTMS['delta'][1])
    ui.SpinBox2_2.setValue(RHYTMS['theta'][1])
    ui.SpinBox3_2.setValue(RHYTMS['alpha'][1])
    ui.SpinBox4_2.setValue(RHYTMS['betha'][1])
    ui.SpinBox5_2.setValue(RHYTMS['gamma'][1])


def open_session_norun(ui):
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(False)


def start(ui):
    ui.ButtonStart.setEnabled(False)
    ui.ButtonPause.setEnabled(True)
    ui.ButtonStop.setEnabled(True)
    ui.SliderChart.setEnabled(False)


def stop(ui):
    ui.ButtonStart.setEnabled(True)
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(False)
    ui.ButtonStop.setEnabled(False)


def pause(ui):
    ui.ButtonPause.setEnabled(False)
    ui.ButtonResume.setEnabled(True)
    ui.SliderChart.setEnabled(True)


def resume(ui):
    ui.ButtonPause.setEnabled(True)
    ui.ButtonResume.setEnabled(False)
    ui.SliderChart.setEnabled(False)