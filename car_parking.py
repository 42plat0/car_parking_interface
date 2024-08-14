import sys
import os
import random

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QKeyEvent, QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt, QRect

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))

class ParkingLot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_image = QPixmap(f"{WORKING_DIR}/images/parking_lot.png")
        self.car_image = QPixmap(f"{WORKING_DIR}/images/parked_car.png")
        self.open_management_window()

        self.setGeometry(200, 300, self.background_image.width(), self.background_image.height())


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)


    def open_management_window(self):
        management_window = ManagementWindow()
        management_window.show()



class ManagementWindow(QMainWindow):
     def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        central_w = QWidget()
        self.setCentralWidget(central_w)
        self.setGeometry(1000, 300, 200, 250)

        vbox = QVBoxLayout(central_w)


        self.park_in_label = QLabel(self)
        self.park_in_label.setText("Įvažiavimas:")

        self.leave_label = QLabel(self)
        self.leave_label.setText("Išvažiavimas:")

        self.car_nums_label_1 = QLabel(self)
        self.car_nums_label_2 = QLabel(self)
        self.car_nums_label_1.setText("Mašinos numeriai:")
        self.car_nums_label_2.setText("Mašinos numeriai:")

        self.plate_in = QLineEdit(self)
        self.plate_out = QLineEdit(self)
        self.park_btn = QPushButton("Priimti", self)
        self.leave_btn = QPushButton("Išleisti", self)

        self.plate_in.setPlaceholderText("XXX-000")
        self.plate_out.setPlaceholderText("XXX-000")

        vbox.addWidget(self.car_nums_label_1)
        vbox.addWidget(self.park_in_label)
        vbox.addWidget(self.plate_in)
        vbox.addWidget(self.park_btn)

        vbox.addWidget(self.car_nums_label_2)
        vbox.addWidget(self.leave_label)
        vbox.addWidget(self.plate_out)
        vbox.addWidget(self.leave_btn)


def main():
    app = QApplication(sys.argv)

    # window = ParkingLot()

    # window.show()
    
    management_window = ManagementWindow()
    management_window.show()

    sys.exit(app.exec_())


main()
