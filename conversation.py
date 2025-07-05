from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QHBoxLayout, QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from styles import *
from circular_image_widget import CircularImageWidget


class Conversation:
    def __init__(self, parent):
        self.parent = parent

    def clear_chat(self):
        from main import save_chat_json

        self.clear_confirm = QMessageBox()
        self.clear_confirm.setStyleSheet(msg_box_style())
        self.clear_confirm.setWindowTitle("Clear Chat")
        self.clear_confirm.setText(f"Are you sure you want to clear the current chat ?")
        self.clear_confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.clear_confirm.setDefaultButton(QMessageBox.No)

        confirmation = self.clear_confirm.exec_()
        if confirmation == QMessageBox.Yes:
            save_chat_json({"messages": []})

            while self.parent.scroll_layout.count():
                item = self.parent.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            self.parent.scroll_area.repaint()

    def load_messages_on_start(self):
        from main import load_history

        chat_history = load_history()

        for message in chat_history:
            if message["role"] == "user":
                persona_name = message.get("persona_name", "User")
                persona_icon = message.get("persona_icon", "default_icon_path")
                self.add_user_message(message["content"], persona_name, persona_icon)
            elif message["role"] == "assistant":
                self.display_bot_message(message["content"])

    def send_message(self):
        user_text = self.parent.input_box.toPlainText().strip()

        if user_text:
            active_persona = self.get_active_persona()
            self.add_user_message(user_text, active_persona["name"], active_persona["icon_path"])
            self.parent.input_box.clear()

            QTimer.singleShot(100, lambda: self.generate_bot_reply(user_text))

            self.parent.scroll_area.verticalScrollBar().setValue(self.parent.scroll_area.verticalScrollBar().maximum())

    def get_active_persona(self):
        from main import load_json

        active_data = load_json("active.json")
        active_persona_key = active_data.get("active_persona", "")
        persona_data = load_json("persona.json").get("personas", {})
        return persona_data.get(active_persona_key, {})

    def add_user_message(self, text, persona_name, persona_icon):
        message_label = QLabel(text, self.parent.scroll_widget)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setStyleSheet(user_message_label_style())
        message_label.setMaximumWidth(780)

        user_info = QLabel(persona_name, self.parent.scroll_widget)
        user_info.setStyleSheet(above_message_info_style())
        picture = CircularImageWidget(persona_icon, 32)
        user_info_layout = QHBoxLayout()
        user_info_layout.addStretch()
        user_info_layout.addWidget(user_info)
        user_info_layout.addWidget(picture)
        user_info_layout.setSpacing(10)

        message_container = QWidget()
        message_container.setFixedWidth(800)
        message_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)

        message_layout = QVBoxLayout(message_container)
        message_layout.addLayout(user_info_layout)
        message_layout.addWidget(message_label)
        message_layout.setContentsMargins(5, 5, 5, 5)

        wrapper = QWidget()
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.addStretch()
        wrapper_layout.addWidget(message_container)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        self.parent.scroll_layout.addWidget(wrapper)

    def display_bot_message(self, text, user_text=None, is_regenerated=False):
        message_label = QLabel(text, self.parent.scroll_widget)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        message_label.setStyleSheet(bot_message_label_style())
        message_label.setMaximumWidth(780)

        bot_info = QLabel(self.parent.bot_data["bot_name"], self.parent.scroll_widget)
        bot_info.setStyleSheet(above_message_info_style())
        picture = CircularImageWidget(self.parent.bot_data["icon_path"], 32)

        bot_info_widget = QWidget()
        bot_info_layout = QHBoxLayout(bot_info_widget)
        bot_info_layout.setAlignment(Qt.AlignLeft)
        bot_info_layout.addWidget(picture)
        bot_info_layout.addWidget(bot_info)
        bot_info_layout.setSpacing(10)
        bot_info_layout.setContentsMargins(5, 5, 5, 5)

        message_container = QWidget()
        message_container.setFixedWidth(800)
        message_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)

        message_layout = QVBoxLayout(message_container)
        message_layout.addWidget(bot_info_widget)
        message_layout.addWidget(message_label)
        message_layout.setContentsMargins(5, 5, 5, 5)

        # Add Regenerate Button if user_text is provided (new messages)
        if user_text is not None:
            regenerate_button = QPushButton()
            regenerate_button.setIcon(QIcon("icons/regen.png"))
            regenerate_button.setStyleSheet(regenerate_button_style())
            regenerate_button.clicked.connect(lambda: self.regenerate_bot_reply(message_label, user_text))

            button_container = QWidget()
            button_layout = QHBoxLayout(button_container)
            button_layout.setAlignment(Qt.AlignRight)
            button_layout.addWidget(regenerate_button)
            button_layout.setContentsMargins(0, 0, 0, 0)
            message_layout.addWidget(button_container)

        wrapper = QWidget()
        wrapper_layout = QHBoxLayout(wrapper)
        wrapper_layout.addWidget(message_container)
        wrapper_layout.addStretch()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)

        self.parent.scroll_layout.addWidget(wrapper)
        self.parent.scroll_area.verticalScrollBar().setValue(self.parent.scroll_area.verticalScrollBar().maximum())

        return message_label

    def generate_bot_reply(self, user_text):
        from main import generate_reply, save_history, load_history

        active_persona = self.get_active_persona()
        chat_history = load_history()
        chat_history.append({
            "role": "user",
            "content": user_text,
            "persona_name": active_persona["name"],
            "persona_icon": active_persona["icon_path"]
        })
        save_history(chat_history[-30:])

        message_label = self.display_bot_message("", user_text=user_text)

        bot_reply = ""
        for chunk in generate_reply(user_text):
            bot_reply += chunk
            message_label.setText(bot_reply)
            QApplication.processEvents()

        chat_history.append({"role": "assistant", "content": bot_reply})
        save_history(chat_history[-30:])
        self.parent.scroll_area.verticalScrollBar().setValue(self.parent.scroll_area.verticalScrollBar().maximum())

        return chat_history

    def regenerate_bot_reply(self, message_label, user_text):
        from main import generate_reply, save_history, load_history

        chat_history = load_history()
        if chat_history and chat_history[-1]["role"] == "assistant":
            chat_history.pop()

        save_history(chat_history[-30:])

        bot_reply = ""
        for chunk in generate_reply(user_text):
            bot_reply += chunk
            message_label.setText(bot_reply)
            QApplication.processEvents()

        chat_history.append({"role": "assistant", "content": bot_reply})
        save_history(chat_history[-30:])



