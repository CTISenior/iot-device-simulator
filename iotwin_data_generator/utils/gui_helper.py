import sys
from utils.setting import Setting

from PySide2.QtWidgets import (
   QComboBox,
   QLabel,
   QLineEdit,
   QCheckBox,
   QSpinBox,
   QHBoxLayout,
   QMessageBox
)


def show_message_box(self, msg, title, msgType='information'):
    msgBox = QMessageBox(self)

    if msgType == 'warning':
        msgBox.setIcon(QMessageBox.Warning)
        self.logger.warning( msg )
    elif msgType == 'question':
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    else: #Information
        msgBox.setIcon(QMessageBox.Information)
        self.logger.info( msg )

    
    msgBox.setText( msg )
    msgBox.setWindowTitle( title )
    msgBox.show()

    return msgBox

    # Define function for the buttons
    def msgButton(self, i):
        if i.text() == '&OK' :
            print("OK Button is pressed.")
        else:
            print("Cancel Button is pressed.")

def create_key_value_fields(rowNum):
    keyComboBox = QComboBox()
    keyComboBox.setEditable(True)
    
    valueSpinBox = QSpinBox()
    valueSpinBox.setValue(0)
    valueSpinBox.setRange(-10000, 10000)

    valueTypeBox = QComboBox()
    valueTypeBox.addItem('RN') #RandomNumber [-1, 0, 1]
    valueTypeBox.addItem('RFN') #RandomFloatNumber [-0.5, 0, 0.5]
    valueTypeBox.addItem('RFN-2') #RandomFloatNumber [-0.1, 0, 0.1]
    valueTypeBox.addItem('RFN-3') #RandomFloatNumber [-0.05, 0, 0.05]
    valueTypeBox.addItem('RFN-4') #RandomFloatNumber [-0.01, 0, 0.01]
    valueTypeBox.addItem('CN') #ConstantNumber

    checkBox = QCheckBox()

    if rowNum == 0 :
        checkBox.setEnabled(False)
        checkBox.setChecked(True)
    else:
        keyComboBox.setEnabled(False)
        valueSpinBox.setEnabled(False)
        valueTypeBox.setEnabled(False)

    keyValueBox = QHBoxLayout()
    keyValueBox.addWidget(keyComboBox)
    keyValueBox.addWidget(QLabel(f'Value-{str(rowNum+1)}:'))
    keyValueBox.addWidget(valueSpinBox)
    keyValueBox.addWidget(valueTypeBox)
    keyValueBox.addWidget(checkBox)

    set_default_keys(keyComboBox)

    return keyValueBox


def get_keyValueBox_widgets(keyValueBox):
    keyComboBox = keyValueBox.itemAt(0).widget()
    valueSpinBox = keyValueBox.itemAt(2).widget()
    valueTypeBox = keyValueBox.itemAt(3).widget()
    checkBox = keyValueBox.itemAt(4).widget()

    return keyComboBox, valueSpinBox, valueTypeBox, checkBox


def set_default_keys(keyComboBox):
    stg = Setting()
    default_keys = stg.getDefaultKeys()

    for key in default_keys:
        keyComboBox.addItem(key)