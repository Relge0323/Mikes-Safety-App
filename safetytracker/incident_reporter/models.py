from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Incident(models.Model):
    """
    Model representing a workplace safety incident.

    Attributes:
        title (str): Short title of the incident (max 75 characters).
        body (str): Detailed description of the incident.
        slug (str): URL-friendly unique identifier for the incident (auto-generated).
        date (datetime): Timestamp of when the incident was created (auto-populated).
        banner (ImageField): Optional image related to the incident. Defaults to 'fallback.jpg'.
        reporter (User): Reference to the User who reported the incident. Can be null or blank.
        status (str): Current status of the incident (new, in_progress, resolved, closed).
        assigned_to (User): Manager assigned to handle this incident (optional).

    Methods:
        __str__(): Returns the incident title as its string representation.
        save(): Overridden to auto-generate unique slug from title before saving.
    """
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.jpg', blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='reported_incidents')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Incident.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date']


class Notification(models.Model):
    """
    Model representing a notification for users.
    
    Attributes:
        user (User): The user who should receive this notification.
        incident (Incident): The incident this notification is about.
        message (str): The notification message.
        notification_type (str): Type of notification (new_incident, status_change, assigned).
        is_read (bool): Whether the notification has been read.
        created_at (datetime): When the notification was created.
    """
    
    NOTIFICATION_TYPES = [
        ('new_incident', 'New Incident'),
        ('status_change', 'Status Change'),
        ('assigned', 'Assigned to Incident'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.message}"