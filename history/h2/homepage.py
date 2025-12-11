import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QPushButton, QTextEdit, QLabel, QHBoxLayout,
                               QMessageBox, QComboBox, QGroupBox, QScrollArea)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QTimer, QSize
from PySide6.QtGui import QFont, QIcon, QColor, QLinearGradient
from PySide6.QtSvg import QSvgRenderer

from backend import VoiceRecognitionBackend
from components import (VoiceSignals,StyledButton)


class Homepage(QMainWindow):
    """Main UI window for voice recognition application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Recognition Assistant")
        self.setGeometry(100, 100, 850, 750)
        self.setMinimumSize(800, 650)
        
        # Apply application-wide stylesheet
        self.setup_app_style()
        
        # Backend instance
        self.backend = VoiceRecognitionBackend()
        
        # Signals for thread-safe updates
        self.signals = VoiceSignals()
        self.signals.text_recognized.connect(self.on_text_recognized)
        self.signals.status_update.connect(self.on_status_update)
        self.signals.error_occurred.connect(self.on_error_occurred)
        
        # Setup backend callbacks
        self.backend.set_callbacks(
            on_text_recognized=lambda text: self.signals.text_recognized.emit(text),
            on_status_update=lambda msg, color: self.signals.status_update.emit(msg, color),
            on_error=lambda error: self.signals.error_occurred.emit(error)
        )
        
        # Get microphone list
        self.microphone_list = self.backend.get_microphone_list()
        
        # Setup UI
        self.setup_ui()
        
        # Show welcome message
        QTimer.singleShot(500, self.show_welcome_message)
        
    def setup_app_style(self):
        """Setup application-wide styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #2c3e50;
            }
            QComboBox {
                padding: 8px 12px;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
                background-color: #ecf0f1;
            }
            QGroupBox {
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #f5f7fa;")
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        
        title = QLabel("🎤 Voice Recognition Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        header_layout.addWidget(title)
        
        subtitle = QLabel("Speak clearly and let AI convert your words to text")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #7f8c8d; padding: 5px;")
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        
        # Microphone selection group
        mic_group = QGroupBox("🎙️ Microphone Settings")
        mic_group.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border: 2px solid #e0e6ed;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        mic_layout = QVBoxLayout()
        mic_layout.setSpacing(10)
        
        mic_label = QLabel("Select Microphone Device:")
        mic_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        mic_layout.addWidget(mic_label)
        
        self.mic_combo = QComboBox()
        self.mic_combo.addItems(self.microphone_list)
        self.mic_combo.setMinimumHeight(38)
        self.mic_combo.setStyleSheet("""
            QComboBox {
                padding: 10px 12px;
                border: 2px solid #e0e6ed;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
            QComboBox:focus {
                border: 2px solid #2980b9;
                background-color: #ecf0f1;
            }
        """)
        mic_layout.addWidget(self.mic_combo)
        mic_group.setLayout(mic_layout)
        main_layout.addWidget(mic_group)
        
        # Status indicator
        self.status_label = QLabel("Status: Ready to start")
        self.status_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status_label.setMinimumHeight(50)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #d5f4e6;
                padding: 15px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                border-left: 5px solid #27ae60;
                color: #27ae60;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # Control buttons - styled for better UX
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.start_btn = StyledButton("▶️ Start Listening", "#27ae60", "#229954")
        self.start_btn.clicked.connect(self.start_listening)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setMinimumWidth(180)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = StyledButton("⏹️ Stop Listening", "#e74c3c", "#c0392b")
        self.stop_btn.clicked.connect(self.stop_listening)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setMinimumWidth(180)
        button_layout.addWidget(self.stop_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Recognized text display with enhanced styling
        text_label = QLabel("📝 Recognized Text")
        text_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        text_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        main_layout.addWidget(text_label)
        
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText(
            "Your recognized speech will appear here...\n\n"
            "Click 'Start Listening' and speak clearly into your microphone."
        )
        self.text_display.setMinimumHeight(160)
        self.text_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e6ed;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-family: 'Segoe UI', 'Consolas', monospace;
                color: #2c3e50;
                selection-background-color: #3498db;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        main_layout.addWidget(self.text_display)
        
        # Action buttons in organized layout
        action_layout = QHBoxLayout()
        action_layout.setSpacing(10)
        
        test_btn = StyledButton("🔊 Test Speech", "#3498db", "#2980b9")
        test_btn.clicked.connect(self.test_speech)
        test_btn.setMinimumHeight(42)
        action_layout.addWidget(test_btn)
        
        clear_btn = StyledButton("🗑️ Clear Text", "#f39c12", "#d68910")
        clear_btn.clicked.connect(self.clear_text)
        clear_btn.setMinimumHeight(42)
        action_layout.addWidget(clear_btn)
        
        help_btn = StyledButton("❓ Help", "#9b59b6", "#8e44ad")
        help_btn.clicked.connect(self.show_help)
        help_btn.setMinimumHeight(42)
        action_layout.addWidget(help_btn)
        
        main_layout.addLayout(action_layout)
        
        # Footer
        footer = QLabel("Voice Recognition Assistant v1.0 | © 2024")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #95a5a6; font-size: 11px; padding: 10px; font-weight: 500;")
        main_layout.addWidget(footer)
        
        central_widget.setLayout(main_layout)
        
    def show_welcome_message(self):
        """Show welcome message on startup"""
        self.signals.status_update.emit(
            "👋 Welcome! Select your microphone and click 'Start Listening'", 
            "#27ae60"
        )
        
    def start_listening(self):
        """Start voice recognition"""
        mic_index = self.mic_combo.currentIndex()
        
        if self.backend.start_listening(mic_index):
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.mic_combo.setEnabled(False)
            
    def stop_listening(self):
        """Stop voice recognition"""
        if self.backend.stop_listening():
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.mic_combo.setEnabled(True)
            
    def test_speech(self):
        """Test text-to-speech"""
        if not self.backend.test_speech():
            QMessageBox.warning(self, "TTS Error", 
                              "Text-to-speech engine is not available.")
        
    def clear_text(self):
        """Clear the text display"""
        if self.text_display.toPlainText():
            reply = QMessageBox.question(
                self, "Clear Text", 
                "Are you sure you want to clear all recognized text?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.text_display.clear()
                self.signals.status_update.emit("🗑️ Text cleared successfully", "#f39c12")
        else:
            QMessageBox.information(self, "Clear Text", "Text area is already empty.")
            
    def show_help(self):
        """Show help dialog with improved styling"""
        help_text = """
        <html>
        <head>
            <style>
                body { font-family: 'Segoe UI', Arial; color: #2c3e50; line-height: 1.6; }
                h2 { color: #2980b9; border-bottom: 2px solid #3498db; padding-bottom: 8px; }
                h3 { color: #34495e; margin-top: 15px; }
                ol, ul { margin-left: 20px; }
                li { margin: 8px 0; }
                b { color: #2980b9; font-weight: 600; }
                code { background-color: #ecf0f1; padding: 2px 6px; border-radius: 4px; }
                .tip { background-color: #d5f4e6; padding: 12px; border-radius: 6px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <h2>📖 How to Use Voice Recognition Assistant</h2>
            
            <h3>🚀 Getting Started:</h3>
            <ol>
                <li>Select your microphone from the dropdown menu</li>
                <li>Click the <b>'Start Listening'</b> button</li>
                <li>Speak clearly into your microphone</li>
                <li>Your speech will be converted to text in real-time</li>
                <li>Click <b>'Stop Listening'</b> when you're done</li>
            </ol>
            
            <h3>💡 Pro Tips:</h3>
            <div class="tip">
                <ul>
                    <li>Speak clearly and at a normal pace</li>
                    <li>Minimize background noise for better accuracy</li>
                    <li>Keep microphone 6-12 inches away from your mouth</li>
                    <li>Ensure you have a stable internet connection</li>
                    <li>Use proper punctuation when mentioning technical terms</li>
                </ul>
            </div>
            
            <h3>🔧 Troubleshooting:</h3>
            <ul>
                <li><b>No recognition:</b> Check microphone permissions and try a different device</li>
                <li><b>Poor accuracy:</b> Reduce background noise and speak more clearly</li>
                <li><b>Network error:</b> Verify your internet connection</li>
                <li><b>Microphone not listed:</b> Reconnect your microphone device</li>
            </ul>
            
            <p style="margin-top: 20px; font-style: italic; color: #7f8c8d;">
                For additional support, please contact the support team.
            </p>
        </body>
        </html>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Help - Voice Recognition Assistant")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Information)
        msg.setMinimumWidth(500)
        msg.exec()
        
        
    @Slot(str)
    def on_text_recognized(self, text: str):
        """Handle recognized text (thread-safe)"""
        current_text = self.text_display.toPlainText()
        
        if current_text:
            self.text_display.append(f"\n• {text}")
        else:
            self.text_display.setText(f"• {text}")
            
    @Slot(str, str)
    def on_status_update(self, status: str, color: str):
        """Update status label (thread-safe)"""
        self.status_label.setText(f"Status: {status}")
        border_color = color if color != "#f44336" else "#e74c3c"
        self.status_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color}15;
                padding: 15px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                border-left: 5px solid {color};
                color: {color};
            }}
        """)
        
    @Slot(str)
    def on_error_occurred(self, error_msg: str):
        """Handle errors (thread-safe)"""
        self.stop_listening()
        QMessageBox.critical(self, "⚠️ Error", error_msg)
        self.signals.status_update.emit("❌ Error occurred. Please try again.", "#e74c3c")
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.backend.is_listening:
            reply = QMessageBox.question(
                self, "Exit Application", 
                "Voice recognition is still running. Exit anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        self.backend.cleanup()
        event.accept()
