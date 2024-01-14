# Ievads
# Līdzīgo risinājumu pārskats

1.	 [CISCO sensors Meraki MT14](https://documentation.meraki.com/MT/MT_Datasheets/MT14_Datasheet_-_Indoor_Air_Quality_Monitor)
2.	[CO2 sensors DP-353](https://www.amazon.com/Detector-Monitor-Display-Humidity-Temperature/dp/B0BMGF21RT?th=1)
3.	[ELRO Connects SF500CO2 CO2 Meter Kit](https://www.elro.eu/en/elro-connects-smart-wifi-co2-meter-kit-complete-set-with-linkable-air-quality-meter-k2-connector-sf500co2)
4.	[Disruptive Technologies Sensor Starter Kit](https://www.disruptive-technologies.com/products/wireless-co2-sensor)
5.	[WiFi Smart 3 In 1 Carbon Dioxide Air Quality Monitor Detector Temperature and Humidity Sensor](https://moeshouse.com/products/wifi-3-in-1-co2-monitor TUYA smart)
6.	Tech stack alternatīvas:
a.	openHAB un kontrolieri kā mqqt klienti
b.	[freeRTOS uz konroliera](https://github.com/aws-iot-builder-tools/freertos-pi-pico)

| Kritērijs | 1 | 2 | 3 | 4 | 5 |
|------------|--------------------|---------|-----------|-----------|-----------|
|CO2	| +	| +	| +	| +	| + | 
|Temp	| +	| +	| +	| +	| + | 
|Mitrums | + | + | + | + | + | 
|WiFi	| +	| +	| +	| -/868Mhz	| + | 
|Pieejams vieglās valodas datu novērtējums	| +	| +	| +	| +	| +/- | 
|Mērījumu vēsture	| +/-	| -	| +/-	| +	| - | 
|Iespēja arhivēt datus	| -	| -	| -	| -	| - | 
|Iespēja regulēt biežumu	| -	| -	| -	| +	| - | 
|Iespēja modificēt	| +/-	| -	| -	| -	| - | 
|Cena (eur)  bez piegādes	| 195,24 | 56.99 | 149.00 | 669,00*| 77.70 | 

---

* ar piegādi <br>
+/- -samērā viegli pieejams, taču nepieciešama papildus aparatūra vai konfigurācija

---
<br>

| Risinājums | Pozitīvās īpašības | Trūkumi | Komentāri |
|------------|--------------------|---------|-----------|
|   CISCO Meraki MT14       |      rāda chart conformance, Total volatile organic compound (TVOC),   Particulate matter (PM)            |         | [MT 14 datasheet](https://documentation.meraki.com/MT/MT_Datasheets/MT14_Datasheet_-_Indoor_Air_Quality_Monitor) |
|            |                    |         |           |

keywords:
[air quality smart sensor datasheet](https://www.google.com/search?q=air+quality+smart+sensor+datasheet)

# 1:
* [MT 14 datasheet](https://documentation.meraki.com/MT/MT_Datasheets/MT14_Datasheet_-_Indoor_Air_Quality_Monitor)<br />

* [MT 14 chart description](https://documentation.meraki.com/MT/MT_General_Articles/MT_Psychrometric_Chart)<br />

* [(teorija) kā TVOC ietekmē](https://www.advsolned.com/how-tvoc-affects-indoor-air-quality-effects-on-wellbeing-and-health/)<br />

## 1 attēli:
![www advsolned com_how-tvoc-affects-indoor-air-quality-effects-on-wellbeing-and-health_](https://github.com/kur-kluda/collab/assets/85872382/f1429817-8a07-49af-91ac-83811cad92e1)
![documentation meraki com_MT_MT_Datasheets_MT14_Datasheet_-_Indoor_Air_Quality_Monitor (1)](https://github.com/kur-kluda/collab/assets/85872382/52a8a669-fd37-4e21-992c-69bb7032f9a4)
![documentation meraki com_MT_MT_General_Articles_MT_Psychrometric_Chart (1)](https://github.com/kur-kluda/collab/assets/85872382/9d678f05-1733-43cf-a6f0-fe4a9619e046)

# Papildresursi:
* [Par TVOC un VOC](https://www.jacksonavedental.com/post/tvoc-levels) - Šajā saitē ir paskaidrots kas ir gan TVOC, gan VOC. Tiek pieminēts, kādos produktos ir VOC un kā noteikt vai produkts ir VOC. VOC ietekme uz veselību. Kādā mērā TVOC pēc daudzuma uzskata par veselībai nekaitējošu līdz nāvējošam? Vēl ir parādīts kā interpretēt TVOC rezultātus.

* [Par VOC sensoriem](https://www.thecmmgroup.com/different-types-voc-detectors-available/#:~:text=There%20are%20three%20main%20types,oxide%20semiconductor%20sensor%20(MOS)) - Šajā saitē tiek izklāstīts par VOC sensoriem un to veidiem. Tiek arī likts uzsvars, kadā gadījumā VOC sensori ir efektīvi.

Intelektisko algoritmu atsauces: 
