from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

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
        save(): Override to auto-generate a unique slug from the title before saving.
    """
    title = models.CharField(max_length=75)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.jpg', blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # is the slug field empty?
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            # make sure the slug is unique in the database
            while Incident.objects.filter(slug=slug).exists():
                # if the slug exists, add a counter at the end
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug
        # calling the parent class's save method to save the model
        super().save(*args, **kwargs)