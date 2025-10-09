from django.shortcuts import render
from incident_reporter.models import Incident

def home_view(request):
    """
    Render the homepage with a summary dashboard of incidents.

    Retrieves the total number of incidents and the most recent incident,
    then passes this data to the 'home.html' template for display.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered 'home.html' template with context containing:
            - total_incidents (int): Total number of incidents in the database.
            - latest_incident (Incident or None): Most recently created Incident instance, or None if no incidents exist.
    """
    total_incidents = Incident.objects.count()
    latest_incident = Incident.objects.order_by('-date').first()
    context = {
        'total_incidents': total_incidents,
        'latest_incident': latest_incident
    }
    return render(request, 'home.html', context)
