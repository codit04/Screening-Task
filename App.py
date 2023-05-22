import sys
import requests
import random
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QLabel)
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QMouseEvent, QPainter, QPen, QColor, QIcon


def randomimage():
    url = 'https://api.github.com/repos/hfg-gmuend/openmoji/contents/src/symbols/geometric?ref=master'

    response = requests.get(url)

    if response.status_code == 200:
        files = response.json()
        links = [file["download_url"] for file in files]
        random.shuffle(links)
        link = random.choice(links)
        return link

    else:
        return "Error!"


class ImageActions(QLabel):
    selected_images = []

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self.setMouseTracking(True)
        self.dragging = False
        self.drag_offset = QPoint()
        self.selected = False
        self.selection_color = Qt.GlobalColor.blue

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.selected:
            painter = QPainter(self)
            painter.setPen(QPen(self.selection_color, 2))
            painter.drawRect(self.rect())

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_offset = event.pos()
            if self.selected:
                for image in self.selected_images:
                    image.drag_offset = event.pos()

        if event.button() == Qt.MouseButton.RightButton:
            self.selected = not self.selected
            self.update()

            if self.selected:
                self.selected_images.append(self)
            else:
                self.selected_images.remove(self)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            if len(self.selected_images) == 0:
                new_pos = self.pos() + (event.pos() - self.drag_offset)
                self.move(new_pos)
            for image in self.selected_images:
                new_pos = image.pos() + (event.pos() - image.drag_offset)
                image.move(new_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def enterEvent(self, event):
        location = f"Location: ({self.x()}, {self.y()})"
        size = f"Size: {self.width()} x {self.height()}"
        color = self.get_avg_color(self.pixmap().toImage())
        self.setToolTip(f"{location}\n{size}\nColor: {color.name()}")

    def leaveEvent(self, event):
        self.setToolTip("")

    def get_avg_color(self, image):
        width = image.width()
        height = image.height()
        totalr = 0
        totalg = 0
        totalb = 0

        for x in range(width):
            for y in range(height):
                color = QColor.fromRgb(image.pixel(x, y))
                totalr += color.red()
                totalg += color.green()
                totalb += color.blue()

        pixels = width * height
        avgr = totalr // pixels
        avgg = totalg // pixels
        avgb = totalb // pixels

        return QColor(avgr, avgg, avgb)


class Button1(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Button 1", parent=parent)
        self.setGeometry(50, 50, 100, 50)
        self.setStyleSheet("background-color: green; color: black;font-size: 16px;")
        self.setFixedSize(100, 50)
        self.clicked.connect(self.showimage)
        self.counter = 0

    def showimage(self):
        self.counter += 1
        url = randomimage()
        response = requests.get(url)
        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            label = ImageActions(pixmap, self.parent())
            lwidth = pixmap.width()
            lheight = pixmap.height()

            pwidget = self.parent()
            pgeometry = pwidget.geometry()

            x = random.randint(0, pgeometry.width() - lwidth)
            y = random.randint(0, pgeometry.height() - lheight)

            label.setGeometry(QRect(x, y, lwidth, lheight))

            label.show()


class Button2(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Button 2", parent=parent)
        self.setGeometry(200, 50, 100, 50)
        self.setStyleSheet("background-color: blue; color: black;font-size: 16px;")
        self.setFixedSize(100, 50)
        self.clicked.connect(self.Button2Click)

    def Button2Click(self):
        if self.parent().button1.counter == 0:
            self.parent().showMessage("No images available to group", 5000)
        else:
            self.clicked.connect(self.groupImages)

    def groupImages(self):
        canvas = self.parent()
        selected_images = [child for child in canvas.children() if isinstance(child, ImageActions) and child.selected]
        if len(selected_images) == 0:
            canvas.showMessage("No images selected to group", 5000)
        else:
            for image in selected_images:
                image.selection_color = Qt.GlobalColor.blue
                image.update()
            canvas.showMessage("Images grouped", 5000)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.showMaximized()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button1 = Button1(parent=self)
        self.button2 = Button2(parent=self)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        layout.addWidget(self.button1)
        layout.addItem(spacer)
        layout.addWidget(self.button2)

        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.message_label.setVisible(False)

        layout.addWidget(self.message_label)

    def showMessage(self, message, duration):
        self.message_label.setText(message)
        self.message_label.setVisible(True)
        QTimer.singleShot(duration, self.hideMessage)

    def hideMessage(self):
        self.message_label.setVisible(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    canvas = Canvas()
    canvas.show()
    sys.exit(app.exec())
