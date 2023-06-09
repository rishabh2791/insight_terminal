import requests
import settings
import json
import time
from device import Device
import RPi.GPIO as GPIO
from datetime import datetime

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
            model = Device(payload)
            devices.append(model)
    timeTaken = datetime.now() - start
    print(f"Got Devices List in {timeTaken}s.")


def getDeviceData():
    for device in devices:
        device.read()


def runTimer():
    while True:
        getDeviceData()
        time.sleep(60)


def main():
    getAllVesselDevices()
    runTimer()


if __name__=="__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main()

