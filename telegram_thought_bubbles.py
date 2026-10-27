import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QScrollArea, QFrame, QPushButton, QInputDialog, QCheckBox, QDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SettingsDialog(QDialog):
    """Окно настроек Telegram"""
    def __init__(self, parent=None, current_state=True):
        super().__init__(parent)
        self.setWindowTitle("Настройки: Мысли над чатами")
        self.resize(320, 200)
        self.setStyleSheet("background-color: #17212b; color: white;")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("⚙️ Конфиденциальность и Чаты")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #5288c1;")
        layout.addWidget(title)

        self.cb_show = QCheckBox("Показывать облака мыслей над чатами")
        self.cb_show.setChecked(current_state)
        self.cb_show.setStyleSheet("color: white; font-size: 13px;")
        layout.addWidget(self.cb_show)

        lbl_privacy = QLabel("Кто может видеть мои мысли:")
        lbl_privacy.setStyleSheet("color: #7f91a4; font-size: 12px; margin-top: 5px;")
        layout.addWidget(lbl_privacy)

        self.btn_privacy = QPushButton("🌍 Все пользователи (Изменить)")
        self.btn_privacy.setStyleSheet("background-color: #2b5278; color: white; border-radius: 6px; padding: 6px;")
        layout.addWidget(self.btn_privacy)

        btn_close = QPushButton("Готово")
        btn_close.setStyleSheet("background-color: #5288c1; color: white; border-radius: 6px; padding: 8px; font-weight: bold;")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

class ThoughtBubble(QFrame):
    """Облако мыслей с поддержкой тегов @username и Premium-режима"""
    def __init__(self, texts, is_premium=False, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #2b5278;
                border-radius: 10px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(6)
        
        # Если Premium — показываем до 3 аккуратных тегов в ряд, иначе одно облако
        items_to_show = texts[:3] if (is_premium and isinstance(texts, list)) else [texts[0] if isinstance(texts, list) else texts]
        
        for t in items_to_show:
            label = QLabel()
            label.setStyleSheet("font-size: 11px; background: transparent;")
            
            # Подсветка @username
            if "@" in t:
                formatted_text = re.sub(r'(@\w+)', r'<span style="color: #85c1e9; font-weight: bold; background-color: #1f3a56; border-radius: 4px; padding: 1px 3px;">\1</span>', t)
                label.setText(f"💭 {formatted_text}")
            else:
                label.setText(f"💭 {t}")
                label.setStyleSheet("color: #ffffff; font-size: 11px;")
                
            layout.addWidget(label)

class ChatItem(QWidget):
    """Виджет чата"""
    def __init__(self, name, last_msg, thoughts=None, is_premium=False, show_bubbles=True):
        super().__init__()
        self.thoughts = thoughts
        self.is_premium = is_premium
        self.show_bubbles = show_bubbles
        self.bubble_widget = None

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(2)
        self.main_layout.setContentsMargins(8, 4, 8, 4)

        self.bubble_container = QHBoxLayout()
        self.main_layout.addLayout(self.bubble_container)

        self.render_bubble()

        chat_row = QHBoxLayout()
        
        avatar = QLabel(name[0])
        avatar.setFixedSize(38, 38)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setStyleSheet("""
            background-color: #5288c1;
            color: white;
            font-weight: bold;
            font-size: 14px;
            border-radius: 19px;
        """)
        chat_row.addWidget(avatar)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(1)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")
        
        msg_label = QLabel(last_msg)
        msg_label.setStyleSheet("color: #7f91a4; font-size: 11px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(msg_label)
        chat_row.addLayout(info_layout)
        chat_row.addStretch()

        self.main_layout.addLayout(chat_row)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #17212b; border: none;")
        self.main_layout.addWidget(line)

    def render_bubble(self):
        if self.bubble_widget:
            self.bubble_widget.deleteLater()
            self.bubble_widget = None

        if self.show_bubbles and self.thoughts:
            self.bubble_widget = ThoughtBubble(self.thoughts, self.is_premium)
            self.bubble_container.addWidget(self.bubble_widget, alignment=Qt.AlignmentFlag.AlignLeft)

    def set_thoughts(self, new_thoughts, is_premium):
        self.thoughts = new_thoughts
        self.is_premium = is_premium
        self.render_bubble()

    def set_bubbles_visible(self, visible):
        self.show_bubbles = visible
        self.render_bubble()

class TelegramApp(QWidget):
    """Главное окно приложения"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Telegram Concept: Thought Bubbles")
        self.resize(360, 580)
        self.setStyleSheet("background-color: #0e1621;")

        self.is_premium_active = False
        self.show_bubbles = True
        self.chat_items = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Шапка Telegram
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)
        
        title = QLabel("Telegram")
        title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()

        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setFixedSize(32, 32)
        self.btn_settings.setStyleSheet("background-color: #17212b; color: white; border-radius: 16px; font-size: 14px;")
        self.btn_settings.clicked.connect(self.open_settings)
        header_layout.addWidget(self.btn_settings)

        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #17212b;")
        header_frame.setLayout(header_layout)
        layout.addWidget(header_frame)

        # Панель быстрых действий
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(10, 6, 10, 6)

        self.btn_set_thought = QPushButton("💭 Моя мысль")
        self.btn_set_thought.setStyleSheet("background-color: #2b5278; color: white; border-radius: 6px; padding: 5px; font-size: 12px; font-weight: bold;")
        self.btn_set_thought.clicked.connect(self.change_my_thought)
        actions_layout.addWidget(self.btn_set_thought)

        self.btn_premium = QPushButton("⭐ Premium: OFF")
        self.btn_premium.setStyleSheet("background-color: #17212b; color: #e5c07b; border: 1px solid #e5c07b; border-radius: 6px; padding: 5px; font-size: 12px;")
        self.btn_premium.clicked.connect(self.toggle_premium)
        actions_layout.addWidget(self.btn_premium)

        layout.addLayout(actions_layout)

        # Список чатов
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)

        self.chats_data = [
            ("Вы (Избранное)", "Заметки", ["Думаю о @elena ❤️", "Кожу под Linux", "☕ чай"]),
            ("Елена (@elena)", "В сети недавно", ["Жду вечера ✨", "@bogdan привет!", "гулять"]),
            ("Павел Дуров", "Готовим апдейт...", ["Будущее дизайна — это код 🚀"]),
            ("Алексей", "Как дела с кодом?", ["Срочно нужен кофе..."]),
            ("Разработка Telegram", "Новые функции", None),
        ]

        for name, msg, thoughts in self.chats_data:
            item = ChatItem(name, msg, thoughts, is_premium=self.is_premium_active, show_bubbles=self.show_bubbles)
            self.chat_items.append(item)
            scroll_layout.addWidget(item)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def change_my_thought(self):
        text, ok = QInputDialog.getText(self, "Мысль над чатом", "Введите мысль (через запятую для Premium-режима):")
        if ok and text:
            thoughts_list = [t.strip() for t in text.split(",") if t.strip()]
            self.chat_items[0].set_thoughts(thoughts_list, self.is_premium_active)

    def toggle_premium(self):
        self.is_premium_active = not self.is_premium_active
        if self.is_premium_active:
            self.btn_premium.setText("⭐ Premium: ON")
            self.btn_premium.setStyleSheet("background-color: #8a2be2; color: white; border-radius: 6px; padding: 5px; font-size: 12px; font-weight: bold;")
        else:
            self.btn_premium.setText("⭐ Premium: OFF")
            self.btn_premium.setStyleSheet("background-color: #17212b; color: #e5c07b; border: 1px solid #e5c07b; border-radius: 6px; padding: 5px; font-size: 12px;")

        for item in self.chat_items:
            if item.thoughts:
                item.set_thoughts(item.thoughts, self.is_premium_active)

    def open_settings(self):
        dialog = SettingsDialog(self, current_state=self.show_bubbles)
        if dialog.exec():
            self.show_bubbles = dialog.cb_show.isChecked()
            for item in self.chat_items:
                item.set_bubbles_visible(self.show_bubbles)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelegramApp()
    window.show()
    sys.exit(app.exec())
