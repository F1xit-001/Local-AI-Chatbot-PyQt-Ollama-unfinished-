from PyQt5.QtWidgets import QWidget, QPushButton, QTextEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import json
from styles import *


class Memory(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
        self.display_memory()

    def init_ui(self):
        self.setGeometry(520, 150, 600, 320)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet("background-color: #131316")

        self.close_window = QPushButton(self)
        self.close_window.setStyleSheet(title_close_btn_style())
        self.close_window.setIcon(QIcon("Icons/back.png"))
        self.close_window.setIconSize(QSize(16, 16))
        self.close_window.setFixedSize(40, 40)
        self.close_window.clicked.connect(self.close)

        title = QLabel("Enter a really short summary of your chat", self)
        title.setStyleSheet(title_style())
        title.move(100, 12)

        note = QLabel("Note: A long summary can confuse the AI!", self)
        note.setStyleSheet(label_name_style())
        note.move(47, 80)

        self.char_description = QTextEdit(self)
        self.char_description.setStyleSheet(char_name_style())
        self.char_description.setGeometry(45, 120, 510, 180)
        self.char_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.char_description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.setStyleSheet(save_button_style())
        self.save_button.setGeometry(502, 5, 90, 40)
        self.save_button.clicked.connect(self.save_memory)

    def save_memory(self):
        memory = self.char_description.toPlainText()
        with open("config/memory.json", "w") as f:
            json.dump({"memory": memory}, f, indent=4)

    def display_memory(self):
        with open("config/memory.json", "r") as f:
            memory = json.load(f).get("memory")
            self.char_description.setPlainText(memory)

