#!/usr/bin/python

import sys
import json
from connectors.client import Client
from utils.setting import Setting
import utils.helper as Helper

#import main as MainWindow

from PyQt5 import (
   QtCore, 
   QtWidgets
)
from PyQt5.QtWidgets import (
   QMainWindow, 
   QFormLayout, 
   QComboBox, 
   QVBoxLayout, 
   QWidget, 
   QLabel, 
   QLineEdit, 
   QCheckBox, 
   QAction, 
   QTabWidget,
   QSpinBox,
   QHBoxLayout,
   QGridLayout
)
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize    


class AddWindow(QTabWidget):
   def __init__(self, MainWindow, parent = None):
      super(AddWindow, self).__init__(parent)
      self.left = 250
      self.top = 250
      self.width = 350
      self.height = 450
      self.setGeometry(self.left, self.top, self.width, self.height)

      self.MainWindow = MainWindow

      self.setFixedSize(QSize(self.width, self.height))
      self.setWindowTitle("IoT Device Simulator")
      
      layout = QVBoxLayout()
      self.setLayout(layout)

      tabs = QTabWidget()
      
      tabs.addTab(self.tab1_UI(), "Main")
      tabs.addTab(self.tab2_UI(), "Custom")
      
      self.button_box = QtWidgets.QDialogButtonBox(
         QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Close,
         QtCore.Qt.Horizontal,
         self
      )

      self.button_box.accepted.connect(self.start_device)
      self.button_box.rejected.connect(self.close)

      self.deviceStatus = QLabel()
      self.deviceStatus.setText('ready!')

      layout2 = QHBoxLayout()

      layout.addWidget(tabs)
      layout2.addWidget(self.deviceStatus)
      layout2.addWidget(self.button_box)
      

      layout.addLayout(layout2)

   def tab1_UI(self):
      self.tab1 = QWidget()

      tab1_boxLayout = QVBoxLayout()
      tab1_formLayout = QFormLayout()

      self.deviceSN = QLineEdit(self)
      tab1_formLayout.addRow("SN:", self.deviceSN)

      self.deviceName = QLineEdit(self)
      tab1_formLayout.addRow("Type/Name:", self.deviceName)
      self.deviceModel = QLineEdit(self)
      tab1_formLayout.addRow("Model:", self.deviceModel)
      self.deviceToken = QLineEdit(self)
      self.deviceToken.setEnabled(False)
      tab1_formLayout.addRow("Token:", self.deviceToken)
      
      self.deviceKey1 = QComboBox(self)
      self.deviceKey1.setEditable(True)
      nameLabel = QLabel(self)
      nameLabel.setText('Value:')
      self.deviceVal1 = QSpinBox(self)
      self.deviceVal1.setValue(0)
      self.deviceVal1.setRange(-10000, 10000)
      self.keyValueBox1 = QHBoxLayout()
      self.keyValueBox1.addWidget(self.deviceKey1)
      self.keyValueBox1.addWidget(nameLabel)
      self.keyValueBox1.addWidget(self.deviceVal1)
      tab1_formLayout.addRow(QLabel("Key:"), self.keyValueBox1)
      
      self.checkBox2 = QCheckBox("")
      self.checkBox2.stateChanged.connect(self.checkBox2_selection)
      self.deviceKey2 = QComboBox(self)

      self.deviceKey2.setEditable(True)
      self.deviceKey2.setEnabled(False)
      self.nameLabel2 = QLabel(self)
      self.nameLabel2.setText('Value-2:')
      self.nameLabel2.setEnabled(False)
      self.deviceVal2 = QSpinBox(self)
      self.deviceVal2.setValue(0)
      self.deviceVal2.setRange(-10000, 10000)
      self.deviceVal2.setEnabled(False)
      keyValueBox2 = QHBoxLayout()
      keyValueBox2.addWidget(self.deviceKey2)
      keyValueBox2.addWidget(self.nameLabel2)
      keyValueBox2.addWidget(self.deviceVal2)
      keyValueBox2.addWidget(self.checkBox2)
      self.keyLabel2 = QLabel(self)
      self.keyLabel2.setText('Key-2:')
      self.keyLabel2.setEnabled(False)
      tab1_formLayout.addRow(self.keyLabel2, keyValueBox2)
      
      self.checkBox3 = QCheckBox("")
      self.checkBox3.stateChanged.connect(self.checkBox3_selection)
      self.deviceKey3 = QComboBox(self)
      self.deviceKey3.setEditable(True)
      self.deviceKey3.setEnabled(False)
      self.nameLabel3 = QLabel(self)
      self.nameLabel3.setText('Value-3:')
      self.nameLabel3.setEnabled(False)
      self.deviceVal3 = QSpinBox(self)
      self.deviceVal3.setValue(0)
      self.deviceVal3.setRange(-10000, 10000)
      self.deviceVal3.setEnabled(False)
      keyValueBox3 = QHBoxLayout()
      keyValueBox3.addWidget(self.deviceKey3)
      keyValueBox3.addWidget(self.nameLabel3)
      keyValueBox3.addWidget(self.deviceVal3)
      keyValueBox3.addWidget(self.checkBox3)
      self.keyLabel3 = QLabel(self)
      self.keyLabel3.setText('Key-3:')
      self.keyLabel3.setEnabled(False)
      tab1_formLayout.addRow(self.keyLabel3, keyValueBox3)

      self.set_default_keys()

      self.interval = QSpinBox(self)
      self.interval.setRange(1, 100)
      tab1_formLayout.addRow(QLabel("Interval(sec):"), self.interval)

      self.protocol = QComboBox(self)
      self.protocol.addItem("MQTT")
      self.protocol.addItem("HTTP")
      tab1_formLayout.addRow(QLabel("Protocol:"), self.protocol)

      self.secBox = QCheckBox("")
      self.secBox.setEnabled(False)
      tab1_formLayout.addRow(QLabel("Secure:"), self.secBox)
      self.secBox.stateChanged.connect(self.click_secure)

      tab1_formLayout.setSpacing(10)
      
      tab1_boxLayout.addLayout(tab1_formLayout)
      self.tab1.setLayout(tab1_boxLayout)

      return self.tab1

   def set_default_keys(self):
      stg = Setting()
      default_keys = stg.getDefaultKeys()

      for key in default_keys:
         self.deviceKey1.addItem(key)
         self.deviceKey2.addItem(key)
         self.deviceKey3.addItem(key)

   def checkBox2_selection(self, state):
      if (state == QtCore.Qt.Checked):
         self.deviceKey2.setEnabled(state)
         self.deviceVal2.setEnabled(state)
         self.nameLabel2.setEnabled(state)
         self.keyLabel2.setEnabled(state)
      else:
         self.deviceKey2.setEnabled(state)
         self.deviceVal2.setEnabled(state)
         self.nameLabel2.setEnabled(state)
         self.keyLabel2.setEnabled(state)
      
   def checkBox3_selection(self, state):
      if (state == QtCore.Qt.Checked):
         self.deviceKey3.setEnabled(state)
         self.deviceVal3.setEnabled(state)
         self.nameLabel3.setEnabled(state)
         self.keyLabel3.setEnabled(state)
      else:
         self.deviceKey3.setEnabled(state)
         self.deviceVal3.setEnabled(state)
         self.nameLabel3.setEnabled(state)
         self.keyLabel3.setEnabled(state)
      
   def click_secure():
      print("secure!")

   def start_device(self):
         protocol = self.protocol.currentText().lower()
         deviceSN = self.deviceSN.text()
         interval = int(self.interval.value())
         key = self.deviceKey1.currentText().lower()
         key2 = ""
         key3 = ""
         val = int(self.deviceVal1.text())
         val2 = ""
         val3 = ""

         if(self.checkBox2.isChecked()):
            key2 = self.deviceKey2.currentText().lower()
            val2 = int(self.deviceVal2.text())
            print("checked2")

         if(self.checkBox3.isChecked()):
            key3 = self.deviceKey3.currentText().lower()
            val3 = int(self.deviceVal3.text())
            print("checked3")
         

         dataObj = {
            "serialNumber": deviceSN,
            "sensorType": self.deviceName.text(),
            "sensorModel": self.deviceModel.text(),
            "accessToken": "",
            "keyValue": [
               {
                  "key": key,
                  "initValue": val
               },
               {
                  "key": key2,
                  "initValue": val2
               },
               {
                  "key": key3,
                  "initValue": val3
               }
            ],
            "protocol": protocol,
            "security": {
               "secure": "",
               "credentials":"",
               "certificates":""
            },
            "thread": True,
            "interval": interval,
         }

         msg = Helper.create_message(dataObj)

         status = Helper.checkDeviceExist(deviceSN)
         if(status == False):
            new_client = Client()
            device_instance = new_client.run(deviceSN, dataObj, msg, protocol)
            if(device_instance != None):
               self.MainWindow.appendToList(device_instance)
            else:
               print(f'Protocol is not supported! | {deviceSN} {protocol}')
               #logging.error(f'Protocol is not supported! {deviceSN} {protocol}')
         else:
            print(f"DeviceSN `{deviceSN}` already exist! | `{protocol}`") #next -> log


########################################### tab 2 ###########################################
   def tab2_UI(self):
      self.tab2 = QWidget()
      tab2_boxLayout = QVBoxLayout()
      tab2_formLayout = QFormLayout()
      
      tab2_formLayout.setSpacing(10)
      
      tab2_boxLayout.addLayout(tab2_formLayout)
      self.tab2.setLayout(tab2_boxLayout)

      return self.tab2


###############################################################################

   def closeEvent(self, event):
      self.MainWindow.display_devices() ## refresh content
