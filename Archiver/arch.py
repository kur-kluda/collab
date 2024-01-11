import gzip
import mysql
from datetime import datetime
import mysql.connector
import json
import dateutil.relativedelta
import pandas as pd
#no need to tie to python specific serializer.
import csv
import os
#select table_name from information_schema...
DB_COUNT = 5
CONFIG_LIMIT="0m 15d 0h 0M 0s"
error_log_folder="error_log"
__DEL_DB_RECORDS__ = os.environ.get("KURKLUDA_DEL_DB")
__DEL_ARCHIVE_RECORDS__ = os.environ.get("KURKLUDA_DEL_ARC")
print(f"delete from Database: {__DEL_DB_RECORDS__} \ndelete from archives: {__DEL_ARCHIVE_RECORDS__}")
__PATH_TO_ARCHIVES__ = "./zipp"

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

def getDiffs_via(d: datetime, dfrom: datetime, dto: datetime) -> datetime:
      return d - dateutil.relativedelta.relativedelta(dto, dfrom)

def archive_db(i: int, refdate: datetime, cur: object):
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. loading table s_{str(i)} records <= {refdate.strftime("%Y-%m-%d %H:%M:%S")} ...')
    sql = "SELECT * FROM `s_"+str(i)+"` WHERE `rcv` <= %(refdate)s ORDER BY `time` ASC"
    #Could not process parameters: str(2023-12-02 16:47:44), it must be of type list, tuple or dict
    val = {"refdate": refdate.strftime('%Y-%m-%d %H:%M:%S')}
    cur.execute(sql, val)
    result = cur.fetchall()
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. starting to archive {len(result)} records')
    if not os.path.exists(os.path.join(__PATH_TO_ARCHIVES__, str(i))): 
        os.makedirs(os.path.join(__PATH_TO_ARCHIVES__, str(i)))
    with gzip.open(os.path.join(os.path.join(__PATH_TO_ARCHIVES__, str(i))+"/"+refdate.strftime('%Y-%m-%d_%H-%M-%S')+"_s_"+str(i)+'.gz'), 'at') as zipp:
        csvw = csv.writer(zipp)
        csvw.writerows(result)
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. archived {len(result)} records')

def delete_from_archives(i: int, refdate: datetime):
      print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. Deleting from s_{str(i)} archives if <= {refdate.strftime("%Y-%m-%d %H:%M:%S")} ...')
      nowdir = os.path.join(__PATH_TO_ARCHIVES__, str(i))
      if not os.path.exists(nowdir):
            print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. invalid path {nowdir}')
            return
      for f in os.listdir(nowdir):
            if(f.endswith(".gz")):
                df = pd.read_csv(nowdir+"/"+f, compression='gzip')
                #safeguard datetime
                df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1])
                newset = df[df.iloc[:, 1] > refdate]
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. legth before: {len(df)} after: {len(newset)}')
                newset.to_csv(nowdir+"/"+f, index=False, compression='gzip')
                print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. deleted exceess records, now: {len(newset)}' )


def getJobList() -> dict:
      print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. Fetching job list from meta database...')
      with open('db_meta.yaml', 'r') as f: 
        cfg_meta = json.load(f)
        db = mysql.connector.connect(
                port = cfg_meta["db"]["port"],
                host=cfg_meta["db"]["host"],
                user=cfg_meta["db"]["user"],
                password=cfg_meta["db"]["password"],
                database=cfg_meta["db"]["database"]
            )
        cur = db.cursor() 
        cur.execute("SELECT `nr`, `archiv_t_comp`, `archiv_t_del` FROM `a_sensormeta` Where `is_real`=1")
        result = cur.fetchall()
        answer = {}
        #unbox(answer) as list
        for r in result:
              answer[r[0]] = (r[1], r[2])
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} .::. Fetched {len(answer)} relevant sensors.')
        return answer

def doJob(nums: dict):
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
        #refdate=getDiffs(datetime.now())
        for i in nums.keys():
            try:
                refdate = getDiffs_via(datetime.now(), datetime.utcfromtimestamp(0), nums[i][0])
                refdate_del = getDiffs_via(datetime.now(), datetime.utcfromtimestamp(0), nums[i][1])
                #smoke test whether there are any old records..
                cur.execute("SELECT `rcv` FROM `s_"+str(i)+"` ORDER BY `time` ASC LIMIT 1")
                result = cur.fetchall()
                if(result[0][0] <= refdate):
                        archive_db(i, refdate, cur)
                #TODO : unarchive and undump to temp db and delete and then arhchive and finally delete initial archive
                if(__DEL_DB_RECORDS__):
                    print(f"DELETING records before {refdate.strftime('%Y-%m-%d %H:%M:%S')} from database..")
                    sql = "DELETE FROM `s_"+str(i)+"` WHERE `rcv` <= %(refdate)s ORDER BY `time` ASC"
                    cur.execute(sql)
                    db.commit()
                if(__DEL_ARCHIVE_RECORDS__):
                    print(f"DELETING records before {refdate.strftime('%Y-%m-%d %H:%M:%S')} from archives..")
                    delete_from_archives(i, refdate_del)

            except Exception as e:
                print(f"Error at {i}: {e}")
                if not os.path.exists(error_log_folder): 
                        os.makedirs(error_log_folder)
                with open(error_log_folder+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f:
                    f.write(str(e))
    except Exception as e:
        print(f"Error at connect: {e}")
        if not os.path.exists(error_log_folder): 
                os.makedirs(error_log_folder)
        with open(error_log_folder+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f:
            f.write(str(e))
    finally:
        if (db.is_connected()):
            try:
                db.close()
            except Exception as e:
                print(f"Error at finally: {e}")
                if not os.path.exists('error_log'): 
                        os.makedirs('error_log')
                with open(error_log_folder+'/'+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"_error.log", 'a') as f:
                    f.write(str(e))

if __name__== '__main__':
	doJob(getJobList())
