'''main.py (integration of all)'''

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QTextEdit, QLabel, QHBoxLayout,
                               QMessageBox, QComboBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient
from PySide6.QtSvg import QSvgRenderer


from homepage import Homepage



def main():
    """Main application entry point"""
    
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