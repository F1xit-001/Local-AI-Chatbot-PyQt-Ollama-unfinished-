def input_box_style():
    return """
    QTextEdit {background-color: #2f2f2f; color: #ececec; padding: 10px; border-radius: 20px;
            font-size: 15px; font-family: 'Inter 24pt'; border-top: 3px solid rgba(47, 2, 119, 0.5);
            }
    """


def send_button_style():
    return """
    QPushButton {
                background-color: #ffffff; color: white; padding: 15px; border-radius: 17px;
                min-width: 1px; min-height: 1px; text-align: center;
                }
                QPushButton:hover {background-color: #dddbdb;}
                QPushButton:pressed {background-color: #dddbdb; padding-top: 6px; padding-bottom: 3px;}
    """


def side_bar_style():
    return """
    background-color: #131316; padding: 5px;
    border-left: 2px solid rgba(47, 2, 119, 0.5);
    """


def edit_button_style():
    return """
    QPushButton {background-color: #131316; color: #ececec; padding: 5px 11px; border-radius: 7px; font-size: 18px;
        font-family: 'Inter 24pt';text-align: left}
        QPushButton:pressed {background-color: #303034; padding-top: 7px; padding-bottom: 2px}
        QPushButton:hover {background-color: #303034}
    """


def title_close_btn_style():
    return """
    QPushButton {background-color: #131316; color: white; border-radius: 16px;}
        QPushButton:hover {background-color: #303034}
    """


def char_name_style():
    return """
    background-color: #131316; color: white; border-radius: 9px;
    border: 1px solid #2f0277; padding: 8px; font-family: 'Inter 24pt';
    font-size: 14px
    """


def label_name_style():
    return """
    background-color: #131316; color: white; font-size: 15px; font-family: 'Inter 24pt'
    """


def save_button_style():
    return """
    QPushButton {
        background-color: #e3e3e3; color: black; border-radius: 8px; padding: 4px; font-size: 12px; font-family: 'Inter 24pt'}
        QPushButton:hover {background-color: #bababa}
        QPushButton:pressed {padding-top: 7px; padding-bottom: 2px}
    """


def create_persona_style():
    return """
    QPushButton {background-color: #131316; border-radius: 20px}
        QPushButton:hover {background-color: #303034}
    """


def persona_btn_style():
    return """
    QPushButton {background-color: #131316; color: white; border-radius: 12px; padding: 8px 20px;
            font-size: 20px; font-family: 'Inter 24pt'; text-align: center}
            QPushButton:hover {background-color: #303034}
            QPushButton:pressed {padding-top: 7px; padding-bottom: 2px}
            """


def delete_button_style():
    return """
    QPushButton {
        background-color: #ffc1b5; color: black; border-radius: 8px; padding: 2px; font-size: 15px; font-family: 'Inter 24pt'}
        QPushButton:hover {background-color: #ff5230}
        QPushButton:pressed {padding-top: 7px; padding-bottom: 2px}
    """


def msg_box_style():
    return """
        QMessageBox {background-color: #131316; color: #ffffff; border: 1px solid #2f0277}
        QMessageBox QLabel {color: #ffffff; font-size: 12px; font-family: 'Inter 24pt'}
        QPushButton {background-color: #e3e3e3; color: #131316; border-radius: 5px; padding: 5px; font-size: 11px;
        font-family: 'Inter 24pt'}
        QPushButton:hover {background-color: #bababa}
        QPushButton:pressed {padding-top: 7px; padding-bottom: 2px}
    """


def set_active_button_style():
    return """
    QPushButton {
        background-color: #44178c; color: black; border-radius: 8px; padding: 2px; font-size: 15px; font-family: 'Inter 24pt'}
        QPushButton:hover {background-color: #4b3372}
        QPushButton:pressed {padding-top: 7px; padding-bottom: 2px}
    """


def title_name_style():
    return """
    background: transparent; border: none; font-family: 'inter 24pt'; font-size: 16px; color: white
    """


def user_message_label_style():
    return """
            background-color: #333333;
            color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'Inter 24pt'
        """


def bot_message_label_style():
    return """
            background-color: #25015e;
            color: #ffffff;
            padding: 10px;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'Inter 24pt'
    """


def above_message_info_style():
    return """
    font-weight: bold; color: white; margin-left: 10px; font-size: 14px;
    """


def regenerate_button_style():
    return """
    QPushButton {background-color: #131316; color: white; border-radius: 13px;}
            QPushButton:hover {background-color: #303034}
    """


def title_style():
    return """
    background-color: #131316; color: white; font-size: 17px; font-family: 'Inter 24pt'
    """