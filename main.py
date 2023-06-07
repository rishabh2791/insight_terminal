import requests
import settings
import json
import time
import RPi.GPIO as GPIO
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
        getDeviceData()
        time.sleep(60)


def main():
    getAllVesselDevices()
    runTimer()


if __name__=="__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    main()


# from pymodbus.client import ModbusSerialClient as ModbusClient
# from pymodbus.transaction import ModbusRtuFramer
# import time
# client = ModbusClient( port = '/dev/ttyAgitators', baudrate = 9600, timeout = 1, parity = 'N', stopbits=2, bytesize=8)
# client.connect()
# try:   
    # result = client.read_holding_registers(5, 8, slave = 4)  
    # result = client.read_coils(5, 8, 3)
    # print(result)
    # print(result.registers)
    # print("Motor Speed : {}".format(result.registers[2]))  
    # time.sleep(1)   
    # #start bit  0          
    # result = client.write_registers(0,1278,unit = 1)   
    # time.sleep(1)   
    # #start bit  1    
    # result = client.write_registers(0,1279,unit = 1)  
    # time.sleep(1)    
    # #after start operation  
    # print("operation starts:")    
    # myCounter = 5  
    # speedRef = 0   
    # while myCounter:              
    #     result = client.write_registers(1,speedRef,unit = 1)   
    #     time.sleep(1)      
    #     result = client.read_holding_registers(100,20,unit = 0x01)  
    #     print("Motor Speed : {} ".format(result.registers[0]))  
    #     myCounter = myCounter - 1     
    #     speedRef = speedRef + 10000    
    #     time.sleep(10)   
    # #Stop Operation   
    # #speed ref will be 0 rpm    
    # time.sleep(5)   
    # result = client.write_registers(1,0,unit = 1)  
    # time.sleep(20)   
    # result = client.read_holding_registers(100,20,unit = 0x01)   
    # print("Motor Speed : {}".format(result.registers[0]))  
    # #driver start bit will be 0 and driver will stop 
    # result = client.write_registers(0,0,unit = 1)
    # result = client.read_holding_registers(100,20,unit = 0x01)   
    # print("Motor Speed : {}".format(result.registers[0]))
# except Exception as e:   
#     print(e)
#     pass    
# time.sleep(1)
# client.close() 