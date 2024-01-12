Mūsu komanda bija izvēlējusies veidot projektu Universitātes gaisa kvalitātes pārvaldības sistēma.
Lai gan mūsu komandā bija pamanāmi cilvēki ar ideālistiskiem skatījumiem, tomēr jāņem vērā, ka nav dzirdēts par plašai publikai brīvi pieejamiem nemirstības risinājumiem, kas nozīmē, ka projekta izstrādei ir tikai neliels laika resurss, kas nozīmē, ka jākoncentrējas uz MVP sasniegšanu, nevis jāiedziļinās dažādos interesantās blakusnodarbēs kā absolūtās drošības meklējumi, neskaitāmu interfeisu izmēģināšana un tamlīdzīgi.

Rezultātā ieguvām mūsuprāt ievērojami dzīvotspējīgu, pietiekami ērti lietojamu un visnotaļ viegli mērogojamu sistēmas iestrādni. Kurai nav papildus atkarība no kādas attālinātas korporācijas lēmumu mainības vai nemainības. Tātad pielietojama arī attālākos civilizācijas punktos vai sasniedzot briedumu arī citur kosmosā.

Nosakot vadlīnijas, nolēmām, ka sekošanu hype un dažādiem modes zīmoliem šeit neprioritizēsim, bet tieši pretēji - vērsīsim skatus uz pietiekami ilgi esošām sistēmām ar maksimāli iespējamo koda caurredzamību, tajā pašā laikā kā jau ļoti limitētu resursu sistēmās, neaizmirstot par resursu limitiem.

Tāpēc izvēlējāmies python, un tikai divos gadījumos: webkameras blakus mini projektā un industriālā 4-20mA standartsensora gadījumā,  lietojām c++. 
Pirmajā gadījumā jo kamerai bija kritiski nepieciešama operatīvā atmiņa, bet sensora gadījumā - jo kontrolierim ar augstākas izšķirtspējas ADC micropython netiek uzturēts, kas nozīmē ka liekot savu portu, ļoti ievērojami daudz laika aizietu mappinga, testēšanas un citos uzdevumos, kas acīmredzami nebūtu laika resursa daudzuma ziņā samērīgi ar projekta kopējo laika resursu.

Mikrokontrolieru kods ir asinhronu uzdevumu struktūrā veidots, un pat zemākā gala kontrolieris (esp32) to spēja izpildīt, pat esot uz operatīvās atmiņas pārpildes robežas.


