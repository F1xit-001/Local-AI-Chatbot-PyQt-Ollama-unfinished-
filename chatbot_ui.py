
from PyQt5.QtWidgets import QWidget, QTextEdit, QPushButton, QLabel, QSizePolicy, QVBoxLayout, QScrollArea, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QEvent
import json
from edit_bot import EditBot
from persona_selector import PersonaSelector
from memory import Memory
from styles import *
from circular_image_widget import CircularImageWidget
from conversation import Conversation


class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.conversation = Conversation(self)
        self.chat_display = QLabel()
        self.input_container = QWidget()
        self.input_box = QTextEdit()
        self.send_button = QPushButton()
        self.side_bar = QWidget()
        self.line_widget = QWidget()
        self.edit_button = QPushButton()
        self.persona_button = QPushButton()
        self.memory_button = QPushButton()
        self.clear_chat = QPushButton()
        self.import_model = QPushButton()
        self.expand_icons = []  # Store references to prevent garbage collection

        self.bot_data = self.load_bot_settings()
        self.bot_icon_path = self.bot_data['icon_path']
        self.init_ui()
        self.conversation.load_messages_on_start()

    def init_ui(self):
        self.setWindowTitle("Chat With " + self.bot_data['bot_name'])
        self.setWindowIcon(QIcon(self.bot_icon_path))
        self.resize(1916, 1080)

        # Chat Display
        self.chat_display.setStyleSheet("background-color: #18181b; color: #ececec; padding: 5px; border-radius: 5px;")
        self.chat_display.setFixedHeight(1060)
        self.chat_display.setFixedWidth(1600)
        self.chat_display.move(0, 0)

        self.scroll_area = QScrollArea(self.chat_display)
        self.scroll_area.setGeometry(302, 15, 1000, 852)  # Positioning inside chat_display
        self.scroll_area.setStyleSheet("background-color: #18181b; border: none;")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Widget to Hold Messages
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll_area.setWidget(self.scroll_widget)

        # input box container
        self.input_container.setGeometry(0, 885, 1600, 195)
        self.input_container.setStyleSheet("background-color: #18181b; border-top: 2px solid rgba(47, 2, 119, 0.5);")

        # Input box and Send Button
        self.input_box.setStyleSheet(input_box_style())
        self.input_box.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.input_box.setMaximumHeight(150)
        self.input_box.setMinimumHeight(50)
        self.input_box.setFixedSize(650, 40)
        self.input_box.move(475, 870)
        self.input_box.raise_()
        self.input_box.textChanged.connect(self.adjust_input_height)
        self.input_box.installEventFilter(self)

        self.send_button.setStyleSheet(send_button_style())
        self.send_button.setFixedSize(35, 35)
        self.send_button.setIcon(QIcon("Icons/arrow-right.png"))
        self.send_button.setIconSize(QSize(18, 18))
        self.send_button.move(1086, 874)
        self.send_button.raise_()
        self.send_button.clicked.connect(self.conversation.send_message)

        # SideBar and It's Options
        self.side_bar.setStyleSheet(side_bar_style())
        self.side_bar.setGeometry(1600, 0, 320, 1080)

        self.line_widget.setStyleSheet("background-color: #2f0277")
        self.line_widget.setGeometry(1620, 160, 280, 1)

        self.edit_button.setStyleSheet(edit_button_style())
        self.edit_button.setGeometry(1620, 175, 280, 35),
        self.edit_button.setText("   Edit")
        self.edit_button.setIcon(QIcon("Icons/Edit.png"))
        self.edit_button.setIconSize(QSize(30, 30))
        self.edit_button.clicked.connect(self.open_edit)

        self.persona_button.setStyleSheet(edit_button_style())
        self.persona_button.setGeometry(1620, 235, 280, 35)
        self.persona_button.setText("    Persona")
        self.persona_button.setIcon(QIcon("Icons/persona.png"))
        self.persona_button.setIconSize(QSize(25, 25))
        self.persona_button.clicked.connect(self.persona_select)

        self.memory_button.setStyleSheet(edit_button_style())
        self.memory_button.setGeometry(1620, 295, 280, 35)
        self.memory_button.setText("    Memory")
        self.memory_button.setIcon(QIcon("Icons/pin.png"))
        self.memory_button.setIconSize(QSize(27, 27))
        self.memory_button.clicked.connect(self.open_memory)

        self.clear_chat.setStyleSheet(edit_button_style())
        self.clear_chat.setGeometry(1610, 110, 150, 35)
        self.clear_chat.setText("Clear Chat")
        self.clear_chat.setIcon(QIcon("Icons/comment.png"))
        self.clear_chat.setIconSize(QSize(27, 27))
        self.clear_chat.clicked.connect(self.conversation.clear_chat)

        self.import_model.setStyleSheet(edit_button_style())
        self.import_model.setGeometry(1620, 840, 280, 35)
        self.import_model.setText("Import Model   (.gguf)")
        self.import_model.setIcon(QIcon("Icons/import.png"))
        self.import_model.setIconSize(QSize(27, 27))
        self.import_model.clicked.connect(self.import_gguf_model)

        self.title_icon = CircularImageWidget(self.bot_icon_path, 75)
        self.title_icon.move(1620, 15)

        self.title_name = QLabel(self.bot_data['bot_name'])
        self.title_name.setStyleSheet(title_name_style())
        self.title_name.setGeometry(1705, 14, 200, 40)
        # -----------------------------------------------
        self.chat_display.setParent(self)
        self.input_container.setParent(self)
        self.input_box.setParent(self)
        self.send_button.setParent(self)
        self.side_bar.setParent(self)
        self.line_widget.setParent(self)
        self.edit_button.setParent(self)
        self.persona_button.setParent(self)
        self.memory_button.setParent(self)
        self.clear_chat.setParent(self)
        self.import_model.setParent(self)
        self.title_icon.setParent(self)
        self.title_name.setParent(self)
        # -----------------------------------------------
        positions = [(1880, 187), (1880, 247), (1880, 306)]
        for x, y in positions:
            icon = QLabel(self)
            icon.setPixmap(QPixmap("Icons/expand_arrow.png").scaled(13, 13))
            icon.move(x, y)
            self.expand_icons.append(icon)  # Store reference
        self.showNormal()

    def adjust_input_height(self):
        doc = self.input_box.document()
        # Set the max width dynamically to stop before the send_button
        max_text_width = self.send_button.x() - self.input_box.x() - 20
        doc.setTextWidth(max_text_width)  # Limit text width to prevent overlap

        new_height = min(150, max(50, int(doc.size().height() + 10)))
        self.input_box.setFixedHeight(new_height)
        self.send_button.move(1084, 870 + new_height - 40)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.input_box and event.type() == QEvent.KeyPress:
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                if event.modifiers() == Qt.ShiftModifier:
                    self.input_box.insertPlainText("\n")
                    return True
                else:
                    self.send_button.click()
                    return True
        return super().eventFilter(obj, event)

    def open_edit(self):
        self.bot_data = self.load_bot_settings()
        self.edit_window = EditBot(self)
        self.edit_window.show()

    def persona_select(self):
        self.persona_window = PersonaSelector(self)
        self.persona_window.show()

    def open_memory(self):
        self.memory_window = Memory(self)
        self.memory_window.show()

    def load_bot_settings(self):
        try:
            with open("config/bot.json", 'r') as f:
                return json.load(f)
        except Exception as e:
            print("Data not found", e)

    def import_gguf_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select GGUF Model", "", "GGUF Model (*.gguf)")
        if not file_path:
            return


