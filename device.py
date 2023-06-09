import serial
import requests
import settings
import minimalmodbus
import RPi.GPIO as GPIO

class Device:
    deviceID = None
    isConstant = False
    constantValue = 0.0
    factor = 1
    nodeAddress = 1
    port = "/dev/ttyAgitators"
    additionalNodeAddress = 22
    readStart = 0
    baudrate = 9600
    byteSize = 8
    stopBits = 2
    timeout = 0.5
    messageLength = 16
    clearBuffer = True
    closePort = True
    instrument = None
    communicationMethod = "modbus"
    previousState = None
    

    def __init__(self, map):
        self.port = map["port"]
        self.deviceID = map["id"]
        self.baudrate = map["baud_rate"]
        self.byteSize = map["byte_size"]
        self.clearBuffer = map["clear_buffers_before_each_transaction"]
        self.closePort = map["close_port_after_each_call"]
        self.constantValue = map["constant_value"]
        self.isConstant = map["is_constant"]
        self.messageLength = map["message_length"]
        self.nodeAddress = map["node_address"]
        self.factor = map["factor"]
        self.additionalNodeAddress = map["additional_node_address"]
        self.readStart = map["read_start"]
        self.stopBits = map["stop_bits"]
        self.timeout = map["time_out"]
        self.communicationMethod = map["communication_method"]
        if (self.communicationMethod == "constant"):
            self.initGPIO()
        if (self.communicationMethod == "modbus"):
            self.initModbus()
        if(self.communicationMethod=="serial"):
            self.initSerial()

    
    def initModbus(self):
        self.instrument = minimalmodbus.Instrument(self.port, self.nodeAddress)
        self.instrument.mode = minimalmodbus.MODE_RTU
        self.instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.serial.baudrate = self.baudrate
        self.instrument.serial.bytesize = self.byteSize
        self.instrument.serial.stopbits = self.stopBits
        self.instrument.serial.timeout = self.timeout
        self.instrument.clear_buffers_before_each_transaction = self.clearBuffer
        self.instrument.close_port_after_each_call = self.closePort


    def initGPIO(self):
        GPIO.setup(self.additionalNodeAddress, GPIO.OUT)
        GPIO.setup(self.nodeAddress, GPIO.IN, GPIO.PUD_DOWN)
        GPIO.output(self.additionalNodeAddress, GPIO.LOW)
        self.previousState = GPIO.input(self.nodeAddress)


    def initSerial(self):
        self.instrument = serial.Serial(self.port)
        self.instrument.parity = minimalmodbus.serial.PARITY_NONE
        self.instrument.baudrate = self.baudrate
        self.instrument.bytesize = self.byteSize
        self.instrument.stopbits = self.stopBits
        self.instrument.timeout = self.timeout
        self.instrument.close()


    def read(self):
        url = settings.BASE_URL + "devicedata/create/"
        postData = {
            "device_id": self.deviceID,
            "value": 0
        }
        if(self.communicationMethod == "constant"):
            data = self.readFromGPIO()
            postData["value"] = data
        if (self.communicationMethod == "modbus"):
            data = self.readFromModbus() 
            postData["value"] = round(data[0]/self.factor,2)
        if (self.communicationMethod == "serial"):
            data = self.readFromSerial()
            weight = round(float(self.readFromSerial()[-2]),2)
            postData["value"] = weight
        print(postData)
        response = requests.post(url, json=postData)
        print(response)


    def readFromModbus(self):
        data = self.instrument.read_registers(self.readStart, self.messageLength, 3)
        self.instrument.serial.close() 
        return data


    def readFromGPIO(self):
        GPIO.output(self.additionalNodeAddress, GPIO.HIGH)
        currentState = GPIO.input(self.nodeAddress)
        GPIO.output(self.additionalNodeAddress, GPIO.LOW)
        if(currentState == GPIO.HIGH and self.previousState == GPIO.LOW):
            return self.constantValue
        else:
            self.previousState = currentState
            return 0
        
        
    def readFromSerial(self):
        self.instrument.open()
        lines = self.instrument.readlines(3)
        self.instrument.close()
        return lines[-1].decode("utf-8").split(" ")
