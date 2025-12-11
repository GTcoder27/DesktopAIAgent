import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QTextEdit, QLabel, QHBoxLayout,
                               QMessageBox, QComboBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient
from PySide6.QtSvg import QSvgRenderer


class VoiceSignals(QObject):
    """Signals for thread-safe GUI updates from backend"""
    text_recognized = Signal(str)
    status_update = Signal(str, str)
    error_occurred = Signal(str)


class StyledButton(QPushButton):
    """Custom styled button with improved appearance"""
    def __init__(self, text, color, hover_color, icon=None):
        super().__init__(text)
        self.color = color
        self.hover_color = hover_color
        self.apply_style()
        
    def apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.color};
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }}
            QPushButton:pressed {{
                transform: scale(0.98);
            }}
            QPushButton:disabled {{
                background-color: #cccccc;
                color: #999999;
            }}
        """)
