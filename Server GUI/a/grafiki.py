from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required
def render_templ_grafs(r):
    view_model = {}
    return render(r, 'grafiki.html', view_model)