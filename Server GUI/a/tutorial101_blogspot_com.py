from django import forms  
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
        widgets = {
            #'nr':,
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
        

from django.shortcuts import render, redirect   
 
# Create your views here.  
def addnew(request):  
    if request.method == "POST":  
        form = SensorMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('/')  
            except:  
                pass
    else:  
        form = SensorMetaForm()  
    return render(request,'tutorial101_blogspot_com_index.html',{'form':form})  
 
def index(request):  
    o_SensorMetas = SensorMeta.objects.all()  
    return render(request,"tutorial101_blogspot_com_show.html",{'SensorMetas':o_SensorMetas})  
 
def edit(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    return render(request,'tutorial101_blogspot_com_edit.html', {'SensorMeta':o_SensorMeta})  
 
def update(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    form = SensorMetaForm(request.POST, instance = o_SensorMeta)  
    if form.is_valid():  
        form.save()  
        return redirect("/")  
    return render(request, 'tutorial101_blogspot_com_edit.html', {'SensorMeta': o_SensorMeta})  
     
def destroy(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    o_SensorMeta.delete()  
    return redirect("/")  