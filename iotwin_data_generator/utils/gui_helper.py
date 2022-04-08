from utils.setting import Setting

from PySide2.QtWidgets import (
    QComboBox,
    QLabel,
    QCheckBox,
    QSpinBox,
    QHBoxLayout,
    QMessageBox
)


def show_message_box(self, msg, title, msgType='information'):
    msgbox = QMessageBox(self)

    if msgType == 'warning':
        msgbox.setIcon(QMessageBox.Warning)
        self.logger.warning(msg)
    elif msgType == 'question':
        msgbox.setIcon(QMessageBox.Question)
        msgbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else:  # Information
        msgbox.setIcon(QMessageBox.Information)
        self.logger.info(msg)

    msgbox.setText(msg)
    msgbox.setWindowTitle(title)
    msgbox.show()

    return msgbox

    # Define function for the buttons
    def msg_button(self, i):
        if i.text() == '&OK':
            print("OK Button is pressed.")
        else:
            print("Cancel Button is pressed.")


def create_key_value_fields(rowNum):
    key_combobox = QComboBox()
    key_combobox.setEditable(True)

    value_spinbox = QSpinBox()
    value_spinbox.setValue(0)
    value_spinbox.setRange(-10000, 10000)

    value_typebox = QComboBox()
    value_typebox.addItem('RN')  # RandomNumber [-1, 0, 1]
    value_typebox.addItem('RFN')  # RandomFloatNumber [-0.5, 0, 0.5]
    value_typebox.addItem('RFN-2')  # RandomFloatNumber [-0.1, 0, 0.1]
    value_typebox.addItem('RFN-3')  # RandomFloatNumber [-0.05, 0, 0.05]
    value_typebox.addItem('RFN-4')  # RandomFloatNumber [-0.01, 0, 0.01]
    value_typebox.addItem('CN')  # ConstantNumber

    checkbox = QCheckBox()

    if rowNum == 0:
        checkbox.setEnabled(False)
        checkbox.setChecked(True)
    else:
        key_combobox.setEnabled(False)
        value_spinbox.setEnabled(False)
        value_typebox.setEnabled(False)

    keyvaluebox = QHBoxLayout()
    keyvaluebox.addWidget(key_combobox)
    keyvaluebox.addWidget(QLabel(f'Value-{str(rowNum+1)}:'))
    keyvaluebox.addWidget(value_spinbox)
    keyvaluebox.addWidget(value_typebox)
    keyvaluebox.addWidget(checkbox)

    set_default_keys(key_combobox)

    return keyvaluebox


def get_keyvaluebox_widgets(keyvaluebox):
    key_combobox = keyvaluebox.itemAt(0).widget()
    value_spinbox = keyvaluebox.itemAt(2).widget()
    value_typebox = keyvaluebox.itemAt(3).widget()
    checkbox = keyvaluebox.itemAt(4).widget()

    return key_combobox, value_spinbox, value_typebox, checkbox


def set_default_keys(key_combobox):
    stg = Setting()
    default_keys = stg.get_default_keys()

    for key in default_keys:
        key_combobox.addItem(key)
