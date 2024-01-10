from umodbus.serial import Serial as ModbusRTUMaster
from machine import Pin
from machine import UART
#print(Pin(0))
#u0 = UART(0, baudrate=4800, bits=8, parity=None, stop=1)
#print(u0)
#uart =UART(0,baudrate = 115200,bits = 8,parity = None,stop = 1 ,tx = Pin(0),rx = Pin(1))
#print(uart)
host = ModbusRTUMaster(
    pins=(Pin('GP0'), Pin('GP1')),      # given as tuple (TX, RX), check MicroPython port specific syntax
    # baudrate=9600,    # optional, default 9600
    # data_bits=8,      # optional, default 8
    # stop_bits=1,      # optional, default 1
    # parity=None,      # optional, default None
    # ctrl_pin=12,      # optional, control DE/RE
    #woot ja nav 0 tad met bad tx port  D: :D :D :D 
    uart_id=0         # optional, see port specific documentation
)

# address of the target/client/slave device on the bus
slave_addr = 10
coil_address = 123
coil_qty = 1
for i in range (10):
    slave_addr = i
    coil_status = host.read_coils(
    slave_addr=slave_addr,
    starting_addr=coil_address,
    coil_qty=coil_qty)
    print('Status of coil {}: {}'.format(coil_address, coil_status))