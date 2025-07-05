from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QTextEdit, QFileDialog, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from circular_image_widget import CircularImageWidget
import json
import os
from styles import *


class EditPersona(QWidget):
    def __init__(self, parent, persona_id=None, persona_data=None):
        super().__init__()
        self.parent = parent
        self.persona_id = persona_id
        self.persona_data = persona_data or {"icon_path": "", "name": "", "description": ""}

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

        self.char_icon = CircularImageWidget(self.persona_data["icon_path"], 64, self)
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
        self.char_name.setText(self.persona_data["name"])

        label_description = QLabel("Description, Definition", self)
        label_description.setStyleSheet(label_name_style())
        label_description.move(47, 205)

        self.char_description = QTextEdit(self)
        self.char_description.setStyleSheet(char_name_style())
        self.char_description.setGeometry(45, 230, 510, 340)
        self.char_description.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.char_description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.char_description.setPlainText(self.persona_data["description"])

        self.save_button = QPushButton("Save Changes", self)
        self.save_button.setStyleSheet(save_button_style())
        self.save_button.setGeometry(502, 5, 90, 40)
        self.save_button.clicked.connect(self.save_persona)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.setStyleSheet(delete_button_style())
        self.delete_button.setGeometry(418, 5, 65, 40)
        self.delete_button.clicked.connect(self.delete_persona)

        self.set_active_btn = QPushButton("Set Active", self)
        self.set_active_btn.setStyleSheet(set_active_button_style())
        self.set_active_btn.setGeometry(394, 95, 160, 40)
        self.set_active_btn.clicked.connect(self.set_active_persona)


    def choose_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            project_dir = os.path.dirname(os.path.abspath(__file__))  # path to this .py file
            relative_path = os.path.relpath(file_path, start=project_dir)
            relative_path = relative_path.replace('\\', '/')
            print(f"Selected image path in EditPersona: {relative_path}")  # Debugg

            self.persona_data["icon_path"] = relative_path

            # Force reload
            self.char_icon.setimagepath(relative_path)
            self.char_icon.repaint()
            self.char_icon.update()
            self.update()

    def save_persona(self):
        if not self.char_name.text():
            return

        if not self.persona_id:
            self.persona_id = self.generate_unique_persona_id()

        self.parent.loaded_personas[self.persona_id] = {
            "icon_path": self.persona_data["icon_path"],
            "name": self.char_name.text(),
            "description": self.char_description.toPlainText()
        }
        self.parent.save_personas()
        self.close()

    def delete_persona(self):
        msg_box = QMessageBox(self)
        msg_box.setStyleSheet(msg_box_style())
        msg_box.setWindowTitle("Confirm Deletion")
        msg_box.setText(f"Are you sure you want to delete {self.persona_data['name']}?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        confirmation = msg_box.exec_()

        if confirmation == QMessageBox.Yes:
            if self.persona_id and self.persona_id in self.parent.loaded_personas:
                del self.parent.loaded_personas[self.persona_id]
                self.parent.save_personas()
            self.close()

    def generate_unique_persona_id(self):  # looks for missing numbers after key "persona" before creating another
        existing_keys = set(self.parent.loaded_personas.keys())  # basically fixes overwriting
        count = 1
        while f"persona{count}" in existing_keys:
            count += 1
        return f"persona{count}"

    def set_active_persona(self):
        with open("config/active.json", "w") as f:
            json.dump({"active_persona": self.persona_id}, f)

        self.parent.active_persona = self.persona_id
        self.close()
