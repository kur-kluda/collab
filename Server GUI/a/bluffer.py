from django.shortcuts import render
from django.template import loader
from django.http import request


#def gen_recs(n: int):
#    for i in range(n):
#        rec = 


def render_bluff(r: request):
    g = r.GET.get("s")
    if(g):
        if(str(g).lower()=="django"):
            num=r.GET.get("n", '-200')
            try:
                num = int(num)
            except ValueError:
                num = 0
            if(num==-200 or num <1):
                g = "show me the <b>n</b>umber bro.."
            else:
                g= f"{num} smart monkeys has been dispatched. Come again."
        else:
            g = None
    view_model = {
        'is_ok': g
    }
    return render(r, 'bluffer.html', view_model)