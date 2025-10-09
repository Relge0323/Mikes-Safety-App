from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Incident(models.Model):
    """
    Model representing a workplace safety incident.

    Attributes:
        title (str): Short title of the incident (max 75 characters).
        body (str): Detailed description of the incident.
        slug (str): URL-friendly unique identifier for the incident.
        date (datetime): Timestamp of when the incident was created (auto-populated).
        banner (ImageField): Optional image related to the incident. Defaults to 'fallback.jpg'.
        reporter (User): Reference to the User who reported the incident. Can be null or blank.

    Methods:
        __str__(): Returns the incident title as its string representation.
    """
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.jpg', blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title