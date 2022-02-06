import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('01.ui', self)

        self.api_server = "http://static-maps.yandex.ru/1.x/"

        self.lon_default = 47.247728
        self.lat_default = 56.139918
        self.delta_default = 1
        self.z_default = 12
        self.map_l_default = "map"

        self.lon = self.lon_default  # долгота
        self.lat = self.lat_default  # широта
        self.delta = self.delta_default
        self.z = self.z_default
        self.map_l = self.map_l_default

        self.label_zoom.setText(f"zoom=x{str(self.z)}")

        self.pixmap = QPixmap()

        self.getImage()
        self.initUI()

    def getImage(self):
        params = {
            "ll": ",".join([str(self.lon), str(self.lat)]),
            # "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": self.map_l,  # sat, skl,
            "z": self.z
        }
        self.label_zoom.setText(f"zoom=x{str(self.z)}")
        self.response = requests.get(self.api_server, params=params)
        # map_request = "http://static-maps.yandex.ru/1.x/?ll=37.530887,55.703118&spn=0.002,0.002&l=map"
        # self.response = requests.get(map_request)

        if not self.response:
            self.lineEdit_lon.setStyleSheet("QLineEdit { background-color: #fcb4b5;}")
            self.lineEdit_lat.setStyleSheet("QLineEdit { background-color: #fcb4b5;}")
            msg = QMessageBox(self)
            msg.setWindowTitle("Ошибка")
            msg.setText(f"Ошибка запроса!")
            msg.setIcon(QMessageBox.Warning)
            msg.setDetailedText(f"Http статус: {self.response.status_code} {self.response.reason}")
            msg.show()
            # print("Ошибка выполнения запроса:")
            # print("Http статус:", self.response.status_code, "(", self.response.reason, ")")
            # sys.exit(1)
        else:
            self.lineEdit_lon.setStyleSheet("QLineEdit { background-color: white;}")
            self.lineEdit_lat.setStyleSheet("QLineEdit { background-color: white;}")
            self.pixmap.loadFromData(self.response.content)
            ## Изображение
            self.picture_label.setPixmap(self.pixmap)

    def initUI(self):
        self.button_coords_search.clicked.connect(self.search_coords)
        self.button_coords_reset.clicked.connect(self.clear_coords)
        self.button_scale_up.clicked.connect(self.scale_up)
        self.button_scale_down.clicked.connect(self.scale_down)

        self.button_up.clicked.connect(lambda: self.change_center(0))
        self.button_right.clicked.connect(lambda: self.change_center(1))
        self.button_down.clicked.connect(lambda: self.change_center(2))
        self.button_left.clicked.connect(lambda: self.change_center(3))

        self.radioButton_map.clicked.connect(self.change_map)
        self.radioButton_sat.clicked.connect(self.change_map)
        self.radioButton_sat_skl.clicked.connect(self.change_map)

        self.pixmap.loadFromData(self.response.content)
        ## Изображение
        self.picture_label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.scale_up()
        elif event.key() == Qt.Key_PageDown:
            self.scale_down()
        if event.key() == Qt.Key_Up:
            self.change_center(0)
        elif event.key() == Qt.Key_Right:
            self.change_center(1)
        elif event.key() == Qt.Key_Down:
            self.change_center(2)
        elif event.key() == Qt.Key_Left:
            self.change_center(3)

    def change_center(self, _int):
        k = 500
        # lon - x, lat - y
        # print(k / (self.z * 0.8))
        if _int == 0:  # вверх
            self.lat += k / (self.z ** 4)
        #     x21 - 0.001
        #     x10 - 1
        #    y = 05 / x
        #    lat = k / xoom
        #    k = 0 .6
        elif _int == 1:  # вправо
            self.lon += k / (self.z ** 4)
        elif _int == 2:  # вниз
            self.lat -= k / (self.z ** 4)
        else:  # влево
            self.lon -= k / (self.z ** 4)
        self.getImage()

    def change_map(self):
        if self.radioButton_map.isChecked():
            self.map_l = "map"
        elif self.radioButton_sat.isChecked():
            self.map_l = "sat"
        else:
            self.map_l = "sat,skl"
        self.getImage()

    def search_coords(self):
        # print(self.lon, self.lat)
        self.lat = self.lineEdit_lat.text()
        self.lon = self.lineEdit_lon.text()
        self.getImage()

    def clear_coords(self):
        self.lineEdit_lat.setText("")
        self.lineEdit_lon.setText("")

    def scale_up(self):
        self.z += 1
        self.z = max(2, min(21, self.z))
        self.getImage()

    def scale_down(self):
        self.z -= 1
        self.z = max(2, min(21, self.z))
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())