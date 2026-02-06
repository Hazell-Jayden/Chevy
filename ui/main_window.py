from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QFrame, QLabel, 
                               QPushButton, QGridLayout, QStackedWidget,
                               QButtonGroup, QSlider, QStyle,
                               QStyleOptionSlider)
from PySide6.QtCore import Qt, QTimer, QDateTime, QSize
from PySide6.QtGui import QIcon  
from pathlib import Path
import os
import subprocess


class LogoutOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Make it a frameless window that stays on top
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Fill the screen (or the parent window size)
        self.setGeometry(parent.screen().geometry())

        # Layout for the overlay
        layout = QVBoxLayout(self)
        
        # The Exit Button
        self.confirm_exit_btn = QPushButton("EXIT")
        self.confirm_exit_btn.setFixedSize(400, 200)
        self.confirm_exit_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: black;
                font-weight: bold;
                font-size: 80px;
                border: 5px solid black;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: darkred; }
        """)
        
        layout.addWidget(self.confirm_exit_btn, alignment=Qt.AlignCenter)
        self.confirm_exit_btn.clicked.connect(self.final_exit)

    def final_exit(self):
        print("System Exiting...")
        # Closes the whole application
        os._exit(0) 

    def mousePressEvent(self, event):
        # If the user clicks anywhere on the overlay (but not the button), close it
        self.close()

class TouchSlider(QSlider):
    def mousePressEvent(self, event):
        # If the user clicks with the left button (or a finger touch)
        if event.button() == Qt.LeftButton:
            # Calculate the new value based on click position
            # This math converts pixel-position into the 1-100 range
            opt = QStyleOptionSlider()
            self.initStyleOption(opt)
            sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
            
            new_value = QStyle.sliderValueFromPosition(
                self.minimum(), self.maximum(), 
                event.position().toPoint().x() - sr.left(), 
                sr.width()
            )
            self.setValue(new_value)
            # Accept the event so the handle starts dragging immediately
            event.accept()
        
        # Call the original behavior so dragging still works
        super().mousePressEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_h_layout = QHBoxLayout(self.central_widget)
        self.main_h_layout.setContentsMargins(5, 5, 5, 5) 
        self.main_h_layout.setSpacing(10)

        self.is_screen_off = False
#-------------------------------------------------------------------------------------#
# Left Top Box
#-------------------------------------------------------------------------------------#    
        self.box_top_left = QFrame()
        self.box_top_left.setObjectName("box1")

        self.box_top_left_layout = QVBoxLayout(self.box_top_left)

        self.time_label = QLabel("00:00:00")
        self.time_label.setObjectName("time_label")

        self.date_label = QLabel("Date")
        self.date_label.setObjectName("date_label")

        self.box_top_left_layout.addWidget(self.time_label, alignment=Qt.AlignCenter)
        self.box_top_left_layout.addWidget(self.date_label, alignment=Qt.AlignCenter)

        # Setup the Timer
        self.date_timer = QTimer(self)
        self.date_timer.timeout.connect(self.update_time_date)
        self.date_timer.start(1000) 

        self.update_time_date()
        
#-------------------------------------------------------------------------------------#
# Left Bottom Box
#-------------------------------------------------------------------------------------#
        self.box_bottom_left = QFrame()
        self.box_bottom_left.setObjectName("box2")

        self.box2_layout = QVBoxLayout(self.box_bottom_left)

#-------------------------------------------------------------------------------------#
# Right Box
#-------------------------------------------------------------------------------------#
        self.box_right = QFrame()
        self.box_right.setObjectName("box3")
        self.box_right_layout = QGridLayout(self.box_right)
        self.box_right_layout.setSpacing(15)

        # Button 1
        self.btn1 = QPushButton("")
        self.btn1.setObjectName("btn1")
        self.btn1.setFixedSize(100, 100)
        self.btn1.setIcon(QIcon("ui/icons/brightness_icon.png"))
        self.btn1.setIconSize(QSize(200, 200))
        self.btn1.setCheckable(True)
        self.btn1.setAutoExclusive(True)
        self.btn1.clicked.connect(lambda: self.window_selection(1))
        self.box_right_layout.addWidget(self.btn1, 0, 0)

        # Button 2
        self.btn2 = QPushButton("")
        self.btn2.setObjectName("btn2")
        self.btn2.setFixedSize(100, 100)
        self.btn2.setIcon(QIcon("ui/icons/lightbulb_icon.png"))
        self.btn2.setIconSize(QSize(200, 200))
        self.btn2.setCheckable(True)
        self.btn2.setAutoExclusive(True)
        self.btn2.clicked.connect(lambda: self.window_selection(2))
        self.box_right_layout.addWidget(self.btn2, 0, 1) 

        # Button 3
        self.btn3 = QPushButton("")
        self.btn3.setObjectName("btn3")
        self.btn3.setFixedSize(100, 100)
        self.btn3.setIcon(QIcon("ui/icons/speaker_icon.png"))
        self.btn3.setIconSize(QSize(200, 200))
        self.btn3.setCheckable(True)
        self.btn3.setAutoExclusive(True)
        self.btn3.clicked.connect(lambda: self.window_selection(3))
        self.box_right_layout.addWidget(self.btn3, 1, 0) 

        # Button 4
        self.btn4 = QPushButton("")
        self.btn4.setObjectName("btn4")
        self.btn4.setFixedSize(100, 100)
        self.btn4.setIcon(QIcon("ui/icons/info_icon.png"))
        self.btn4.setIconSize(QSize(200, 200))
        self.btn4.setCheckable(True)
        self.btn4.setAutoExclusive(True)
        self.btn4.clicked.connect(lambda: self.window_selection(4))
        self.box_right_layout.addWidget(self.btn4, 1, 1)    

        # Button 5
        self.btn5 = QPushButton("")
        self.btn5.setObjectName("btn5")
        self.btn5.setFixedSize(100, 100)
        self.btn5.setIcon(QIcon("ui/icons/dark_mode_icon.png"))
        self.btn5.setIconSize(QSize(200, 200))
        self.btn5.clicked.connect(self.toggle_dark_mode)
        self.box_right_layout.addWidget(self.btn5, 2, 0)  

        # Button 6
        self.btn6 = QPushButton("")
        self.btn6.setObjectName("btn6")
        self.btn6.setFixedSize(100, 100)
        self.btn6.setIcon(QIcon("ui/icons/logout_icon.png"))
        self.btn6.setIconSize(QSize(200, 200))
        self.btn6.clicked.connect(self.logout_and_exit)        
        self.box_right_layout.addWidget(self.btn6, 2, 1) 

        self.nav_buttons = [self.btn1, self.btn2, self.btn3, self.btn4]
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True) # Only one green at a time 
        for i, btn in enumerate(self.nav_buttons):
            btn.setCheckable(True)
            # Adding buttons to group with an ID (1, 2, 3, 4)
            self.button_group.addButton(btn, i + 1)

#-------------------------------------------------------------------------------------#
# Stacked Left Box
#-------------------------------------------------------------------------------------#
        # 1. Create the Stacked Widget for the LEFT side
        self.left_stack = QStackedWidget()

        self.left_stack.setStyleSheet("""
            QStackedWidget {
                border: none;
                background: transparent;
            }
        """)
        # 2. PAGE 0: The Original Left Column (Clock + Bottom Box)
        self.left_home_page = QWidget()
        self.left_home_layout = QVBoxLayout(self.left_home_page)
        self.left_home_layout.setSpacing(10)
        self.left_home_layout.setContentsMargins(0, 0, 0, 0)

        # Move your existing boxes into this layout
        self.left_home_layout.addWidget(self.box_top_left, 2)
        self.left_home_layout.addWidget(self.box_bottom_left, 4)
        

        self.screen_brightness_page = QFrame()
        self.screen_brightness_page.setObjectName("screen_brightness_page")
        self.brightness_layout = QVBoxLayout(self.screen_brightness_page)

        self.brightness_layout.setContentsMargins(50, 50, 50, 50)
        self.brightness_layout.setSpacing(30)
        # 1. Title
        self.brightness_label = QLabel("SCREEN BRIGHTNESS")
        self.brightness_label.setObjectName("brightness_title")
        self.brightness_layout.addWidget(self.brightness_label, alignment=Qt.AlignCenter)

        # 2. Brightness Slider
        self.slider = TouchSlider(Qt.Horizontal)
        self.slider.setMinimum(1)   # Don't let it go to 0 (black screen!)
        self.slider.setMaximum(100)
        self.slider.setValue(70)     # Default value
        self.slider.setFixedHeight(100) # Make it big for touch
        self.brightness_layout.addWidget(self.slider)

        # 3. Percentage Display
        self.perc_label = QLabel("70%")
        self.perc_label.setObjectName("brightness_perc")
        self.brightness_layout.addWidget(self.perc_label, alignment=Qt.AlignCenter)

        # Connect the slider to a function
        self.slider.valueChanged.connect(self.update_brightness_logic)

        actual_brightness = self.get_current_system_brightness()
        self.slider.setValue(actual_brightness)
        self.perc_label.setText(f"{actual_brightness}%")

        self.window2 = QFrame()
        self.window2.setObjectName("window2")
        self.window2_layout = QVBoxLayout(self.window2)

        self.window3 = QFrame()
        self.window3.setObjectName("window3")
        self.window3_layout = QVBoxLayout(self.window3)

        self.window4 = QFrame()
        self.window4.setObjectName("window4")
        self.window4_layout = QVBoxLayout(self.window4)
    
        # 4. Add pages to the stack and add the stack to the Main H Layout
        self.left_stack.addWidget(self.left_home_page)       # Index 0
        self.left_stack.addWidget(self.screen_brightness_page) # Index 1# 2. Add them in this order
        self.left_stack.addWidget(self.window2) # Index 1# 2. Add them in this order
        self.left_stack.addWidget(self.window3) # Index 1# 2. Add them in this order
        self.left_stack.addWidget(self.window4) # Index 1# 2. Add them in this order

        # 3. Start on the Home Page
        self.left_stack.setCurrentIndex(0)
        self.current_window = 0

        # IMPORTANT: Replace your old left_column_layout in the main layout
        self.main_h_layout.addWidget(self.left_stack, 6) # Left side (60%)
        self.main_h_layout.addWidget(self.box_right, 4)  # Right side (40%)
        
        self._load_stylesheet()

    def _load_stylesheet(self):
        qss_path = Path(__file__).resolve().parent / "style.qss"
        with open(qss_path, "r") as f:
            self.setStyleSheet(f.read())

    def update_time_date(self):
        now = QDateTime.currentDateTime()
        
        current_time = now.toString("h:mmAP")
        
        day_num = now.date().day()
        suffix = self.get_date_suffix(day_num)
        date_string = f"{day_num}{suffix} {now.toString('MMMM')}"
        
        self.time_label.setText(current_time)
        self.date_label.setText(date_string)

    def get_date_suffix(self, day):
        if 11 <= day <= 13:
            return "th"
        else:
            return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    def window_selection(self, window_index):
        if (self.current_window == window_index):
            self.left_stack.setCurrentIndex(0)
            self.current_window = 0
            print("Returning to Home")

            # CLEAN RESET: Uncheck the currently active button
            active_btn = self.button_group.checkedButton()
            if active_btn:
                # We must turn off exclusivity briefly to uncheck the button
                self.button_group.setExclusive(False)
                active_btn.setChecked(False)
                self.button_group.setExclusive(True)
            
        else:
            self.left_stack.setCurrentIndex(window_index)
            self.current_window = window_index
            

    def update_brightness_logic(self, value):
        # 1. Update the text label
        self.perc_label.setText(f"{value}%")
        
        # 2. Run the hardware command
        try:
            # This runs exactly what you typed in the terminal
            subprocess.run(["sudo", "brightnessctl", "set", f"{value}%"], check=True)
        except Exception as e:
            print(f"Error setting brightness: {e}")

    def get_current_system_brightness(self):
        try:
            # Run the 'get' command to see current percentage
            result = subprocess.run(["brightnessctl", "g"], capture_output=True, text=True)
            current_raw = int(result.stdout.strip())
            
            # Run the 'max' command to see the limit (your 255)
            result_max = subprocess.run(["brightnessctl", "m"], capture_output=True, text=True)
            max_raw = int(result_max.stdout.strip())
            
            # Calculate percentage: (Current / Max) * 100
            return int((current_raw / max_raw) * 100)
        except Exception as e:
            print(f"Sync Error: {e}")
            return 50 # Fallback default
        
    def toggle_dark_mode(self):
        print("Toggling Dark Mode")
        if not self.is_screen_off:
            # 1. Turn Screen Off
            subprocess.run(["brightnessctl", "set", "0%"])
            self.is_screen_off = True
            
            # 2. Show a "Wake Up" Overlay
            # This covers the whole UI so no other buttons can be pressed
            self.wake_overlay = QWidget(self)
            self.wake_overlay.setGeometry(self.rect())
            self.wake_overlay.setStyleSheet("background-color: black;") # Or transparent
            self.wake_overlay.show()
            
            # 3. Connect the overlay click to the wake function
            # We override the mousePressEvent of this overlay specifically
            self.wake_overlay.mousePressEvent = self.wake_up_screen
        else:
            self.wake_up_screen(None)

    def wake_up_screen(self, event):
        # 1. Restore Brightness (to the slider's current value)
        current_val = self.slider.value()
        subprocess.run(["brightnessctl", "set", f"{current_val}%"])
        
        # 2. Remove the overlay and reset state
        if hasattr(self, 'wake_overlay'):
            self.wake_overlay.deleteLater()
        
        self.is_screen_off = False
        print("System Awakened")
        
    def logout_and_exit(self):
            # Instantiate the overlay
            self.overlay = LogoutOverlay(self)
            self.overlay.show()