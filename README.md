# [Projektēšanas pārskats arī pdf](https://github.com/kur-kluda/collab/raw/main/projektesanas_parskats.pdf)
---
---
# [Aplikācija :: Grafiki realtime](https://dj.jtag.me/)

[kods .:. ](https://github.com/kur-kluda/collab/blob/main/Server%20GUI/a/templates/grafiki.html#70)
Tā ir aizsargāta grafana, ko konfigurēt var tikai saslēdzot datoru ar serveri un lietojot īpašu domēnvārdu.

---

Hub 1-4 un sensori 1-13 ir reālo situāciju aprakstoši. 
Pārējie ir ģenerēti, tos droši drīkstat testēt kā vien labpatīk.
Visiem CRUD pamatā viens kods, mainās tikai atribūti.
[kods .:. ](https://github.com/kur-kluda/collab/blob/main/Server GUI/a/tutorial101_ciud_sensors.py#75)

# [Aplikācija :: Mērījumu meta](https://dj.jtag.me/clud/)

# [Aplikācija :: Sensoru meta](https://dj.jtag.me/ciud/)

# [Aplikācija :: Hubu meta](https://dj.jtag.me/crud/)

---

# Aplikācija :: mikrokontrolieru kods ir asinhroni uzdevumi
[kods .:.](https://github.com/kur-kluda/collab/blob/main/µC sensors/pico w dht11/main.py#265)

---

# Aplikācija :: Arhivators ir chron uzdevums
[kods .:.](https://github.com/kur-kluda/collab/blob/main/Archiver/arch.py#67)
Tāpēc nav saites, bet lūk ekrānšāviņi:

![image](https://github.com/kur-kluda/collab/assets/104323709/0573e629-321e-4201-a2ff-bc62ed07d2bd)
![image](https://github.com/kur-kluda/collab/assets/104323709/335ddf50-cd99-49a4-bacf-0c4f6ae221a6)

---
---

## [0 mēģinājums bootstrap](https://dj.jtag.me/s)
## [1. mēģinājums lēni strādā CRUD](https://dj.jtag.me/t)
## [2. mēģinājums lēni strādā CRUD](https://dj.jtag.me/t/)
## [kameras sadalītājs (diemžēl par lēnu)](https://github.com/kur-kluda/collab/blob/main/µC camera/broke.py#212)
## [more config](https://dj.jtag.me/ad)
## [configure grafana](http://apa_dumb/)

Mūsu sistēmas MVP iekļauj sevī vairākus ISO25010:2011 aspektus:





**Funkcionālie:**
Sistēma ir labi piemērota sensoru mērījumu apskatei un pārraudzībai, kamēr vien tiek ievadīti realitātei atbilstoši metadati. Sistēmā ir iekļauti vairāki būtībā atšķirīgi sensoru tipi, tātad tā ir tuvināta reālajai situācijāi (lauka apstākļiem).

Sistēmas precizitāte ir atbilstoša konkrēto mikrokontrolieru precizitātei. Digitāliem sensoriem, protams tas ir iekšējs rādītājs, taču analogajam sensora piemēram mēs izmantojam 12 bitu ADC, kas ļauj iegūt 4096 vērtības.

Sistēma spēj sadarboties ar Raspberry pi, ja to lieto kā centrmezglu vai pat kā wifi nodrošinātāju pārējie centrmezgliem.

**Drošība**: sistēmā ir iekļauts jaukšanas moments, kas neļauj ļaunprāšiem viegli paredzamā veidā iejaukties atjaunināšanas datos. Līdzīgus momentus iespējams jo viegli iekļaut arī sensoru datu pārraidē. Gadījumā ja pazūd tīkls, centrmezgli cenšas atkārtoti savienoties ar tīklu, un attiecīgi mērījumu ievākšana tiek apturēta, kad mērījumu saraksti aizņem tuvu kritiskajām atmiņas lielumus. Kad parādās tīkls, datu buferi tiek iztukšoti un mērījumi atsākti.

**Funkcionalitāte**: sasniedzām visas obligātās funkcijas, bet atmetām 3d vizualizāciju.

Sistēma atbilst tiem standartiem, kuru atbilstību ir deklarējuši attiecīgo iekārtu ražotāji. Analogajam mēram ir iekļauta rezerve gadījumiem kad strāva būtu virs 20mA, pie tam centrmezglam ir sava iekšējā aizsardzība pret īssavienojumiem.

**Uzticamības**:

Sistēma pārbaudīti nodrošina savas funkcijas, tomēr ir samērā plašas izaugsmes iespējas.

Kā jau pieminēts, ir aizsardzība pret īssavienojumiem un rezerve augstākām strāvām. Tāpat jau minēts par tīkla darbības atjaunošanu.

**Lietojamības**:
Metadatu ievade ir attēlota ar pārbaudīto datatables saskarni, tāpat lietotāja grafiki ar pārbaudīto Grafana saskarni.
Mūsuprāt grafiki ir daudz pievilcīgāki par sākotnējo matplotlib versiju.

**Efektivitātes**:
Sistēma pēc ielādes ļauj responsīvi kārtot, šķirot metadatus. Ielādes laiku gan neizdevās uzlabot, jo pēc python3 atjaunināšanas kešošanai piedāvā tikai memcached vai redis, proti ārējus risinājumus.

Mikrokontrolieru atmiņa tiek lietota maksimālā līmenī, kā redzams OUT OF MEMORY video.

**Uzturamības**:
Kods ir samērā viegli un mazāk kā stundas laikā saslēdzams ar jebkuru centrmezglu, kas spēj darbināt micropython, jo mainās tikai porti un varbūt LED specifika.
 
**Kustināmības (Portability)**:
Tāpat ir viegli paplašināmi metadati un pievienojami jauni objekti pēc nepieciešamības
