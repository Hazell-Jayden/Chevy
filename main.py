import sys
import signal 
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import os
import sys

def main():
    print("Starting program")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()