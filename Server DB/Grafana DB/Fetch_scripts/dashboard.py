from secrets._secrets import tell_the_secrets
import sqlite3
import os
import re
import subprocess
from datetime import datetime

TABLE_NAME="dashboard"
s = tell_the_secrets()
print(s)

conn = sqlite3.connect(s["pathToGrafanaDB"])
os.makedirs(f"../{TABLE_NAME}", exist_ok=True)

cursor = conn.cursor()
cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
fields = cursor.fetchall()

resolver = {}
for f in fields:
	resolver[f[1]] = f[0]

def d(colname: str):
	return resolver.get(colname, "")

cursor.execute(f"SELECT * FROM {TABLE_NAME}")
records = cursor.fetchall()

conn.close()

existing_files_dict = {}
rex = re.compile(r".+_([^_\.]+)\.sql$")
#if os == win => dir *_uid* /b
#elif os == linux => ls *_uid*
for fn in os.listdir(f"../{TABLE_NAME}"):
	m = rex.match(fn)
	if m:
		print(m[1])
		fpath = os.path.join(f"../{TABLE_NAME}", fn)
		if os.path.isfile(fpath):
			existing_files_dict[m[1]] = fpath

for rec in records:
	fn = existing_files_dict.get(rec[d("uid")], False)
	if not fn: fn = os.path.join(f"../{TABLE_NAME}", rec[d("slug")] + "_" + rec[d("uid")] + ".sql" )
	print(f" currently exporting {fn}...") #ndqm or how was that called?
	with open(fn, "w") as dump:
		dump.write(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (\n")
		struct = ""
		for f in fields:
			struct += f"{f[1]} {f[2]},\n"
		dump.write(struct.rstrip(',\n'))
		dump.write(f"\n)\n\n")

		#the data:
		dump.write(f"INSERT INTO {TABLE_NAME} VALUES ({', '.join(map(repr, rec))});\n")

print(f"{TABLE_NAME} sync complete. now gitting")

os.chdir("../")

print(subprocess.check_output('git pull', shell=True))
print(subprocess.check_output('git add .', shell=True))
print(subprocess.check_output(f'git commit -m "Grafana DB :: {TABLE_NAME} sync {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"', shell=True))
print(subprocess.check_output('git push origin', shell=True) )