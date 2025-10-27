from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from .models import Incident, Notification
from django.contrib.auth.decorators import login_required
from users.decorators import manager_required
from . import forms
from .utils import notify_managers_new_incident, notify_reporter_status_change, notify_manager_assignment
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import messages

def incident_list(request):
    """
    Display a list of all incidents with optional filtering and search.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'incident_list.html' with filtered incidents.
    """
    incidents = Incident.objects.all().order_by('-date')
    filter_form = forms.IncidentFilterForm(request.GET)
    
    # Apply filters if form is valid
    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        status = filter_form.cleaned_data.get('status')
        reporter = filter_form.cleaned_data.get('reporter')
        assigned_to = filter_form.cleaned_data.get('assigned_to')
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        
        if search:
            incidents = incidents.filter(
                Q(title__icontains=search) | Q(body__icontains=search)
            )
        
        if status:
            incidents = incidents.filter(status=status)
        
        if reporter:
            incidents = incidents.filter(reporter=reporter)
        
        if assigned_to:
            incidents = incidents.filter(assigned_to=assigned_to)
        
        if date_from:
            incidents = incidents.filter(date__gte=date_from)
        
        if date_to:
            # Add one day to include the entire end date
            date_to_end = datetime.combine(date_to, datetime.max.time())
            incidents = incidents.filter(date__lte=date_to_end)
    
    context = {
        'incident': incidents,
        'filter_form': filter_form,
        'total_count': incidents.count(),
    }
    
    return render(request, 'incident_reporter/incident_list.html', context)

def incident_page(request, slug):
    """
    Display the details of a single incident identified by its slug.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The URL-friendly slug identifying the incident.

    Returns:
        HttpResponse: Rendered 'incident_page.html' template with the incident data.

    Raises:
        Http404: If no Incident exists with the given slug.
    """
    incident = get_object_or_404(Incident, slug=slug)
    return render(request, 'incident_reporter/incident_page.html', {'incident':incident})

@login_required(login_url='/users/login/')
def incident_new(request):
    """
    Handle the creation of a new incident report.

    Only accessible to authenticated users. If the request is POST,
    the form data is validated and a new Incident is created and saved
    with the current user as the reporter. On success, shows a success
    message and presents a fresh form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'incident_new.html' template with the
                      incident creation form.
    """
    if request.method == 'POST':
        form = forms.CreateIncident(request.POST, request.FILES)
        if form.is_valid():
            newincident = form.save(commit=False)
            newincident.reporter = request.user
            newincident.save()
            
            # Notify all managers about the new incident
            notify_managers_new_incident(newincident)
            
            # Show success message
            messages.success(request, f'Incident "{newincident.title}" has been reported successfully. A manager will review it soon.')
            
            # Redirect to fresh form (employees stay on this page)
            return redirect('incident:new-incident')
    else:
        form = forms.CreateIncident()
    return render(request, 'incident_reporter/incident_new.html', {'form': form})

@manager_required(redirect_url='/incident_reporter/')
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
    old_status = incident.status
    old_assigned_to = incident.assigned_to
    
    if request.method == 'POST':
        form = forms.UpdateIncidentStatus(request.POST, instance=incident)
        if form.is_valid():
            updated_incident = form.save()
            
            # Notify reporter if status changed
            if old_status != updated_incident.status:
                notify_reporter_status_change(updated_incident, old_status, updated_incident.status)
            
            # Notify manager if they were newly assigned
            if updated_incident.assigned_to and updated_incident.assigned_to != old_assigned_to:
                notify_manager_assignment(updated_incident, updated_incident.assigned_to)
            
            messages.success(request, f'Incident status updated successfully.')
            return redirect('incident:page', slug=slug)
    else:
        form = forms.UpdateIncidentStatus(instance=incident)
    
    return render(request, 'incident_reporter/incident_update_status.html', {
        'form': form,
        'incident': incident
    })

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
    
    # Basic stats
    stats = {
        'total': incidents.count(),
        'new': incidents.filter(status='new').count(),
        'in_progress': incidents.filter(status='in_progress').count(),
        'resolved': incidents.filter(status='resolved').count(),
        'closed': incidents.filter(status='closed').count(),
    }
    
    # Get incidents by priority
    new_incidents = incidents.filter(status='new').order_by('-date')[:5]
    in_progress_incidents = incidents.filter(status='in_progress').order_by('-date')[:5]
    
    # Get incidents assigned to current manager
    my_assigned = incidents.filter(assigned_to=request.user).exclude(status='closed')
    
    # Recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_incidents = incidents.filter(date__gte=seven_days_ago).count()
    
    # Incidents by reporter (top 5)
    top_reporters = (
        incidents.values('reporter__username')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    
    context = {
        'stats': stats,
        'new_incidents': new_incidents,
        'in_progress_incidents': in_progress_incidents,
        'my_assigned': my_assigned,
        'recent_incidents': recent_incidents,
        'top_reporters': top_reporters,
    }
    
    return render(request, 'incident_reporter/manager_dashboard.html', context)

@login_required(login_url='/users/login/')
def my_incidents(request):
    """
    Display incidents reported by the current user.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Rendered template with user's incidents.
    """
    incidents = Incident.objects.filter(reporter=request.user).order_by('-date')
    
    context = {
        'incident': incidents,
        'total_count': incidents.count(),
    }
    
    return render(request, 'incident_reporter/my_incidents.html', context)

@login_required(login_url='/users/login/')
def notifications_list(request):
    """
    Display all notifications for the current user.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Rendered notifications list.
    """
    notifications = Notification.objects.filter(user=request.user)
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    return render(request, 'incident_reporter/notifications.html', context)

@login_required(login_url='/users/login/')
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read and redirect to the incident page.
    
    Args:
        request (HttpRequest): The HTTP request object.
        notification_id (int): The ID of the notification to mark as read.
    
    Returns:
        HttpResponse: Redirect to incident page.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('incident:page', slug=notification.incident.slug)

@login_required(login_url='/users/login/')
def mark_all_notifications_read(request):
    """
    Mark all notifications for the current user as read.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Redirect to notifications page.
    """
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return redirect('incident:notifications')