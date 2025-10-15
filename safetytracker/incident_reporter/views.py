from django.shortcuts import render, redirect, get_object_or_404
from .models import Incident
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required

from . import forms

def incident_list(request):
    """
    Display a list of all incidents in reverse chronological order.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'incident_list.html' with all incidents.
    """
    incident = Incident.objects.all().order_by('-date')
    return render(request, 'incident_reporter/incident_list.html', {'incident':incident})

def incident_page(request, slug):
    """
    Display the details of a single incident identified by its slug.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The URL-friendly slug identifying the incident.

    Returns:
        HttpResponse: Rendered 'incident_page.html' template with the incident data.

    Raises:
        Incident.DoesNotExist: If no Incident exists with the given slug.
    """
    incident = get_object_or_404(Incident, slug=slug)
    return render(request, 'incident_reporter/incident_page.html', {'incident':incident})

@login_required(login_url='/users/login/')
def incident_new(request):
    """
    Handle the creation of a new incident report.

    Only accessible to authenticated users. If the request is POST,
    the form data is validated and a new Incident is created and saved
    with the current user as the reporter. On success, redirects to
    the incident list. For GET requests, an empty form is displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'incident_new.html' template with the
                      incident creation form, or a redirect to the
                      incident list after successful creation.
    """
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

@manager_required(redirect_url='/incident_reporter')
def incident_update_status(request, slug):
    """
    Allow managers to update the status of an incident.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The URL-friendly slug identifying the incident.
    
    Returns:
        HttpResponse: Rendered template or redirect after status update.
    """

    incident = get_object_or_404(Incident, slug=slug)

    if request.method == 'POST':
        form = forms.UpdateIncidentStatus(request.POST, instance=incident)
        if form.is_valid():
            form.save()
            return redirect('incident:page', slug=slug)
    else:
        form = forms.UpdateIncidentStatus(instance=incident)

    return render(request, 'incident_reporter/incident_update_status.html', {'form': form, 'incident': incident})


@manager_required(redirect_url='/incident_reporter/')
def manager_dashboard(request):
    """
    Display a dashboard for managers with incident statistics and filters.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Rendered manager dashboard.
    """

    incidents = Incident.objects.all()

    stats = {
        'total': incidents.count(),
        'new': incidents.filter(status='new').count(),
        'in_progress': incidents.filter(status='in_progress').count(),
        'resolved': incidents.filter(status='resolved').count(),
        'closed': incidents.filter(status='closed').count(),
    }

    # get the recent incidents by status
    new_incidents = incidents.filter(status='new')[:5]
    in_progress_incidents = incidents.filter(status='in_progress')[:5]

    context = {
        'stats': stats,
        'new_incidents': new_incidents,
        'in_progress_incidents': in_progress_incidents,
    }

    return render(request, 'incident_reporter/manager_dashboard.html', context)