# -*- coding: utf-8 -*-
import sys
import serial.tools.list_ports
from PyQt5.QtWidgets import (QWidget, QDialog, QCheckBox, QScrollArea,  QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMainWindow, QSlider, QApplication, QDialogButtonBox, QLabel, QAction, qApp, QTextEdit, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtCore import Qt
from Workers import Reader, Speaker, Converter
from UIClasses import *
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.startUIMenu()
        self.menu = True
        self.loaded = False
        self.com_name = ''
        self.log_window = None
    def initUI(self):
        self.setWindowTitle('CRoWSLab - Custom ROuted Wireless Schematic Lab')
        self.setWindowIcon(QIcon('src//imgs//chip.png'))
        self.setMaximumWidth(1500)
        self.setMaximumHeight(1200)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(900)
        exitAct = QAction('&Quit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Quit the app')
        exitAct.triggered.connect(self.exit)
        loadAct = QAction('&Load', self)
        loadAct.setShortcut('Ctrl+L')
        loadAct.setStatusTip('Load lab')
        loadAct.triggered.connect(self.load)
        comAct = QAction('&Choose port', self)
        comAct.setShortcut('Ctrl+P')
        comAct.triggered.connect(self.choose_com)
        saveAct = QAction('&Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save current project')
        saveAct.triggered.connect(self.save)
        helpAct = QAction('&Help', self)
        helpAct.setShortcut('Ctrl+H')
        helpAct.setStatusTip('Show instructions')
        helpAct.triggered.connect(self.showReadMe)
        clearAct = QAction('&Clear', self)
        clearAct.setShortcut('Ctrl+D')
        clearAct.setStatusTip('Clear the circuit')
        clearAct.triggered.connect(self.clear)
        log_act = QAction('Show log', self)
        log_act.setShortcut('Ctrl+J')
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveAct)
        fileMenu.addAction(loadAct)
        fileMenu.addAction(exitAct)
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(clearAct)
        editMenu.addAction(comAct)
        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(helpAct)
        helpMenu.addAction(log_act)
    def startUIMenu(self):
        self.Menu = UIMenu(self)
        self.setCentralWidget(self.Menu)
        self.Menu.ToolsBTN.clicked.connect(self.startUIWorkspc)
        self.Menu.ExitBTN.clicked.connect(self.exit)
        self.show()
    def startUIWorkspc(self):
        self.Workspc = UIWorkspc(self)
        self.setCentralWidget(self.Workspc)
        self.Workspc.CPSBTN.clicked.connect(self.startUIMenu)
        self.Workspc.inputs.sendButton.clicked.connect(self.send)
        self.menu = False
        self.load()
        self.show()
    def clear(self):
        if self.loaded:
            image = QImage('//src//imgs//empty.png')
            self.Workspc.lab_row.pic.setImage(image)
            self.Workspc.lab_row.name.setText('Lab name: ')
            self.loaded = False
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Warning')
            msg.setText('No lab loaded yet')
            msg.setStyleSheet('background-color: #1f2827;')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
    def choose_com(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            msg = f'Found: {len(ports)} ports'
        for p in ports:
            msg = msg + '\n' + str(p.device)
        self.show_com_dialogue(msg)
    def show_com_dialogue(self, msg):
        input_dialog = InputDialog(msg)
        if input_dialog.exec():
            self.com_name = input_dialog.getInputs()
    def load(self):
        if not self.menu:
            path, _ = QFileDialog.getOpenFileName(self, 'Load a file', '', 'Netlist Files (*.txt)')        
            if path != '':
                reader = Reader()
                reader.old_read_cicuit(path)
                self.Workspc.lab_row.name.setText('Lab name: ' + reader.lab_name)
                image = QImage('out//Circuit.png')
                self.Workspc.lab_row.pic.setImage(image)
                self.loaded = True
    def showReadMe(self):
        msg = QMessageBox()
        msg.setWindowTitle('Help')
        msg.setText('\tLoad a lab from a netlist file (stored in src/ntlst/ by default).\n \
        Select a COM port you plan on using. \n \
        Connect terminals to the nodes of the circuit by writing terminals\' numbers next to the nodes\' numbers.\
        You can also connect measuring equipment by filling in the fields in the right column. \n\
        Select nodes to be power nodes (ground, +5V and Vref) if needed. \n\
        When all setting up is done press "SEND!" and your data will be sent to the MC you\'ve connected to the COM port. \n \
        Then our circuit board will connect your circuit for you.')
        msg.setStyleSheet("background-color: #1f2827;")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    def save(self):
        if not self.loaded:
            msg = QMessageBox()
            msg.setWindowTitle('Warning')
            msg.setText('No lab loaded yet')
            msg.setStyleSheet("background-color: #1f2827;")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        speaker = Speaker()
        speaker.clear_output()
        speaker.write_to_out('--CMT--')
        for i in range(0, 8):
            speaker.write_to_out(self.Workspc.inputs.table.edits[i].text())
        speaker.write_to_out('--MSR--')
        for i in range(0, 8):
            speaker.write_to_out(self.Workspc.inputs.table.mesure_edits[i].text())       
        speaker.write_to_out('--NOD--')
        if self.Workspc.inputs.table.is_gnd:
            speaker.write_to_out('1')
        if self.Workspc.inputs.table.is_5v:
            speaker.write_to_out('2')
        if self.Workspc.inputs.table.is_ref:
            speaker.write_to_out('3')
    def send(self):
        if self.loaded:
            self.save()
            s = Speaker()
            conv = Converter()
            conv.read('out//raw_output.txt')
            conv.convert()
            conv.clear('out//send_this.txt')
            conv.write('out//send_this.txt')
            if not conv.err:
                s.send_to_COM_port(self.com_name, 'out//send_this.txt')
                self.show_log()
            else:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('See log.txt roe details')
                msg.setStyleSheet("background-color: #1f2827;")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('No lab loaded yet')
            msg.setStyleSheet("background-color: #1f2827;")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
    def show_log(self):
        self.log_window = Log_Window()
        self.log_window.show()
    def exit(self):
        if self.loaded:
            self.clear()
        self.close()

def main():
    app = QApplication(sys.argv)
    sshFile="src//styles//styles.css"
    fh = open(sshFile,"r")
    my_style = fh.read()
    app.setStyleSheet(my_style)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()    
