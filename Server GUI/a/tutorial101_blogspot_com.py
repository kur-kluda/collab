from django import forms
from django.urls import reverse  
from a.models import SensorMeta  
class SensorMetaForm(forms.ModelForm):  
    class Meta:  
        model = SensorMeta  
        fields = [
'model',
'hub',
'interface',
'measurements',
'loc_la',
'loc_lo',
'loc_ro',
'comment',
'is_real',
] 
        labels={
#'nr': 'nr',
'model': 'model',
'hub': 'hub',
'interface': 'interface',
'measurements': 'measurements',
'loc_la': 'loc_la',
'loc_lo': 'loc_lo',
'loc_ro': 'loc_ro',
'comment': 'comment',
'is_real': 'is_real',
        }
"""
        widgets = {
'nr':forms.NumberInput(attrs={ 'class': 'form-control' }),
'model': forms.TextInput(attrs={ 'class': 'form-control' }),
'hub': forms.NumberInput(attrs={ 'class': 'form-control' }),
'interface':forms.NumberInput(attrs={ 'class': 'form-control' }),
'measurements':forms.TextInput(attrs={ 'class': 'form-control' }),
'loc_la':forms.NumberInput(attrs={ 'class': 'form-control' }),
'loc_lo':forms.NumberInput(attrs={ 'class': 'form-control' }),
'loc_ro':forms.NumberInput(attrs={ 'class': 'form-control' }),
'comment':forms.TextInput(attrs={ 'class': 'form-control' }),
'is_real':forms.CheckboxInput(attrs={ 'class': 'form-control' }),
      }
"""        

from django.shortcuts import render, redirect   
 
# Create your views here.  
def addnew(request):  
    if request.method == "POST":  
        form = SensorMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect(reverse('ciud_index')) 
            except:  
                pass
    else:  
        form = SensorMetaForm()  
    return render(request,'tutorial101_blogspot_com_new.html',{'form':form})  
 
def index(request):  
    o_SensorMetas = SensorMeta.objects.all()  
    return render(request,"tutorial101_blogspot_com_list.html",{'SensorMetas':o_SensorMetas})  
 
def edit(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    return render(request,'tutorial101_blogspot_com_edit.html', {'SensorMeta':o_SensorMeta})  
 
def update(request, nr):
    if request.method == "POST":   
        o_SensorMeta = SensorMeta.objects.get(nr=nr)  
        form = SensorMetaForm(request.POST, instance = o_SensorMeta)  
        if form.is_valid():  
            form.save()  
            return redirect(reverse('ciud_index')) 
    else:
         o_SensorMeta = SensorMeta.objects.get(nr=nr) 
         form = SensorMetaForm(instance= o_SensorMeta)
    return render(request, 'tutorial101_blogspot_com_edit.html', {'SensorMeta': o_SensorMeta,
                                                                  'form': form,
                                                                  "errorText": f"invalid form {form.errors}",
                                                                  "ispost": True if request.POST else False,})  
     
def destroy(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    o_SensorMeta.delete()  
    return redirect(reverse('ciud_index'))  