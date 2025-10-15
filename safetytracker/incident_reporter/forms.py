from django import forms
from . import models

class CreateIncident(forms.ModelForm):
    class Meta:
        model = models.Incident
        fields = ['title', 'body', 'banner']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief incident title'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description of the incident'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Incident Title',
            'body': 'Description',
            'banner': 'Photo (optional)',
        }