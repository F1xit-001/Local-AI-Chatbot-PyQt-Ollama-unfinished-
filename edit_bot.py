from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QTextEdit, QFileDialog, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from circular_image_widget import CircularImageWidget
import json
from styles import *


class EditBot(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.setGeometry(520, 150, 600, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet("background-color: #131316")

        self.title_close_btn = QPushButton(self)
        self.title_close_btn.setStyleSheet(title_close_btn_style())
        self.title_close_btn.setIcon(QIcon("Icons/back.png"))
        self.title_close_btn.setIconSize(QSize(16, 16))
        self.title_close_btn.setFixedSize(40, 40)
        self.title_close_btn.clicked.connect(self.close)

        self.char_icon = CircularImageWidget(self.parent.bot_icon_path, 64, self)
        self.char_icon.move(45, 55)

        self.char_icon_edit = QPushButton(self)
        self.char_icon_edit.setStyleSheet("border-radius: 12px; background-color: #131316")
        self.char_icon_edit.setIcon(QIcon("Icons/writeedit.png"))
        self.char_icon_edit.setGeometry(86, 96, 25, 25)
        self.char_icon_edit.clicked.connect(self.choose_icon)

        label_name = QLabel("Character Name", self)
        label_name.setStyleSheet(label_name_style())
        label_name.move(47, 130)

        self.char_name = QLineEdit(self)
        self.char_name.setStyleSheet(char_name_style())
        self.char_name.setGeometry(45, 155, 510, 40)
        self.char_name.setMaxLength(20)
        self.char_name.setText(self.parent.bot_data['bot_name'])

        label_description = QLabel("Description, Definition", self)
        label_description.setStyleSheet(label_name_style())
        label_description.move(47, 205)

        self.char_description = QTextEdit(self)
        self.char_description.setStyleSheet(char_name_style())
        self.char_description.setGeometry(45, 230, 510, 340)
        self.char_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.char_description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.char_description.setPlainText(self.parent.bot_data['bot_personality'])

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.setStyleSheet(save_button_style())
        self.save_button.setGeometry(502, 5, 90, 40)
        self.save_button.clicked.connect(self.save_bot_settings)

    def choose_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_path:
            file_path = file_path.replace('\\', '/')
            self.parent.bot_icon_path = file_path
            self.char_icon.setimagepath(file_path)

    def save_bot_settings(self):
        data = {
            "icon_path": self.parent.bot_icon_path,
            "bot_name": self.char_name.text(),
            "bot_personality": self.char_description.toPlainText()
        }

        with open("config/bot.json", "w") as f:
            json.dump(data, f, indent=4)
        self.parent.bot_data = self.parent.load_bot_settings()
        self.parent.title_name.setText(self.parent.bot_data['bot_name'])
        self.parent.setWindowTitle("Chat With " + self.parent.bot_data['bot_name'])
        self.parent.title_icon.setimagepath(self.parent.bot_data['icon_path'])
        self.close()

