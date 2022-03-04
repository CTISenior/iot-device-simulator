#!/usr/bin/python

import sys
import json
import logging

from windows.AddWindow import AddWindow
from connectors.client import Client
import utils.helper as Helper


from PyQt5.QtWidgets import (
    QMainWindow, 
    QHeaderView, 
    QApplication, 
    QScrollArea, 
    QGridLayout, 
    QListWidget, 
    QMessageBox, 
    QListWidgetItem, 
    QGroupBox, 
    QScrollBar, 
    QTableWidget, 
    QPushButton, 
    QComboBox, 
    QMenu, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QCheckBox, 
    QAction, 
    QTabWidget, 
    QTableWidget, 
    QTableWidgetItem, 
    QSpinBox,
    QVBoxLayout
)
from PyQt5.QtCore import (
    Qt,
    QSize, 
    QEvent,
    pyqtSlot
)
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.left = 200
        self.top = 200
        self.width = 800
        self.height = 600

        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setFixedSize(QSize(self.width, self.height))
        
        self.setWindowTitle("IoT Device Simulator")
        self.device_instance_list = [] 

        self.initMenuBar()
        self.initUI()
        
        self.add_window = AddWindow(self)

        #logging.basicConfig(filename="logs/"+self.clientID, level=logging.DEBUG)
        
        logging.debug("Main Window")
        

    def initMenuBar(self):
        menubar = self.menuBar()

        fileMenuBar = menubar.addMenu('File')
        refresh_act = QAction('Refresh', self)
        close_act = QAction('Close', self)
        refresh_act.triggered.connect(self.display_devices)
        close_act.triggered.connect(self.closeEvent)
        fileMenuBar.addAction(refresh_act)
        fileMenuBar.addAction(close_act)

        devicesMenuBar = menubar.addMenu('Devices')
        newDevice_act = QAction('Add Device', self)
        command_act = QAction('Command Panel', self)
        newDevice_act.triggered.connect(self.addDeviceBtn)
        devicesMenuBar.addAction(newDevice_act)
        devicesMenuBar.addAction(command_act)
        
        
        helpMenuBar = menubar.addMenu('Help')
        thread_act = QAction('List Threads', self)
        helpMenuBar.addAction(thread_act)

    def initUI(self):
        main_layout = QGridLayout()

        self.deviceCount = QLabel()

        self.device_list_box()
        self.device_log_box()

        initbutton = QPushButton('Add device', self)
        initbutton.clicked.connect(self.addDeviceBtn)

        main_layout.addWidget(self.deviceListBox, 0, 0)
       
        main_layout.addWidget(self.deviceLogBox, 0, 1)
        main_layout.addWidget(self.deviceCount, 1,0)
        main_layout.addWidget(initbutton, 1,1)

        main_layout.setColumnStretch(0, 4)
        main_layout.setColumnStretch(1, 2)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(main_layout)


    def device_list_box(self):
        self.deviceListBox = QGroupBox("<Device List>")
        vbox = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(15)
        self.tableWidget.setHorizontalHeaderLabels(['Serial Number', 'Protocol', 'Keys', 'Values', 'Thread', 'Status'])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)
        self.tableWidget.viewport().installEventFilter(self)

        self.display_devices()
        
        vbox.addWidget(self.tableWidget)
        self.deviceListBox.setLayout(vbox)

       
    def device_log_box(self):
        self.deviceLogBox = QGroupBox("<Device Log>")
        vbox = QVBoxLayout()
        
        self.list_widget = QListWidget(self)
        self.setStyleSheet( """QListWidget{
                color: gray;
            }
            """
        )
        self.list_widget.setEnabled(False)
  
        self.show_logs()

        vbox.addWidget(self.list_widget)
        self.deviceLogBox.setLayout(vbox)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.text())
            self.show_device_logs("sn")

    def eventFilter(self, source, event):
        if(event.type() == QEvent.MouseButtonPress and
            event.buttons() == Qt.RightButton and
            source is self.tableWidget.viewport()):
                item = self.tableWidget.itemAt(event.pos())
                if item is not None:
                    self.menu = QMenu(self)
                    if(int(item.column()) == 0):
                        self.current_deviceSN = item.text()
                        self.startAction = self.menu.addAction('Start') 
                        self.deleteAction = self.menu.addAction('Delete')
                        self.stopAction = self.menu.addAction('Stop') 
                        
        return super(MainWindow, self).eventFilter(source, event)

    def generateMenu(self, pos):
        action = self.menu.exec_(self.tableWidget.mapToGlobal(pos))
        if(action != None):
            if(action == self.startAction):
                self.startDevice()
            elif(action == self.deleteAction):
                self.deleteDevice()
            elif(action == self.stopAction):
                self.stopDevice()
            self.display_devices()
        else:
            print("none")
    
    def startDevice(self): #before starting a device, json file can be modified to edit a device
        if(self.check_device_status() == False):
            deviceSN = self.current_deviceSN
            deviceObj = Helper.get_device_data(deviceSN)
            msg = Helper.create_message(deviceObj)
            
            new_client = Client()
            device_instance = new_client.run(deviceSN, deviceObj, msg, deviceObj['protocol'])
            if(device_instance != None):
                self.appendToList(device_instance)
            else:
                print(f'Protocol is not supported! | {deviceSN} {protocol}')
                #logging.error(f'Protocol is not supported! {deviceSN} {protocol}')

        else:
            self.showDialog('Device is already running!')

    def stopDevice(self):
        if(self.check_device_status() == False):
            self.showDialog('Device is already stopped!')
        else:
            
            deviceObj = Helper.get_device_instance(self.device_instance_list, self.current_deviceSN)
            deviceObj.stop_thread()
            self.removeFromList(deviceObj)
            print("stop device " + self.current_deviceSN)
            #logging.debug("stop device " + self.current_deviceSN)

    def deleteDevice(self):
        if(self.check_device_status() == False):
            Helper.delete_json(self.current_deviceSN)
            #logging.debug("delete device " + self.current_deviceSN)
            print("delete device " + self.current_deviceSN)
        else:
            self.showDialog('Device is running!') 

        
    def display_devices(self):
        print("display devices")
        self.deviceCount.setText('Number of running devices: ' + str(Helper.getRunningDeviceCount()))
        devices = Helper.read_json()['devices']
        self.tableWidget.setRowCount(len(devices))
        i=0
        for dev in devices:
            deviceSN = dev['serialNumber']
            self.tableWidget.setItem(i, 0, QTableWidgetItem(deviceSN))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(dev['protocol']))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(f'[{dev["keyValue"][0]["key"]} {dev["keyValue"][1]["key"]} {dev["keyValue"][2]["key"]}]'))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(f'[{dev["keyValue"][0]["initValue"]} {dev["keyValue"][1]["initValue"]} {dev["keyValue"][2]["initValue"]}]'))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(f'{dev["thread"]}({dev["interval"]})'))

            obj = Helper.get_device_instance(self.device_instance_list, deviceSN)
            if(obj == False):
                self.tableWidget.setItem(i, 5, QTableWidgetItem("Stopped"))
            else:
                if(obj.check_thread() != False):
                    self.tableWidget.setItem(i, 5, QTableWidgetItem("Running"))
                else:
                    self.tableWidget.setItem(i, 5, QTableWidgetItem("Stopped"))
            i+=1
        
    def show_logs(self):
        self.list_widget.addItem(QListWidgetItem("0"))

    def show_device_logs(self, sn):
        print("device logs for " + sn)

        #logging

    def showDialog(self, msg):
        button = QMessageBox.information(
            self,
            "Info!",
            msg
        )

    def check_device_status(self):
        return Helper.get_device_instance(self.device_instance_list, self.current_deviceSN)

    
    def addDeviceBtn(self):
        if self.add_window.isVisible():
            print("already visible")
        else:
            self.add_window = AddWindow(self)
            self.add_window.show()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', 
                        quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            sys.exit()
            event.accept()
        else:
            event.ignore()

    #@staticmethod
    def appendToList(self, obj):
        self.device_instance_list.append( obj )
        self.display_devices()
    def removeFromList(self, obj):
        self.device_instance_list.remove( obj )
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
