import minimalmodbus

class Device:
    deviceID = None
    isConstant = False
    constantValue = 0.0
    nodeAddress = 1
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
        self.readStart = map["read_start"]
        self.stopBits = map["stop_bits"]
        self.timeout = map["time_out"]
        self.instrument = minimalmodbus.Instrument("/dev/ttyAgitators", self.nodeAddress, close_port_after_each_call = self.closePort)

    def read(self):
        data = self.instrument.read_registers(self.readStart, self.messageLength, 3)
        self.instrument.serial.close()