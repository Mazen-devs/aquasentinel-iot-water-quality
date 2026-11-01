# Turbidity proxy (Packet Tracer "Wind Detector" device, Python runtime).
# Transcribed from the code screenshot in the project report.
from time import *
from physical import *
from ioeclient import IoEClient

toggle = False


def setup():
    # Give the device the exact native format its firmware expects
    IoEClient.setup({
        "type": "Wind Detector",
        "states": [{
            "name": "level",
            "type": "number",
            "unit": "km/h"
        }]
    })


def loop():
    global toggle
    toggle = not toggle

    # 10 = alert (turbidity > 5.0 rule), 0 = safe
    value = 10 if toggle else 0

    IoEClient.reportStates(value)
    setDeviceProperty(getName(), "level", value)

    print("API Level Sent: " + str(value))
    delay(6000)                  # flip state every 6 s


if __name__ == "__main__":
    setup()
    while True:
        loop()
        sleep(0)
