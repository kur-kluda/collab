import base64
import io
import os
import urllib.parse
from typing import Any, List, Optional
import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
import mysql
from datetime import datetime
import mysql.connector
import json

def show_db_plot_overlord(xcol, ycol, tablename, 
#orderby_expression, 
limit, xlabel, ylabel, data: Optional[list]) -> Optional[Image.Image]:
    orderby_expression = "rcv DESC"
	try:
 		#print(os.path.abspath('../../agr/db.yaml'))
 		with open('../../agr/db.yaml', 'r') as f:
 		#with open('db.yaml', 'r') as f:
 			cfg = json.load(f)

 		db = mysql.connector.connect(
                    host=cfg["db"]["host"],
                    user=cfg["db"]["user"],
                    password=cfg["db"]["password"],
                    database=cfg["db"]["database"]
                )
 		cur = db.cursor()
 		cur.execute(f"SELECT `{xcol}`, `{ycol}` FROM `{tablename}` ORDER BY {orderby_expression} LIMIT {limit}")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel(f'{xlabel}')
 		ax.set_ylabel(f'{ylabel}')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None
    
#DONE: merge these plot functions in one more general purpose plot as only parameters change...
def show_db_matplot(data: Optional[list]) -> Optional[Image.Image]:
    return show_db_plot_overlord("1", "2", "s_1", "50", "temperatura", "r. mitrums")

def show_db_matplot_hum_date(data: Optional[list]) -> Optional[Image.Image]:
	return show_db_plot_overlord("time", "2", "s_1", "50", "laiks GMT+0", "r. mitrums")

def show_db_matplot_temp_date(data: Optional[list]) -> Optional[Image.Image]:
	return show_db_plot_overlord("time", "1", "s_1", "50", "laiks GMT+0", "temperatura")

def show_db_matplot_co2_date(data: Optional[list]) -> Optional[Image.Image]:
	return show_db_plot_overlord("time", "1", "s_2", "50", "laiks GMT+0", "co2 ppm")

def show_db_matplot_tvoc_date(data: Optional[list]) -> Optional[Image.Image]:
	return show_db_plot_overlord("time", "2", "s_2", "50", "laiks GMT+0", "tvoc ppm")


