import sys
import os
import re

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QRect

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))


class Validation():

    @staticmethod
    def license_plates(plate):
        valid_plate_pattern = r"^[a-z]{3}-[0-9]{3}$"
        return bool(re.fullmatch(valid_plate_pattern, plate, re.IGNORECASE))


class ParkingLot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.background_image = QPixmap(
            f"{WORKING_DIR}/images/parking_lot.png")
        self.car_image = QPixmap(f"{WORKING_DIR}/images/parked_car.png")

        self.parking_lot_size = 5

        self.setGeometry(200, 300, self.background_image.width(),
                         self.background_image.height())

        space_y = 0
        self.space_coordinates = [(x, space_y) for x in range(
            0, self.background_image.width(), self.car_image.width())]

        self.parking_lot = [{"id": i+1, "plate_num": None, "available": True, "space_x_y": self.space_coordinates[i], "drawn_obj": None}
                            for i in range(self.parking_lot_size)]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_image)

        try:
            for space in self.parking_lot:
                if space["drawn_obj"] is not None:
                    painter.drawPixmap(space["drawn_obj"], self.car_image)
        except Exception:
            pass

    def place_car(self, plate_num):

        for car in self.parking_lot:
            if plate_num == car["plate_num"]:
                print("Masina siais numeriais jau pastatyta")
                return False

        for i in range(len(self.parking_lot)):
            rect = QRect(*self.parking_lot[i]["space_x_y"],
                         self.car_image.width(), self.car_image.height())
            if self.parking_lot[i]["available"] is True:
                self.parking_lot[i]["available"] = False
                self.parking_lot[i]["plate_num"] = plate_num
                self.parking_lot[i]["drawn_obj"] = rect
                break
        else:
            print("Nebera vietos")
            return False

        self.update()

        return True

    def release_car(self, plate_num):

        for i in range(len(self.parking_lot)):

            if self.parking_lot[i]["available"] is False and self.parking_lot[i]["plate_num"] == plate_num:
                self.parking_lot[i]["available"] = True
                self.parking_lot[i]["plate_num"] = None
                self.parking_lot[i]["drawn_obj"] = None
                break
        else:
            print("Masinos siais numeriais nera")
            return False

        self.update()

        return True


class ManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.parking_window = ParkingLot()

        self.setWindowTitle("Parking")

        central_w = QWidget()
        self.setCentralWidget(central_w)
        self.setGeometry(1000, 300, 200, 250)

        vbox = QVBoxLayout(central_w)

        self.park_car_label = QLabel(self)
        self.park_car_label.setText("Įvažiavimas:")

        self.car_nums_label_1 = QLabel(self)
        self.car_nums_label_1.setText("Mašinos numeriai:")

        self.park_car = QLineEdit(self)
        self.park_car.setPlaceholderText("XXX-000")

        self.park_car_btn = QPushButton("Priimti", self)
        self.park_car_btn.clicked.connect(self.add_car)

        self.leave_label = QLabel(self)
        self.leave_label.setText("Išvažiavimas:")

        self.car_nums_label_2 = QLabel(self)
        self.car_nums_label_2.setText("Mašinos numeriai:")

        self.remove_car = QLineEdit(self)
        self.remove_car.setPlaceholderText("XXX-000")

        self.release_car_btn = QPushButton("Išleisti", self)
        self.release_car_btn.clicked.connect(self.del_car)

        vbox.addWidget(self.car_nums_label_1)
        vbox.addWidget(self.park_car_label)
        vbox.addWidget(self.park_car)
        vbox.addWidget(self.park_car_btn)

        vbox.addWidget(self.car_nums_label_2)
        vbox.addWidget(self.leave_label)
        vbox.addWidget(self.remove_car)
        vbox.addWidget(self.release_car_btn)

        self.open_parking_window()

    def open_parking_window(self):
        self.parking_window.show()

    def add_car(self):
        if Validation.license_plates(self.park_car.text()):
            plate_num = self.park_car.text().upper()
            if not self.parking_window.place_car(plate_num=plate_num):
                mbox = QMessageBox(
                    self, text="Masina siais numeriais jau ileista")
                mbox.exec_()

            self.park_car.clear()
        else:
            mbox = QMessageBox(self, text="Neteisingi numeriai")
            mbox.exec_()

    def del_car(self):
        if Validation.license_plates(self.remove_car.text()):
            plate_num = self.remove_car.text().upper()
            if not self.parking_window.release_car(plate_num=plate_num):
                mbox = QMessageBox(self, text="Masinos siais numeriais nera")
                mbox.exec_()

            self.remove_car.clear()
        else:
            mbox = QMessageBox(self, text="Neteisingi numeriai")
            mbox.exec_()


def main():
    app = QApplication(sys.argv)

    management_window = ManagementWindow()
    management_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
