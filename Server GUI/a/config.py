from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import socket
from django.contrib.auth.decorators import login_required

config_yaml = {
	"s_1": ("127.0.0.1", 911), 
	"s_2": ("jtag.me", 912), 
}
all_sensors = range(1,3)

@login_required
def config(r):
	errorText=None	
	if r.method == 'POST':
		data = r.POST
		for i in all_sensors:
			try:			
				intr = data.get("measure_all_interval_"+str(i))
				if int(intr) > 0:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect(config_yaml.get("s_"+str(i)))
					s.send(("GET /?"+str(int(intr)^ord('c'))+" HTTP1.1").encode())
					s.close()
			except Exception as e:
				errorText=str(errorText) + "\nServer "+str(i)+": "+ str(e)
	view_model = {
	'errorText': errorText,
	'range': all_sensors
	}
	return render(r, 'config.html', view_model)