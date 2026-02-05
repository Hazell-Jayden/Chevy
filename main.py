import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # 1. Initialize the Application
    app = QApplication(sys.argv)

    # 2. Create the Window
    window = MainWindow()
    
    # 3. Future Hardware Connections go here!
    # Example: arduino.signal.connect(window.update_ui_status)
    window.update_ui_status("Dashboard Loaded. Ready for Arduino.")

    # 4. Show and Run
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()