```
12 width tātad 4096 (0-4095). Vref ~=3.3V
(DACiks+1) * 3300 / 4096 ==> salīdzinošie mV
```

---
```
??vai 4 ==0 vai tomēr 0==0?? TODO: A avots
ja 4==0:
(sensora_max - sensora_min)* SmV/Vref + sensora_min

4600 * Smv/Vref - 400
```
---

(sensora_max - sensora_min)*(DACiks+1)/2^DAC_w + sensora_min

4600*(DACiks+1)/4096+40

1.123046875*(DACiks+1)+40
