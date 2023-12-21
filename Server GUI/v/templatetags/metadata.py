from django import template
register = template.Library()

@register.filter(name='getmeta')
#def getmeta(i):
def getmeta(value):
	metadata = {
		1: ["DHT11 orig", "DHT22", "DHT22", "DHT11"],
		2: ["CCS811"]
	}
	l = metadata.get(value)
	if(l is None): return "<b>error fetching metadata list</b>"
	if(len(l) == 1): return l[0]
	answ = ""
	for i in range(len(l)-1):
		answ = answ + l[i]+ ", "
	answ = answ + l[len(l)-1]
	return answ


"""
{# {% for n in i|getmeta %}
{{n}} 
{% endfor %}#}
"""