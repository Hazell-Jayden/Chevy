from gpiozero import Button
from signal import pause

# Define the button on GPIO 17
# 'pull_up=True' uses the Pi's internal resistor so you don't need one!
button = Button(17, pull_up=True)

def button_pressed():
    print("🔘 Button was pressed!")

def button_released():
    print("📤 Button was released!")

# Link the events to the functions
button.when_pressed = button_pressed
button.when_released = button_released

print("System Ready. Press the button! (Ctrl+C to stop)")

# This keeps the script running in the background
pause()