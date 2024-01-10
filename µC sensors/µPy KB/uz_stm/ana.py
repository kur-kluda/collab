from machine import Pin
import time

co2s2 = machine.ADC(28)
ad2= machine.ADC(29)
while True:
    r = co2s2.read_u16()
    r2 = ad2.read_u16()
    fl = 14.013695652*(r-1072)
    print(f"ppm: {fl}")
    print(r)
    print(f"sysvol : {r2/65535*3.3*3}")
    time.sleep(1)