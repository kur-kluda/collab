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

#TODO: merge these plot functions in one more general purpose plot as only parameters change...
def show_db_matplot(data: Optional[list]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
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
 		cur.execute("SELECT `1`, `2` FROM `s_1` ORDER BY rcv DESC LIMIT 50")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel('temperatura')
 		ax.set_ylabel('r. mitrums')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None

def show_db_matplot_hum_date(data: Optional[list]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
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
 		cur.execute("SELECT `time`, `2` FROM `s_1` ORDER BY rcv DESC LIMIT 50")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel('laiks GMT+0')
 		ax.set_ylabel('r. mitrums')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None

def show_db_matplot_temp_date(data: Optional[list]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
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
 		cur.execute("SELECT `time`, `1` FROM `s_1` ORDER BY rcv DESC LIMIT 50")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel('laiks GMT+0')
 		ax.set_ylabel('temperatura')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None


def show_db_matplot_co2_date(data: Optional[list]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
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
 		cur.execute("SELECT `time`, `1` FROM `s_2` ORDER BY rcv DESC LIMIT 50")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel('laiks GMT+0')
 		ax.set_ylabel('co2 ppm')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None


def show_db_matplot_tvoc_date(data: Optional[list]) -> Optional[Image.Image]:
	"""Convert matplotlib data to image."""
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
 		cur.execute("SELECT `time`, `2` FROM `s_2` ORDER BY rcv DESC LIMIT 50")
 		result = cur.fetchall()
 		#print(result)
 		db.close()
 		fig, ax = plt.subplots() 
 		plt.scatter(*zip(*result))
 		#plt.imshow(list, interpolation="bilinear")
 		#plt.axis("off")
 		ax.set_xlabel('laiks GMT+0')
 		ax.set_ylabel('tvoc ppm')
 		image = io.BytesIO()
 		plt.savefig(image, format="png")
 		image.seek(0)
 		string = base64.b64encode(image.read())
 		image_64 = "data:image/png;base64," +   urllib.parse.quote_plus(string)
 		return image_64
	except ValueError:
		return None

