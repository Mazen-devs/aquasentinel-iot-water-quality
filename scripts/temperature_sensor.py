# Water temperature sensor (Packet Tracer "Temperature Monitor" device, Python runtime).
# Transcribed from the code screenshot in the project report.
from options import Options
from time import *
from physical import *
from gpio import *
from environment import Environment
from ioeclient import IoEClient

unit = "C"
toggle_state = False
tick_count = 0


def setup():
    IoEClient.setup({
        "type": "Temperature Monitor",
        "states": [{
            "name": "Temperature",
            "type": "number",
            "unit": "&deg;C",
            "decimalDigits": 1
        }]
    })


def loop():
    detect()
    delay(1000)


def detect():
    global toggle_state, tick_count
    tick_count += 1
    if tick_count >= 5:          # flip state every 5 s
        toggle_state = not toggle_state
        tick_count = 0

    # 32.0 triggers the "temperature > 30 C" thermal-flush rule
    value = 32.0 if toggle_state else 25.0

    setCustomText(30, 20, 200, 20, str(value) + " " + unit)
    IoEClient.reportStates(value)
    setDeviceProperty(getName(), "level", value)
    print("Sending Temp: " + str(value))


if __name__ == "__main__":
    setup()
    while True:
        loop()
