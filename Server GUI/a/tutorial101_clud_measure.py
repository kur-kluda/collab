from django import forms
from django.urls import reverse  
from a.models import MeasureMeta  
class MeasureMetaForm(forms.ModelForm):  
    class Meta:  
        model = MeasureMeta  
        fields = [
'measurement',
'range_low',
'range_high',
] 
        labels={
#'nr': 'nr',
'measurement': 'measurement',
'range_low': 'range_low',
'range_high': 'range_high',
}   

from django.shortcuts import render, redirect   
 
def create(request):  
    if request.method == "POST":  
        form = MeasureMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect(reverse('clud_index'),
                                success=f"<p style='font-size: larger;'>Add new Measure Meta status: <span style='color:green'>OK</span> With id {form.nr}</p>"
                                ) 
            except:  
                pass
    else:  
        form = MeasureMetaForm()  
    return render(request,'tutorial101_clud_create.html',{'form':form})  
 
def index(request, **kwargs):  
    syccess = kwargs.get("success")
    o_MeasureMetas = MeasureMeta.objects.all()  
    return render(request,"tutorial101_clud_list.html",{'MeasureMetas':o_MeasureMetas,
                                                        'prevMSG': syccess})  
 
def update(request, nr):
    if request.method == "POST":   
        o_MeasureMeta = MeasureMeta.objects.get(nr=nr)  
        form = MeasureMetaForm(request.POST, instance = o_MeasureMeta)  
        if form.is_valid():  
            form.save()  
            return redirect(reverse('clud_index'), 
                            success=f"<p style='font-size: larger;'>Update Measure Meta status: <span style='color:green'>OK</span> With id {nr}</p>") 
    else:
         o_MeasureMeta = MeasureMeta.objects.get(nr=nr) 
         form = MeasureMetaForm(instance= o_MeasureMeta)
    return render(request, 'tutorial101_clud_update.html', {'MeasureMeta': o_MeasureMeta,
                                                                  'form': form,
                                                                  "errorText": f"invalid form {form.errors}",
                                                                  "ispost": True if request.POST else False,})  
     
def destroy(request, nr):  
    o_MeasureMeta = MeasureMeta.objects.get(nr=nr)  
    o_MeasureMeta.delete()  
    return redirect(reverse('clud_index'), 
                    success=f"<p style='font-size: larger;'>Delete Measure Meta status: <span style='color:green'>OK</span> With id {nr}</p>")  