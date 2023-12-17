from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import socket

def config(r):
	errorText=None	
	if r.method == 'POST':
		try:		
			data = r.POST
			intr = data.get("measure_all_interval")
			if int(intr) > 0:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect(("127.0.0.1", 911))
				s.send(("GET /?"+str(int(intr)^ord('c'))+" HTTP1.1").encode())
				s.close()
		except Exception as e:
			errorText=str(e)
	view_model = {
	'errorText': errorText
	}
	return render(r, 'config.html', view_model)