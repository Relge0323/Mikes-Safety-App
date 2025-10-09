from django import forms
from . import models

class CreateIncident(forms.ModelForm):
    class Meta:
        model = models.Incident
        fields = ['title', 'body', 'slug', 'banner']