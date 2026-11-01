# Tryptophan-like fluorescence (TLF) proxy for faecal contamination
# (Packet Tracer "Smoke Detector" device, Python runtime).
# Transcribed from the code screenshot in the project report.
from time import *
from physical import *
from gpio import *
from ioeclient import IoEClient

# Variables for the automatic shift
toggle_state = False
tick_count = 0


def setup():
    # Register the device with the IoT server
    IoEClient.setup({
        "type": "Smoke Detector",
        "states": [{
            "name": "Level",
            "type": "number",
            "unit": "",
            "decimalDigits": 2
        }]
    })


def loop():
    global toggle_state, tick_count
    tick_count += 1
    if tick_count >= 7:          # flip state every 7 s
        toggle_state = not toggle_state
        tick_count = 0
    detect()
    delay(1000)


def detect():
    global toggle_state
    # 0.8 triggers the "TLF > 0.5" rule; 0.1 triggers the "< 0.2" reset rule
    value = 0.8 if toggle_state else 0.1

    IoEClient.reportStates(value)
    setDeviceProperty(getName(), "level", value)
    setCustomText(30, 20, 200, 20, "TLF: " + str(value))
    print("TLF Level: " + str(value))


if __name__ == "__main__":
    setup()
    while True:
        loop()
