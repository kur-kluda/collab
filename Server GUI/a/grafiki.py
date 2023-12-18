from django.shortcuts import render
from django.template import loader

def render_templ_grafs(r):
    view_model = {}
    return render(r, 'grafiki.html', view_model)