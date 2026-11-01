# pH sensor proxy (Packet Tracer "CO2 Detector" device, Python runtime).
# Transcribed from the code screenshot in the project report. Packet Tracer's
# Python environment provides time, physical, gpio and ioeclient; this does not
# run under standard CPython.
from time import *
from physical import *
from gpio import *
from ioeclient import IoEClient

toggle = False
tick_count = 0


def setup():
    # Tell the IoT server to expect a numeric property called "Level"
    IoEClient.setup({
        "type": "pH Sensor",
        "states": [{
            "name": "Level",
            "type": "number",
            "unit": "pH",
            "decimalDigits": 1
        }]
    })


def loop():
    global toggle, tick_count
    tick_count += 1
    if tick_count >= 6:          # flip state every 6 s
        toggle = not toggle
        tick_count = 0
    detect()
    delay(1000)


def detect():
    global toggle
    # 2.0 triggers the "pH < 3.0" alert rule; 5.0 triggers the reset rule
    value = 2.0 if toggle else 5.0

    # Report to the IoT server and set every property name the rule engine might read
    IoEClient.reportStates(value)
    setDeviceProperty(getName(), "level", value)
    setDeviceProperty(getName(), "value", value)
    setDeviceProperty(getName(), "pH", value)

    setCustomText(30, 20, 200, 20, "pH: " + str(value))
    print("pH Value Sent: " + str(value))


if __name__ == "__main__":
    setup()
    while True:
        loop()
