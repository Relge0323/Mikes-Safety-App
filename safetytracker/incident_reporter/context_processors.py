from .models import Notification

def unread_notifications(request):
    """
    Add unread notification count to all templates.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}