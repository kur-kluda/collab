from machine import UART, Pin

u0 = UART(0, baudrate=4800, bits=8, parity=None, stop=1)
print(u0)


txData= [0x01,0x03,0x00,0x02,0x00,0x01,0x25,0xCA]
txB = bytearray(txData)
u0.write(txB)

print(f"Sent data : {str(txB)}")


rxD = []
i = 0
dt = 0
while True:
    while(u0.any() <1):
        pass
    while(u0.any() > 0):
        rxD.append(u0.read(1))
        i += 1
        
        if(i ==7):
            print(f"rcv data: {str(rxD)}")
            
            data = ((int.from_bytes(rxD[3], 'big')) << 8) + (int.from_bytes(rxD[4], 'big'))
            
            print(data)
            
            rxD =[]
            i = 0