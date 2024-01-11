import gzip
import mysql
from datetime import datetime
import mysql.connector
import json
import dateutil.relativedelta
#no need to tie to python specific serializer.
import csv
import os
#select table_name from information_schema...
DB_COUNT = 5
CONFIG_LIMIT="0m 15d 0h 0M 0s"

def getDiffs(d: datetime) -> datetime: #Tiek definēta funkcija 'getDiffs', kas paņem 'datetime' objektu 'd' kā ievadi un atgriež modificētu 'datetime' objektu. 	
	sp = CONFIG_LIMIT.split(' ') #Tā sadala simbolu virkni 'CONFIG_LIMIT' sarakstā no simbolu apakšvirknēm, izmantojot '' jeb space kā atdalītāju. Iznākušais saraksts tiek glabāts mainīgajā 'sp'.                                                       
	for i in sp:                                                                       #for ciklā notiek iterēšana katram 'i' elementam 
		if(i.endswith('y')):                                                           #sarakstā 'sp'. for ciklā tas pārbauda beigu rakstzīmi katram elementam 'i', lai noskaidrotu vienību skaitu, proti, sekundes,
			d = d - dateutil.relativedelta.relativedelta(years=int(i.strip('y')))      #minūtes, stundas, dienas, mēnēši un gadi. Tiek izmantota 'endswith' metode, lai pārbaudītu beigu rakstzīmi. 
		elif(i.endswith('m')):                                                         #Atkarībā no laika vienības, tas paņem skaitlsko vērtību, izņemot laika vienības rakstzīmes,
			d = d - dateutil.relativedelta.relativedelta(months=int(i.strip('m')))     #izmantojot 'int(i.strip('<unit>'))' un atņem tieši tik daudz laika no pamata 'datetime' objekta 'd',
		elif(i.endswith('d')):                                                         #izmantojot 'dateutil.relativedelta.relativedelta' funkciju.
			d = d - dateutil.relativedelta.relativedelta(days=int(i.strip('d')))       #Modificētā 'datetime' objekta 'd' tiek atgriezts pēc norādīto laiku intervālu atņemšanas.
		elif(i.endswith('h')):                                                         #
			d = d - dateutil.relativedelta.relativedelta(hours=int(i.strip('h')))      #
		elif(i.endswith('M')):                                                         #
			d = d - dateutil.relativedelta.relativedelta(minutes=int(i.strip('M')))    #
		elif(i.endswith('s')):                                                         #
			d = d - dateutil.relativedelta.relativedelta(seconds=int(i.strip('s')))    #
	return	d

def archive_db(i: int, refdate: datetime, cur: object): #Tiek nodefinēta funkcija 'archive_db', kas arhivē ierakstus no datubāzes tabulas. 'i' ir integer parametrs, 'refdate' ir 'datetime' objekts, kurš pārstāv atsauces datumu. 'cur' ir datubāzes kursora objekts.  
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. loading table s_{str(i)} records...') 
	sql = "SELECT * FROM `s_"+str(i)+"` WHERE `rcv` <= %(refdate)s ORDER BY `time` ASC" #Uzbūvē SQL vaicājumu, kas atlasa visus ierakstus '*' no tabulas, kuras nosaukums ir 's_1', kur 'rcv' kolonna ir mazāka vai vienāda par norādīto datumu. Rezultāti tiek salikti ar 'time' kolonnu augošā secībā.
#Could not process parameters: str(2023-12-02 16:47:44), it must be of type list, tuple or dict
	val = {"refdate": refdate.strftime('%Y-%m-%d %H:%M:%S')} #Sagatavo parametru SQL vaicājumam, kur '%s' tiek substitēts ar formatēto simbolu virknes 'refdata'.
	cur.execute(sql, val) #Izpilda SQL vaicājumu ar dotajiem parametriem, izmantojot datubāzes kursoru.
	result = cur.fetchall() #Paņem visas rindas no izpildītā vaicājuma un glabā tos 'result' mainīgajā.
	if not os.path.exists(refdate.strftime('%Y-%m-%d_%H-%M-%S')): #Pārbauda vai direktorija, 
		os.makedirs(refdate.strftime('%Y-%m-%d_%H-%M-%S'))        #kas ir nosaukta ar formatētu atsauces datumu eksistē.
	with gzip.open(refdate.strftime('%Y-%m-%d_%H-%M-%S')+"/"+refdate.strftime('%Y-%m-%d_%H-%M-%S')+"_s_"+str(i)+'.gz', 'at') as zipp: #Arhivē paņemtos ierakstus saspiestā CSV failā, 
		csvw = csv.writer(zipp)                                                                                                       #kurš atrodas
		csvw.writerows(result)                                                                                                        #iepriekš izveidotajā direktorijā.                  
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. archived {len(result)} records') #Izvada ziņu, kas parāda laiku, datumu un sasniegto ierakstu skaitu. 

def doJob(): 
    db = {'connected': False} #Inicializē 'db' vārdnīcu ar atslēgu 'connected', kas ir iestatīts uz 'False'. Tas ir vajadzīgs, lai noteiktu vai ir datubāzes savienojums. 
    try:                                #Mēģinājumi nolasīt datubāzes konfigurācijas no
        with open('db.yaml', 'r') as f: #YAML faila ar nosaukumu 'db.yaml'. 
             cfg = json.load(f)         #Konfigurācija tiek iestatīta 'cfg' mainīgajā.

        db = mysql.connector.connect(               #Izveido savienojumu ar MySQL,
                    host=cfg["db"]["host"],         #izmantojot parametrus no konfigurācijas.
                    user=cfg["db"]["user"],         #Tas arī izveido datubāzes kursoru 'cur'
                    password=cfg["db"]["password"], #SQL vaicājumu izpildei
                    database=cfg["db"]["database"]  #
                )
        cur = db.cursor()
        refdate=getDiffs(datetime.now()) #Izsauc 'getDiffs' funkciju, lai izrēķinātu datumu, balstoties uz reāllaika datumu un laiku.
        for i in range(1, DB_COUNT+1): #Iterē tabulas noteiktā diapazonā.
            cur.execute("SELECT `rcv` FROM `s_"+str(i)+"` ORDER BY `time` ASC LIMIT 1") #Paņem pirmo 'rcv' vērtību no tagādējās tabulas.
            result = cur.fetchall()                                                     #Ja šī vērtība ir mazāka vai vienāda ar atsauces datumu,
            if(result[0][0] <= refdate):                                                #tad tā izsauks 'archive_db' funkciju,
                    archive_db(i, refdate, cur)                                         #lai arhivētu ierakstus.
    except Exception as e:                                                                            #Noķer un izvada jebkuru izņēmumu,
        print(f"Error: {e}")                                                                          #kas notiek koda izpildes laikā.
        if not os.path.exists('error_log'):                                                           #Tas arī rakstīs                               
                os.makedirs('error_log')                                                              #kļūdas ziņu kļūdu failā.
        with open(error_log+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f: #
            f.write(str(e))                                                                           #
    finally:                                                                                                  #'finally' blokā, tas pārbauda, ja datubāzes savienojums ir atvērts un tas mēģinātu aizvērtu to.
        if (db.is_connected()):                                                                               #Ja kļūda notiek aizvēršanas procesā,
            try:                                                                                              #tad tiks izvadīta kļūda un tā tiks ierakstīta kļūdas failā.
                db.close()                                                                                    #
            except Exception as e:                                                                            #
                print(f"Error: {e}")                                                                          #
                if not os.path.exists('error_log'):                                                           #
                        os.makedirs('error_log')                                                              #
                with open(error_log+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f: #
                    f.write(str(e))                                                                           #

if __name__== '__main__':
	doJob()
