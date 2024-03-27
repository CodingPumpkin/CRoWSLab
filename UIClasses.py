# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QDialog, QCheckBox, QScrollArea,  QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QMainWindow, QSlider, QApplication, QDialogButtonBox, QLabel, QAction, qApp, QTextEdit, QLineEdit, QGridLayout, QMessageBox)
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtCore import Qt
class Log_Window(QWidget):
    def __init__(self):
        super().__init__()
        lo = QVBoxLayout()
        self.text = QTextEdit()
        f = open('out//log.txt', 'r')
        self.text.setText(f.read())
        lo.addWidget(self.text)
        self.setLayout(lo)
class InputDialog(QDialog):
    def __init__(self, msg, parent=None):
        super().__init__(parent)
        self.field = QLineEdit(self, objectName='dEdit')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);
        text = QLabel(msg)
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addWidget(self.field)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    def getInputs(self):
        return self.field.text()
class UIMenu(QWidget):
    def __init__(self, parent=None):
        super(UIMenu, self).__init__(parent)
        self.ToolsBTN = QPushButton('Start', objectName='bigB')
        self.ExitBTN = QPushButton('Quit', objectName='bigB')
        layout = QHBoxLayout()
        layout.addWidget(self.ExitBTN)
        layout.addWidget(self.ToolsBTN)
        self.setLayout(layout)
class GoBackRow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout()
        label = QLabel()
        self.back_button = QPushButton('<-', objectName='smallB')
        self.back_button.setMaximumWidth(20)
        layout.addWidget(self.back_button)
        label.setText('go back')
        layout.addWidget(label)
        self.setLayout(layout)
class ImageViewer(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        area = QScrollArea()
        self.label = QLabel()
        area.setWidget(self.label)
        layout = QVBoxLayout()
        layout.addWidget(area)
        self.setLayout(layout)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label.adjustSize()
class Show_readme_png(QWidget):
    def __init__(self):
        super().__init__()
        lo = QVBoxLayout()
        path, _ = QFileDialog.getOpenFileName(self, 'Load an img', '', 'readme files (*.png)')        
        if path != '':
            img = ImageViewer()
            img.setImage(QImage(path))
            lo.addWidget(img)
        self.setLayout(lo)       
class LabRow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        main_layout = QVBoxLayout()
        self.pic = ImageViewer()
        self.pic.setFixedHeight(334)
        self.pic.setStyleSheet('background-color: transparent;')
        self.pic.setImage(QImage('//src//imgs//empty.png'))
        self.name = QLabel('Lab name: ')
        self.name.setFont(QFont('Arial', 16))
        self.name.setStyleSheet('color : white; height: 100px')
        components = QLabel('Available circuit elements: ')
        components.setFont(QFont('Arial', 16))
        components.setStyleSheet('color : white; height: 100px')
        main_layout.addWidget(self.name)
        main_layout.addWidget(components)
        main_layout.addWidget(self.pic)
        self.setLayout(main_layout)
class Grid(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.number_of_nodes = 8
        self.is_gnd = False
        self.is_5v = False
        self.is_ref = False
        layout = QGridLayout()
        node_head = QLabel('Specify numbers of the circuit elements\' terminals\nthat are to be connected to the nodes:')
        node_head.setStyleSheet('font-size: 24px')
        layout.addWidget(node_head, 0, 0, 1, 4)
        self.nodes = []
        self.nodes.append(QLabel('Node 0'))
        self.nodes.append(QLabel('Node 1'))
        self.nodes.append(QLabel('Node 2'))
        for i in range(3,self.number_of_nodes):
            self.nodes.append(QLabel('Node %d' %i))
        self.edits = []
        for i in range(0,self.number_of_nodes):
            self.edits.append(QLineEdit())
            self.edits[i].setText('')
        self.mesure_edits = []
        for i in range(0,self.number_of_nodes):
            self.mesure_edits.append(QLineEdit())
            self.mesure_edits[i].setText('')
        for i in range(0,self.number_of_nodes):
            layout.addWidget(self.nodes[i], i+1, 1)
            layout.addWidget(self.edits[i], i+1, 2)
            layout.addWidget(self.mesure_edits[i], i+1, 3)
        self.cbox_gnd = QCheckBox("GND",self)
        self.cbox_gnd.stateChanged.connect(self.clickBox_gnd)
        self.cbox_5V = QCheckBox("5V",self)
        self.cbox_5V.stateChanged.connect(self.clickBox_5v)
        self.cbox_ref = QCheckBox("REF",self)
        self.cbox_ref.stateChanged.connect(self.clickBox_ref)
        layout.addWidget(self.cbox_gnd, 1, 0)
        layout.addWidget(self.cbox_5V, 2, 0)
        layout.addWidget(self.cbox_ref, 3, 0)
        layout.setHorizontalSpacing(70)
        layout.setVerticalSpacing(10)
        self.setLayout(layout)
    def clickBox_gnd(self):
        self.is_gnd = not self.is_gnd
        if self.is_gnd:
            self.nodes[0].setStyleSheet('color: black')
        else:
            self.nodes[0].setStyleSheet('color: white')
    def clickBox_5v(self):
        self.is_5v = not self.is_5v
        if self.is_5v:
            self.nodes[1].setStyleSheet('color: red')
        else:
            self.nodes[1].setStyleSheet('color: white')
    def clickBox_ref(self):
        self.is_ref = not self.is_ref
        if self.is_ref:
            self.nodes[2].setStyleSheet('color: brown')
        else:
            self.nodes[2].setStyleSheet('color: white')
class UserInputs(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        layout = QHBoxLayout()
        main_area = QScrollArea()
        main_area.setStyleSheet('background-color: transparent;')
        main_area.setFixedHeight(300)
        self.table = Grid()
        main_area.setWidget(self.table)
        main_area.setWidgetResizable(True)
        layout.addWidget(main_area)
        self.sendButton = QPushButton('SEND!', objectName='bigB')
        layout.addWidget(self.sendButton)
        self.setLayout(layout)
class UIWorkspc(QWidget):
    def __init__(self, parent=None):
        super(UIWorkspc, self).__init__(parent)
        layout = QVBoxLayout()
        self.lab_row = LabRow()
        layout.addWidget(self.lab_row)
        self.inputs = UserInputs()
        layout.addWidget(self.inputs)
        self.SNDBTN = self.inputs.sendButton
        back_row = GoBackRow()
        self.CPSBTN = back_row.back_button
        layout.addWidget(back_row)
        self.setLayout(layout)
