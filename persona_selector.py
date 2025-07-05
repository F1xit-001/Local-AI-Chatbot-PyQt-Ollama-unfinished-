from json import JSONDecodeError
from PyQt5.QtWidgets import QWidget, QPushButton, QScrollArea, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import json
import os
from edit_persona import EditPersona
from styles import *


class PersonaSelector(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.personas_file = "config/persona.json"
        self.loaded_personas = self.load_persona()
        self.active_persona = self.load_active_persona()
        self.active_persona_id = self.active_persona

        self.init_ui()

    def init_ui(self):
        self.setGeometry(520, 150, 600, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet("background-color: #131316")

        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(0, 50, 600, 550)
        scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        scroll_area.setWidget(self.scroll_widget)

        self.create_persona = QPushButton(self)
        self.create_persona.setStyleSheet(create_persona_style())
        self.create_persona.setIcon(QIcon("Icons/add.png"))
        self.create_persona.setGeometry(558, 0, 40, 40)
        self.create_persona.clicked.connect(self.create_new_persona)

        self.title_close_btn = QPushButton(self)
        self.title_close_btn.setStyleSheet(title_close_btn_style())
        self.title_close_btn.setIcon(QIcon("Icons/back.png"))
        self.title_close_btn.setIconSize(QSize(16, 16))
        self.title_close_btn.setFixedSize(40, 40)
        self.title_close_btn.clicked.connect(self.close)

        self.persona_buttons()

    def load_persona(self):
        if os.path.exists(self.personas_file):
            with open(self.personas_file, "r") as f:
                return json.load(f).get("personas", {})
        return {}

    def load_active_persona(self):
        if os.path.exists("config/active.json"):
            with open("config/active.json", "r") as f:
                try:
                    data = json.load(f)
                    return data.get("active_persona", None)
                except JSONDecodeError:
                    return None
        return None

    def save_personas(self):
        with open(self.personas_file, "w") as f:
            json.dump({"personas": self.loaded_personas}, f, indent=4)

    def persona_buttons(self):
        for persona_id, data in self.loaded_personas.items():
            persona_btn = QPushButton(self.scroll_widget)
            persona_btn.setStyleSheet(persona_btn_style())
            if persona_id == self.active_persona_id:
                persona_btn.setText(data["name"] + "  (active)")
            else:
                persona_btn.setText(data["name"])
            persona_btn.setFixedHeight(60)
            if os.path.exists(data["icon_path"]):
                pixmap = QPixmap(data["icon_path"])
                icon_label = QLabel(persona_btn)
                icon_label.setPixmap(pixmap.scaled(75, 75, aspectRatioMode= 1, transformMode=Qt.SmoothTransformation))
                icon_label.setFixedWidth(60)

            persona_btn.clicked.connect(lambda checked, pid=persona_id: self.edit_persona(pid))
            self.scroll_layout.addWidget(persona_btn)

    def create_new_persona(self):
        self.edit_persona_window = EditPersona(self)
        self.edit_persona_window.parent
        self.edit_persona_window.show()
        self.close()

    def edit_persona(self, persona_id):
        self.edit_persona_window = EditPersona(self, persona_id, self.loaded_personas[persona_id])
        self.edit_persona_window.show()
        self.close()
