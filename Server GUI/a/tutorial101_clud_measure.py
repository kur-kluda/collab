from django import forms
from django.urls import reverse  
from a.models import MeasureMeta  
from django.contrib.auth.decorators import login_required

class MeasureMetaForm(forms.ModelForm):  
    class Meta:  
        model = MeasureMeta  
        fields = [
'measurement',
'range_low',
'range_high',
'range_step',
] 
        labels={
#'nr': 'nr',
'measurement': 'measurement',
'range_low': 'range_low',
'range_high': 'range_high',
'range_step': 'range_step',
}   

from django.shortcuts import render, redirect   
@login_required
def create(request):  
    errorText=None
    if request.method == "POST":  
        form = MeasureMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                new_msr = form.save()  
                return index(request=request,
                                success=f"<p style='font-size: larger;'>Add new Measure Meta status: <span style='color:green'>OK</span> .:. {new_msr.get_measurement_display()} .:. {new_msr.range_low} : {new_msr.range_high} @ {new_msr.range_step}</p>")
                return redirect(reverse('clud_index'),
                                success=f"<p style='font-size: larger;'>Add new Measure Meta status: <span style='color:green'>OK</span> With {request.POST['measurement']} .:. {request.POST['range_low']} : {request.POST['range_high']}</p>"
                                ) 
            except Exception as ex:  
                errorText= f"Exception: {ex}"
                pass
        else:
            errorText= f"invalid form {form.errors}"
    else:  
        form = MeasureMetaForm()  
    return render(request,'tutorial101_clud_create.html',{'form':form,
                                                          "errorText": errorText,
                                                           "ispost": True if request.POST else False,})  
@login_required 
def index(request, **kwargs):  
    syccess = kwargs.get("success")
    o_MeasureMetas = MeasureMeta.objects.all()  
    return render(request,"tutorial101_clud_list.html",{'MeasureMetas':o_MeasureMetas,
                                                        'prevMSG': syccess})  
@login_required 
def update(request, measurement, range_low, range_high, range_step):
    if request.method == "POST":   
        o_MeasureMeta = MeasureMeta.objects.get(measurement=measurement, range_low=range_low, range_high=range_high, range_step=range_step)  
        form = MeasureMetaForm(request.POST, instance = o_MeasureMeta)  
        if form.is_valid():  
            form.save()  
            return index(request=request,
                         success= f"<p style='font-size: larger;'>Update Measure Meta status: <span style='color:green'>OK</span> .:. {o_MeasureMeta.get_measurement_display()} .:. {range_low} : {range_high} @ {range_step}</p>") 
            return redirect(reverse("clud_index"), 
                            success= f"<p style='font-size: larger;'>Update Measure Meta status: <span style='color:green'>OK</span> With {measurement} .:. {range_low} : {range_high}</p>") 
    else:
         o_MeasureMeta = MeasureMeta.objects.get(measurement=measurement, range_low=range_low, range_high=range_high, range_step=range_step) 
         form = MeasureMetaForm(instance= o_MeasureMeta)
    return render(request, 'tutorial101_clud_update.html', {'MeasureMeta': o_MeasureMeta,
                                                                  'form': form,
                                                                  "errorText": f"invalid form {form.errors}",
                                                                  "ispost": True if request.POST else False,})  
@login_required     
def destroy(request, measurement, range_low, range_high, range_step):  
    o_MeasureMeta = MeasureMeta.objects.get(measurement=measurement, range_low=range_low, range_high=range_high, range_step=range_step)  
    mdis = o_MeasureMeta.get_measurement_display()
    o_MeasureMeta.delete()  
    return index(request=request,
                    success=f"<p style='font-size: larger;'>Delete Measure Meta status: <span style='color:green'>OK</span> .:. {mdis} .:. {range_low} : {range_high} @ {range_step}</p>")  
    return redirect(reverse('clud_index'), 
                    success=f"<p style='font-size: larger;'>Delete Measure Meta status: <span style='color:green'>OK</span> With {measurement} .:. {range_low} : {range_high}</p>")  