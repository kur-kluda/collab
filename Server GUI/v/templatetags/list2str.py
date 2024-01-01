from django import template
register = template.Library()

@register.filter(name='list2str')
#def getmeta(i):
def list2str(l: list):
	if(l is None): return "<b>error fetching list</b>"
	if(len(l) == 1): return str(l[0])
	answ = ""
	for i in range(len(l)-1):
		print(i)
		answ = answ + str(l[i])+ ", "
	print(answ)
	answ = answ + str(l[len(l)-1])
	print(f"bf ret: {answ}")
	return answ