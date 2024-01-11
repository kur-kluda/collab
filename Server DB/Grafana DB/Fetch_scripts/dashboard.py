from secrets._secrets import tell_the_secrets
import sqlite3
import os
import re
import subprocess
from datetime import datetime

TABLE_NAME="dashboard" # Tiks izveidots mainīgais ar nosaukumu 'TABLE_NAME' un tas tiks piesaistīts simbolu virknes vērtībai 'dashboard'.
s = tell_the_secrets() # Tiks izsaukta funkcija 'tell_the_secrets()' un piesaista rezultātu mainīgajam 's'.
print(s) # Tiks izvadīta vērtība no mainīgā 's'. Izvade ir atkarīga no tā, ko funkcija 'tell_the_secrets()' atgriezīs.

conn = sqlite3.connect(s["pathToGrafanaDB"]) # Izveido savienojumu ar SQLite datubāzi, izmantojot metodi 'connect' no 'sqlite3' moduļa. Informācija par Datubāzes ceļu tiek paņemta no 'š' direktorijas, izmantojot atslēgu '"pathTOGrafanaDB"'. Mainīgajam 'conn' ir savienojums ar SQLite datubāzi.  
os.makedirs(f"../{TABLE_NAME}", exist_ok=True) # Funkcija 'os.' izveido apakšdirektoriju ar nosaukumu 'dashboard' direktorijā. Parametrs 'exist_ok=True' nodrošina to, ka funkcija nesignalizēs par kļūdu, ka direktorija jau eksistē.

cursor = conn.cursor() # Tiks izveidots kursora objekts, izmantojot metodi 'cursor()', kad ir savienojums ar SQLite datubāzi, ko nodrošina 'conn', Kursors tiek izmantots, lai izpildītu SQL vaicājumus un izgūtu rezultātus no datubāzes.
cursor.execute(f"PRAGMA table_info({TABLE_NAME})") # Izpilda SQL vaicājumu, izmantojot kursoru. Tas paņems informāciju par kolonnām no tabulas. 'table_info' atgriezīs norādīto rindu katrai kolonnai norādītajā tabulā ar detalizētu informāciju par katru kolonnu.
fields = cursor.fetchall() # Izgūst visas rindas no iepriekš izpildītā SQL vaicājuma un glabā tās mainīgajā 'field'.

resolver = {} # Inicializē tukšu direktoriju ar nosaukumu 'rsolver'.
for f in fields: # for cikls, kas iterē caur katru elementu 'f' sarakstā 'fields', kur katrs elements pārstāv informāciju par kolonnu no tabulas.
	resolver[f[1]] = f[0] # Elements 'f[1]' atbildīs otrajam elementam no masīva 'f', kas visbiežāk ir kolonnas vārds. Elements 'f[0]' atbildīs pirmajam elementam masīvā, kas ir indeksa identifikators sasaistītajai kolonnai. Pēc tam cikls izveido ieeju 'resolver' direktorijā atslēga ir kolonnas vārds 'f[1]' un vērtība ir sasaistītais indekss 'f[0]'. 

def d(colname: str): # Tiks definēta funkcija 'd', kas ņems vienu parametru 'colname' no simbolu virknes..
	return resolver.get(colname, "") # Tiks izmantota 'get()' metode 'resolver' direktorijas, lai paņemtu vērtību, kas ir sasaistīta ar norādīto 'colname'.Ja 'colname' tiks atrasta direktorijā, tad sasaistītā vērtība tiek atgriezta, ja nē, tad funkcija atgriezīs tukšu simbolu virkni '""', kā pamata vērtību.

cursor.execute(f"SELECT * FROM {TABLE_NAME}") # Tiks izmantota 'execute' metode no SQLite kurura 'cursor', lai izpildītu SQL vaicājumu. SQL vaicājums satur 'SELECT * FROM' vaicājumu, kur '*' pārstāv visas kolonnas un 'TABLE_NAME' norāda tabulu, kurā vajag atlasīt visas kolonnas.
records = cursor.fetchall() # Izgūst visas rindas no visiem ierakstiem un glabā tās mainīgajā 'records'.

conn.close() # Aizver SQLite datubāzes savienojumu.

existing_files_dict = {} #T iks inicializeta direktorija ar nosaukumu 'existing_files_dict'
rex = re.compile(r".+_([^_\.]+)\.sql$") # Izveido kompilētu izteiksmes objektu, izmantojot 're.compile' funkciju.
#if os == win => dir *_uid* /b
#elif os == linux => ls *_uid*
for fn in os.listdir(f"../{TABLE_NAME}"): # Iterē caur failiem norādītajā direktorijā '../(TABLE_NAME)'. Katrā failā, tas sasaistīs faila nosaukumu ar mainīgo 'fn'
	m = rex.match(fn) # Metode 'match' tiks izmantota no kompilētās izteiksmes 'rex', lai pārbaudīitu vai faila nosaukums 'fn' atbilst ceļam, kas tika definēts ar izteiksmi. Ja tādas atbilstības nav, tad rezultāts tiks glabāts mainīgajā 'm'.
	if m: # Ja nav atbilstības, tad tas tiks izpildīts.
		print(m[1]) #Izvade
		fpath = os.path.join(f"../{TABLE_NAME}", fn) # Uzbūvē pilnu ceļu uz failu ar 'fpath', savienojot direktorijas ceļu ar faila nosaukumu.
		if os.path.isfile(fpath):                    # Tad tas pārbauda vai uzbūvētais ceļs ir sasaistīts ar failu, izmantojot 'os.path.isfile(fpath)'.
			existing_files_dict[m[1]] = fpath        # Ja tas ir fails, tad tas modificē 'existing_file_dict' direktoriju. Atslēga ir paņemta no faila nosaukuma 'm[1]' un vērtība ir pilnais ceļs uz failu 'fpath'.

for rec in records: # Tiks inicializēts cikls pār katru ierakstu 'recordings' sarakstā. 
	fn = existing_files_dict.get(rec[d("uid")], False) # Katram ierakstam, tas mēģinās paņemt informāciju par ceļu uz failu, kas ir sasaistīts ar ieraksta unikālo identifikatoru 'uid' no 'existing_files_dict'. Ja ceļš uz failu tiks atrasts, tad tas tiks sasaistīts ar mainīgo 'fn', pretējā gadījumā tas uzbūvēs pamata ceļu uz failu.
	if not fn: fn = os.path.join(f"../{TABLE_NAME}", rec[d("slug")] + "_" + rec[d("uid")] + ".sql" ) # Ja ceļš uz failu netika atrasts 'existing_files_dict', tad tiks izveidota pamata ceļš uz failu savienojot ceļu uz direktoriju '../(TABLE_NAME)' ar faila nosaukumu, balstotoes uz ierakstu 'slug' un 'uid'. 
	print(f" currently exporting {fn}...") # ndqm or how was that called?                             # Izvadīs ziņu, ka tagadējais fails tiek eksportēts.
	with open(fn, "w") as dump: # Tiks atvērts fails, kurš tika norādīts ar ceļu uz failu 'fn'. Fails tiks atvērts ar 'with' izteiksmi, kas nodrošina to, ka fails ir patiešām aizvērts pēc rakstīšanas.
		dump.write(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (\n") # Tiks uzrakstīts SQL vaicājums, lai izveidotu tabulu ar norādīto 'TABLE_NAME'. 
		struct = ""                       # for cikls iterēs pār katru lauku 'fields' sarakstā,
		for f in fields:                  # kas ietver informāciju par tabulas kolonnām. Tas uzbūvēs simbolu virkni 'string', 
			struct += f"{f[1]} {f[2]},\n" # savienojot kolonnas nosaukumu 'f[1]' un datu tipu 'f[2]' un komatu. 
		dump.write(struct.rstrip(',\n')) # uzbūvētās kolonnas definīcijas tiks ierakstītas failā. Atdalošais komats un jauna rinda tiks noņemti, lietojot 'rstrip(',\n')'.
		dump.write(f"\n)\n\n") # Aizverošās iekavas un divas jaunas līnijas tiek pievienotas, lai pabeigtu tabulas izveides vaicājumu.

		#the data:
		dump.write(f"INSERT INTO {TABLE_NAME} VALUES ({', '.join(map(repr, rec))});\n") #Tiks uzrakstīts  SQL 'INSERT' vaicājums SQL failā 'dump'.

print(f"{TABLE_NAME} sync complete. now gitting")

os.chdir("../")

print(subprocess.check_output('git pull', shell=True))
print(subprocess.check_output('git add .', shell=True))
print(subprocess.check_output(f'git commit -m "Grafana DB :: {TABLE_NAME} sync {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"', shell=True))
print(subprocess.check_output('git push origin', shell=True) )