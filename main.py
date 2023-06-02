import requests
import settings
import json
import time
from datetime import datetime
from agitator.anchor import Anchor
from agitator.cowl import Cowl
from agitator.paddle import Paddle
from agitator.emulsifier import Emulsifier
from agitator.inner import InnerAgitator
from agitator.hot_pot import HotPot
from temperature.main_vessel import MainVesselTemperature
from temperature.hot_pot import HotPotTemperature
from pressure.main_vessel import MainVesselPressure
from weight.main_vessel import MainVesselWeight
from weight.hot_pot import HotPotWeight


deviceTypes = {
    "Anchor" : Anchor,
    "Cowl" : Cowl,
    "Emulsifier" : Emulsifier,
    "Hot Pot": HotPot,
    "Hot Pot Load Cell" : HotPotWeight,
    "Hot Pot Temperature" : HotPotTemperature,
    "Inner Agitator" : InnerAgitator,
    "Main Vessel Load Cell" : MainVesselWeight,
    "Main Vessel Pressure" : MainVesselPressure,
    "Main Vessel Temperature" : MainVesselTemperature,
    "Paddle" : Paddle,
}

devices = []


def getAllVesselDevices():
    start = datetime.now()
    print("Getting Devices List")
    url = settings.BASE_URL + "device/"
    condition = {
        "EQUALS":
        {
            "Field":"vessel_id",
            "Value":settings.VESSEL_ID
        }
    }
    response = requests.post(url, json=condition)
    if isinstance(response, Exception):
        exit()
    payloads = json.loads(response.content.decode("utf-8"))["payload"]
    for payload in payloads:
        if payload["enabled"]:
            model = deviceTypes[payload["device_type"]["description"]](payload)
            devices.append(model)
    timeTaken = datetime.now() - start
    print(f"Got Devices List in {timeTaken}s.")


def getDeviceData():
    for device in devices:
        device.read()


def runTimer():
    while True:
        time.sleep(1)
        getDeviceData()


def main():
    getAllVesselDevices()
    # runTimer()


if __name__=="__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main()