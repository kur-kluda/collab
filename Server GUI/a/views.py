from django.shortcuts import render
import os
from a.utils import show_db_matplot
from a.utils import show_db_matplot_hum_date
from a.utils import show_db_matplot_temp_date
from a.utils import show_db_matplot_hum_date1
from a.utils import show_db_matplot_temp_date1
from a.utils import show_db_matplot_co2_date
from a.utils import show_db_matplot_tvoc_date
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.utils.encoding import smart_str

def dbplot(req):
    errorText=""
    if req.method =='GET':
        wordcloud = show_db_matplot([])  
        
        view_model = {
        'errorText': errorText,
        'wordcloud': wordcloud
        }
        return render(req, 'index1.html', view_model)


def dbplot_date(req):
    errorText=""
    if req.method =='GET':
        wordcloud = show_db_matplot_hum_date([]) 
        wordclouda = show_db_matplot_temp_date([])
        wc1 = show_db_matplot_hum_date1([]) 
        wc1a = show_db_matplot_temp_date1([]) 
        wc2 = show_db_matplot_co2_date([]) 
        wc2a = show_db_matplot_tvoc_date([]) 
        
        view_model = {
        'errorText': errorText,
        'wordcloud1': wordcloud,
        'wordcloud': wordclouda,
        'wordcloud1a': wc1,
        'wordclouda': wc1a,
        'wordcloud2': wc2,
        'wordcloud2a': wc2a
        }
        return render(req, 'index1.html', view_model)


def view_text(r, file_name):
   file_path = 'filez/' + file_name
   #response = HttpResponse(open(file_path, 'rb').read(), content_type='application/force-download')
#   response = HttpResponse(open(file_path, 'rb').read(), content_type='text/plain')
   #response = HttpResponse(open(file_path, 'rb').read(), content_type='text/html; charset=utf-8')
   
#response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#   return response
   view_model = {
   'fl': open(file_path, 'r', encoding='utf-8').read(),
   }
   return render(r, 't.html', view_model)

