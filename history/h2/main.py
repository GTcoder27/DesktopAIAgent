"""
Frontend
"""
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QTextEdit, QLabel, QHBoxLayout,
                               QMessageBox, QComboBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient
from PySide6.QtSvg import QSvgRenderer

# Import backend
from backend import VoiceRecognitionBackend
from homepage import Homepage





def main():
    """Main application entry point"""
    # Enable high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set application info
    app.setApplicationName("Dekstop AI Agent")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("GTcoder")
    
    try:
        window = Homepage()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Startup Error", f"Failed to start application:\n\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()