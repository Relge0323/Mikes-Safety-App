from django.shortcuts import render, redirect
from .models import Incident
from django.contrib.auth.decorators import login_required
from . import forms

def incident_list(request):
    incident = Incident.objects.all().order_by('-date')
    return render(request, 'incident_reporter/incident_list.html', {'incident':incident})

def incident_page(request, slug):
    incident = Incident.objects.get(slug=slug)
    return render(request, 'incident_reporter/incident_page.html', {'incident':incident})

@login_required(login_url='/users/login/')
def incident_new(request):
    if request.method == 'POST':
        form = forms.CreateIncident(request.POST, request.FILES)
        if form.is_valid():
            newincident = form.save(commit=False)
            newincident.reporter = request.user
            newincident.save()
            return redirect('incident:list')
    else:
        form = forms.CreateIncident()
    return render(request, 'incident_reporter/incident_new.html', {'form': form})