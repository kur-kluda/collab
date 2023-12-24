# 1. Aprēķini
12 width tātad 4096 (0-4095). \
$V_{ref} \approx 3.3V$ \
\
$(DACiks+1) * 3300 \over 4096$ ==> salīdzinošie mV [priekš kalibrācijas/debug]

$\approx$ *4/5

---
```
??vai 4 ==0 vai tomēr 0==0?? TODO: A avots
ja 4==0:
```
${(sensora_{max} - sensora_{min})* S_{mV} \over V_{ref}} + sensora_{min} \text{          } \implies\qquad{4600 * S_{mv} \over V_{ref}} - 400 $

---

${(sensora_{max} - sensora_{min})*(DACiks+1) \over 2^{DAC_w}} + sensora_{min}  \implies \qquad {4600 *(DACiks+1) \over 4096}+40 \implies $
<br>
<br>

<p align=center><b>1.123046875 * (DACiks+1)+400 ppm</b></p>

---

# 2. Kalibrācija

![image](https://github.com/kur-kluda/collab/assets/85872382/1f01b496-45d2-4088-a991-7d56b6de6319)

Diemžēl man ir tikai 1 multimetrs, nevaru vienlaicīgi redzēt ieejas strāvu un izejas voltāžu, tad nu centos trāpīt..

Apakšējo nevaru zem 0.07V nolaist, skrūve uz riņķi rauj

---

```
Tātad jākalibrē pret +0.07V = 0mA
tero granulitāte (izšķirtspēja) : 3.3/4096 = 0,000805664 V uz katru DACika līmeni.
zudums: 0.07V ~= 86,884855225 DACika līmeņi (87 grrrr)
```


1. 4mA **cerams** ir uz 400ppm, nevis sākas tā itkā būtu 0pp-> 4mA.. Ja būtu I avots.. Vai shēma kā nonullēt GND sensoru. Vdiv ja mx tad "0" ? or smthn?

2. **cerams** ka tur ir kāds sazarojums vai diode vai kkas, kas nelaiž tiešām virs Vmax.. Ja būtu I avots..


Bez nobīdes būtu:
$V_{kal}={I_{mēr}*V_{ref} \over I_{rangs}}$

## Ieejas ķēdes pretestību, kapacitāti, induktivitāti es nezinu. Tāpēc "kalibrēju" ar ķēdē ieslēgtu sensoru citādi nez kā vēl..

Atsk nulli ignorēšu, aprēķinu pret $V_{ref}$ teorētisko vismaz 2 punktos. ja sakrīt, tiešām ir solītā linearitāte pat ar pārveidotāju kā starpnieku. Ja ne, atstāju pēdējo.

$\implies V_{m-kal}={I_{mēr}*3300 \over 20} \implies \qquad V_{m-kal}={I_{mēr}*165$
