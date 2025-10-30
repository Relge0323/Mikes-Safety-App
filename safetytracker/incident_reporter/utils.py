from .models import Notification
from users.models import Profile

def create_notification(user, incident, message, notification_type):
    """
    Create a notification for a user.
    
    Args:
        user (User): The user to notify.
        incident (Incident): The incident related to the notification.
        message (str): The notification message.
        notification_type (str): Type of notification.
    """
    Notification.objects.create(
        user = user,
        incident = incident,
        message = message,
        notification_type = notification_type
    )

def notify_managers_new_incident(incident):
    """
    Notify all managers when a new incident is created.
    
    Args:
        incident (Incident): The newly created incident.
    """
    managers = Profile.objects.filter(role='manager').select_related('user')
    
    for manager_profile in managers:
        create_notification(
            user = manager_profile.user,
            incident = incident,
            message = f"New incident reported: {incident.title}",
            notification_type = 'new_incident'
        )

def notify_reporter_status_change(incident, old_status, new_status):
    """
    Notify the reporter when incident status changes.
    
    Args:
        incident (Incident): The incident that changed status.
        old_status (str): The previous status.
        new_status (str): The new status.
    """
    if incident.reporter:
        create_notification(
            user = incident.reporter,
            incident = incident,
            message = f"Your incident '{incident.title}' status changed from {incident.get_status_display()} to {dict(incident.STATUS_CHOICES)[new_status]}",
            notification_type = 'status_change'
        )

def notify_manager_assignment(incident, manager):
    """
    Notify a manager when they are assigned to an incident.
    
    Args:
        incident (Incident): The incident being assigned.
        manager (User): The manager being assigned.
    """
    create_notification(
        user = manager,
        incident = incident,
        message = f"You have been assigned to incident: {incident.title}",
        notification_type = 'assigned'
    )