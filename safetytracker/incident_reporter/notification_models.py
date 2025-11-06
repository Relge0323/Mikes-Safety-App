from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """
    Model representing a notification for users.
    """
    
    NOTIFICATION_TYPES = [
        ('new_incident', 'New Incident'),
        ('status_change', 'Status Change'),
        ('assigned', 'Assigned to Incident'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message}"