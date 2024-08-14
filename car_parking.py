import sys
import os
import random

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QKeyEvent, QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt, QRect

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


KEYS = {
    "up": 87,
    "down": 83,
    "right": 68,
    "left": 65
}


class ParkingLot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_image = QPixmap(f"{WORKING_DIR}/images/parking_lot.png")
        self.car_image = QPixmap(f"{WORKING_DIR}/images/parked_car.png")

        self.parking_lot_size = 5

        self.setGeometry(200, 300, self.background_image.width(),
                         self.background_image.height())

        self.speed = 20

        self.client_max_height = self.background_image.height() - self.car_image.height()
        self.client_max_width = self.background_image.width() - self.car_image.width()
        
        space_y = 0
        self.space_coordinates = [(x, space_y) for x in range(0, self.background_image.width(), self.car_image.width())]

        self.parking_lot = [{"id": i+1, "plate_num": None, "available": True, "space_x_y": self.space_coordinates[i]}
                for i in range(self.parking_lot_size)]

        self.car_x = 0
        self.car_y = 0

        self.cars = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

        try:
            for car in self.cars:
                painter.drawPixmap(car, self.car_image)
        except Exception:
            pass

    def place_car(self):

        for i in range(len(self.parking_lot)):
            rect = QRect(*self.parking_lot[i]["space_x_y"], self.car_image.width(),self.car_image.height())
            if self.parking_lot[i]["available"] is True:
                self.car_x, self.car_y = self.parking_lot[i]["space_x_y"]
                self.parking_lot[i]["available"] = False
                break
        else:
            print("Nebera vietos")
            return 
                
        self.cars.append(rect)
        
        print(self.cars)

        self.update()
        pass

class ManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parking_window = ParkingLot()

        self.setWindowTitle("Login")

        central_w = QWidget()
        self.setCentralWidget(central_w)
        self.setGeometry(1000, 300, 200, 250)

        vbox = QVBoxLayout(central_w)

        self.park_in_label = QLabel(self)
        self.park_in_label.setText("Įvažiavimas:")
        
        self.car_nums_label_1 = QLabel(self)
        self.car_nums_label_1.setText("Mašinos numeriai:")
        
        self.plate_in = QLineEdit(self)
        self.park_btn = QPushButton("Priimti", self)
        self.plate_in.setPlaceholderText("XXX-000")
        self.park_btn.clicked.connect(self.accept_car)

        self.leave_label = QLabel(self)
        self.leave_label.setText("Išvažiavimas:")
        
        self.car_nums_label_2 = QLabel(self)
        self.car_nums_label_2.setText("Mašinos numeriai:")
        
        self.plate_out = QLineEdit(self)
        self.leave_btn = QPushButton("Išleisti", self)
        self.plate_out.setPlaceholderText("XXX-000")

        vbox.addWidget(self.car_nums_label_1)
        vbox.addWidget(self.park_in_label)
        vbox.addWidget(self.plate_in)
        vbox.addWidget(self.park_btn)

        vbox.addWidget(self.car_nums_label_2)
        vbox.addWidget(self.leave_label)
        vbox.addWidget(self.plate_out)
        vbox.addWidget(self.leave_btn)

    def open_parking_window(self):
        self.parking_window.show()
    
    def accept_car(self):
        self.open_parking_window()
        self.parking_window.place_car()

def main():
    app = QApplication(sys.argv)

    management_window = ManagementWindow()
    management_window.show()

    sys.exit(app.exec_())


main()
