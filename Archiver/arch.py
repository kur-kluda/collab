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

def getDiffs(d: datetime) -> datetime:	
	sp = CONFIG_LIMIT.split(' ')
	for i in sp:
		if(i.endswith('y')):
			d = d - dateutil.relativedelta.relativedelta(years=int(i.strip('y')))
		elif(i.endswith('m')):
			d = d - dateutil.relativedelta.relativedelta(months=int(i.strip('m')))
		elif(i.endswith('d')):
			d = d - dateutil.relativedelta.relativedelta(days=int(i.strip('d')))
		elif(i.endswith('h')):
			d = d - dateutil.relativedelta.relativedelta(hours=int(i.strip('h')))
		elif(i.endswith('M')):
			d = d - dateutil.relativedelta.relativedelta(minutes=int(i.strip('M')))
		elif(i.endswith('s')):
			d = d - dateutil.relativedelta.relativedelta(seconds=int(i.strip('s')))
	return	d

def archive_db(i: int, refdate: datetime, cur: object):
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. loading table s_{str(i)} records...')
	sql = "SELECT * FROM `s_"+str(i)+"` WHERE `rcv` <= %(refdate)s ORDER BY `time` ASC"
#Could not process parameters: str(2023-12-02 16:47:44), it must be of type list, tuple or dict
	val = {"refdate": refdate.strftime('%Y-%m-%d %H:%M:%S')}
	cur.execute(sql, val)
	result = cur.fetchall()
	if not os.path.exists(refdate.strftime('%Y-%m-%d_%H-%M-%S')): 
		os.makedirs(refdate.strftime('%Y-%m-%d_%H-%M-%S'))
	with gzip.open(refdate.strftime('%Y-%m-%d_%H-%M-%S')+"/"+refdate.strftime('%Y-%m-%d_%H-%M-%S')+"_s_"+str(i)+'.gz', 'at') as zipp:
		csvw = csv.writer(zipp)
		csvw.writerows(result)
	print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. archived {len(result)} records')

def doJob():
    db = {'connected': False}
    try:
        with open('db.yaml', 'r') as f:
             cfg = json.load(f)

        db = mysql.connector.connect(
                    host=cfg["db"]["host"],
                    user=cfg["db"]["user"],
                    password=cfg["db"]["password"],
                    database=cfg["db"]["database"]
                )
        cur = db.cursor()
        refdate=getDiffs(datetime.now())
        for i in range(1, DB_COUNT+1):
            cur.execute("SELECT `rcv` FROM `s_"+str(i)+"` ORDER BY `time` ASC LIMIT 1")
            result = cur.fetchall()
            if(result[0][0] <= refdate):
                    archive_db(i, refdate, cur)
    except Exception as e:
        print(f"Error: {e}")
        if not os.path.exists('error_log'): 
                os.makedirs('error_log')
        with open(error_log+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f:
            f.write(str(e))
    finally:
        if (db.is_connected()):
            try:
                db.close()
            except Exception as e:
                print(f"Error: {e}")
                if not os.path.exists('error_log'): 
                        os.makedirs('error_log')
                with open(error_log+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f:
                    f.write(str(e))

if __name__== '__main__':
	doJob()
