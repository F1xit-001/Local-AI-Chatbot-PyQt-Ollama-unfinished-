from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QRect


class CircularImageWidget(QWidget):
    def __init__(self, image_path, diameter=64, parent=None):
        super().__init__(parent)
        self.diameter = diameter
        self.setFixedSize(diameter, diameter)
        self.setimagepath(image_path)

    def setimagepath(self, image_path):
        self.image_path = image_path.replace('\\', '/')
        self.pixmap = QPixmap(self.image_path)
        if self.pixmap.isNull():
            pass
        else:
            self.pixmap = self.pixmap.scaled(
                self.diameter, self.diameter,
                Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, self.diameter, self.diameter)
        painter.setClipPath(path)

        if not self.pixmap.isNull():
            target_rect = QRect(0, 0, self.diameter, self.diameter)
            source_rect = self.pixmap.rect().center()
            source_rect = QRect(source_rect.x() - self.diameter // 2, source_rect.y() - self.diameter // 2,
                                self.diameter, self.diameter)
            painter.drawPixmap(target_rect, self.pixmap, source_rect)
