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
 
def create(request):  
    errorText=None
    if request.method == "POST":  
        form = SensorMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                new_sens = form.save()  
                return index(request=request,
                             success=f"<p style='font-size: larger;'>Add new Sensor Meta status: <span style='color:green'>OK</span> With id {new_sens.nr}</p>")
                return redirect(reverse('ciud_index'),
                                success=f"<p style='font-size: larger;'>Add new Sensor Meta status: <span style='color:green'>OK</span> With id {request.POST['nr']}</p>"
                                ) 
            except Exception as ex:  
                errorText= f"Exception: {ex}"
                pass
        else:
            errorText= f"invalid form {form.errors}"
    else:  
        form = SensorMetaForm()  
    return render(request,'tutorial101_ciud_create.html',{'form':form,
                                                          "errorText": errorText,
                                                           "ispost": True if request.POST else False,})  
 
def index(request, **kwargs):  
    syccess = kwargs.get("success")
    o_SensorMetas = SensorMeta.objects.all()  
    return render(request,"tutorial101_ciud_list.html",{'SensorMetas':o_SensorMetas,
                                                        'prevMSG': syccess})  
 
def update(request, nr):
    if request.method == "POST":   
        o_SensorMeta = SensorMeta.objects.get(nr=nr)  
        form = SensorMetaForm(request.POST, instance = o_SensorMeta)  
        if form.is_valid():  
            form.save() 
            return index(request=request,
                         success=f"<p style='font-size: larger;'>Update Sensor Meta status: <span style='color:green'>OK</span> With id {nr}</p>") 
            return redirect(reverse('ciud_index'), 
                            success=f"<p style='font-size: larger;'>Update Sensor Meta status: <span style='color:green'>OK</span> With id {nr}</p>") 
    else:
         o_SensorMeta = SensorMeta.objects.get(nr=nr) 
         form = SensorMetaForm(instance= o_SensorMeta)
    return render(request, 'tutorial101_ciud_update.html', {'SensorMeta': o_SensorMeta,
                                                                  'form': form,
                                                                  "errorText": f"invalid form {form.errors}",
                                                                  "ispost": True if request.POST else False,})  
     
def destroy(request, nr):  
    o_SensorMeta = SensorMeta.objects.get(nr=nr)  
    o_SensorMeta.delete()  
    return index(request=request,
                success=f"<p style='font-size: larger;'>Delete Sensor Meta status: <span style='color:green'>OK</span> With id {nr}</p>")  
    return redirect(reverse('ciud_index'), 
                    success=f"<p style='font-size: larger;'>Delete Sensor Meta status: <span style='color:green'>OK</span> With id {nr}</p>")  