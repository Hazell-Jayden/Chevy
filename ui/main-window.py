from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class MainWindow(QMainWindow):
    # This is a custom signal we will use later to talk to hardware
    # For now, it's just here as a placeholder for the logic
    def __init__(self):
        super().__init__()

        # Screen setup for the Freenove 800x480
        self.setWindowTitle("Pi Command Center")
        self.setFixedSize(800, 480)
        self.setWindowFlags(Qt.FramelessWindowHint) # No title bar
        self.setStyleSheet("background-color: #121212; color: #E0E0E0;")

        # Central Widget & Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Header
        self.header = QLabel("SYSTEM HUB")
        self.header.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ADB5; margin-bottom: 20px;")
        self.header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.header)

        # Status Label (Where hardware updates will show)
        self.status_display = QLabel("Waiting for Hardware...")
        self.status_display.setStyleSheet("font-size: 18px; background: #1E1E1E; padding: 20px; border-radius: 10px;")
        self.status_display.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.status_display)

        # Buttons Row
        self.button_layout = QHBoxLayout()
        self.power_btn = QPushButton("Lights OFF")
        self.power_btn.setFixedSize(150, 60)
        self.power_btn.setStyleSheet("background-color: #393E46; border-radius: 5px;")
        
        self.exit_btn = QPushButton("Close App")
        self.exit_btn.setFixedSize(150, 60)
        self.exit_btn.setStyleSheet("background-color: #FF2E63; border-radius: 5px;")
        self.exit_btn.clicked.connect(self.close) # Built-in close function

        self.button_layout.addWidget(self.power_btn)
        self.button_layout.addWidget(self.exit_btn)
        self.main_layout.addLayout(self.button_layout)

    def update_ui_status(self, text):
        """A helper function to change the status text from main.py"""
        self.status_display.setText(text)