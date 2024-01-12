from django import forms
from django.urls import reverse  
from a.models import HubMeta  
from django.contrib.auth.decorators import login_required

class HubMetaForm(forms.ModelForm):  
    class Meta:  
        model = HubMeta  
        fields = [
'model',
'hub',
'loc_la',
'loc_lo',
'loc_ro',
'update_interval',
'comment',
'is_real',
] 
       # exclude=["nr"]
        labels={
#'nr': 'nr',
'model': 'model',
'hub': 'Parent hub',
'loc_la': 'loc_la',
'loc_lo': 'loc_lo',
'loc_ro': 'loc_ro',
'comment': 'comment',
'is_real': 'is_real',
}

from django.shortcuts import render, redirect   
@login_required  
def create(request):  
    errorText=None
    if request.method == "POST":  
        form = HubMetaForm(request.POST)  
        if form.is_valid():  
            try:  
                newhub = form.save()  
                return index(request=request,
                                success=f"<p style='font-size: larger;'>Add new Hub Meta status: <span style='color:green'>OK</span> With id {newhub.nr}</p>")
                return redirect(reverse('crud_hub_index'),
                                success=f"<p style='font-size: larger;'>Add new Hub Meta status: <span style='color:green'>OK</span> With id {request.POST['nr']}</p>") 
            except Exception as ex: 
                errorText= f"Exception: {ex}" 
                pass
        else:
            errorText= f"invalid form {form.errors}"
    else:  
        form = HubMetaForm()  
    return render(request,'tutorial101_crud_hub_create.html',{'form':form,
                                                          "errorText": errorText,
                                                           "ispost": True if request.POST else False,})  
@login_required 
def index(request, **kwargs):  
    syccess = kwargs.get("success")
    o_HubMetas = HubMeta.objects.all()  
    return render(request,"tutorial101_crud_hub_list.html",{'HubMetas':o_HubMetas,
                                                        'prevMSG': syccess})  
@login_required
def update(request, nr):
    if request.method == "POST":   
        o_HubMeta = HubMeta.objects.get(nr=nr)  
        form = HubMetaForm(request.POST, instance = o_HubMeta)  
        if form.is_valid():  
            form.save()  
            return index(request=request,
                        success=f"<p style='font-size: larger;'>Update Hub Meta status: <span style='color:green'>OK</span> With id {nr}</p>") 
            return redirect(reverse('crud_hub_index')) 
    else:
         o_HubMeta = HubMeta.objects.get(nr=nr) 
         form = HubMetaForm(instance= o_HubMeta)
    return render(request, 'tutorial101_crud_hub_update.html', {'HubMeta': o_HubMeta,
                                                                  'form': form,
                                                                  "errorText": f"invalid form {form.errors}",
                                                                  "ispost": True if request.POST else False,})  
@login_required    
def destroy(request, nr):  
    o_HubMeta = HubMeta.objects.get(nr=nr)  
    o_HubMeta.delete()  
    return index(request=request,
                 success=f"<p style='font-size: larger;'>Delete Hub Meta status: <span style='color:green'>OK</span> With id {nr}</p>") 
    return redirect(reverse('crud_hub_index'))  