from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_employee(self):
        return self.role == 'employee'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save the Profile whenever the User is saved.
    """
    instance.profile.save()