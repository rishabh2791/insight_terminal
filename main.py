import requests
import settings
import json
from agitator.anchor import Anchor
from agitator.cowl import Cowl
from agitator.paddle import Paddle
from agitator.emulsifier import Emulsifier
from agitator.inner import InnerAgitator
from temperature.main_vessel import MainVesselTemperature
from temperature.hot_pot import HotPotTemperature
from pressure.main_vessel import MainVesselPressure
from weight.main_vessel import MainVesselWeight
from weight.hot_pot import HotPotWeight


deviceTypes = {
    "Anchor" : Anchor,
    "Cowl" : Cowl,
    "Emulsifier" : Emulsifier,
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
        model = deviceTypes[payload["device_type"]["description"]](payload)
        devices.append(model)


def main():
    getAllVesselDevices()
    print(devices)
    pass


if __name__=="__main__":
    main()