import requests
import settings
import minimalmodbus
import RPi.GPIO as GPIO

class Device:
    deviceID = None
    isConstant = False
    constantValue = 0.0
    nodeAddress = 1
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
    

    def __init__(self, map):
        self.deviceID = map["id"]
        self.baudrate = map["baud_rate"]
        self.byteSize = map["byte_size"]
        self.clearBuffer = map["clear_buffers_before_each_transaction"]
        self.closePort = map["close_port_after_each_call"]
        self.constantValue = map["constant_value"]
        self.isConstant = map["is_constant"]
        self.messageLength = map["message_length"]
        self.nodeAddress = map["node_address"]
        self.additionalNodeAddress = map["additional_node_address"]
        self.readStart = map["read_start"]
        self.stopBits = map["stop_bits"]
        self.timeout = map["time_out"]
        if (self.isConstant):
            self.initGPIO()
        else:
            self.initModbus()
        

    def initModbus(self):
        self.instrument = minimalmodbus.Instrument("/dev/ttyAgitators", self.nodeAddress)
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
        GPIO.setup(self.nodeAddress, GPIO.IN, GPIO.PUD_UP)


    def read(self):
        data = None
        if(self.isConstant):
            data = self.readFromGPIO()
        else:
            data = self.readFromModbus() 
            url = settings.BASE_URL + "devicedata/create/"
            postData = {
                "device_id" : self.deviceID,
                "value" : data[0],
            }
            response = requests.post(url, json=postData)
            print(response)
            print("{} - {}".format(self.nodeAddress, data))


    def readFromModbus(self):
        data = self.instrument.read_registers(self.readStart, self.messageLength, 3)
        self.instrument.serial.close() 
        return data


    def readFromGPIO(self):
        status = GPIO.input(self.instrument)
        if(status == GPIO.HIGH):
            return self.constantValue