from django import forms
from . import models
from django.contrib.auth.models import User

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

class UpdateIncidentStatus(forms.ModelForm):
    class Meta:
        model = models.Incident
        fields = ['status', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'status': 'Incident Status',
            'assigned_to': 'Assign to Manager',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who are managers in the assigned_to dropdown
        from users.models import Profile
        manager_profiles = Profile.objects.filter(role='manager')
        manager_users = [profile.user.id for profile in manager_profiles]
        self.fields['assigned_to'].queryset = User.objects.filter(id__in=manager_users)
        self.fields['assigned_to'].required = False


class IncidentFilterForm(forms.Form):
    """Form for filtering incidents by various criteria."""
    
    STATUS_CHOICES = [('', 'All Statuses')] + list(models.Incident.STATUS_CHOICES)
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or description...'
        }),
        label='Search'
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )
    
    reporter = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Reporter',
        empty_label='All Reporters'
    )
    
    assigned_to = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Assigned To',
        empty_label='All Managers'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='To Date'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter assigned_to to only show managers
        from users.models import Profile
        manager_profiles = Profile.objects.filter(role='manager')
        manager_users = [profile.user.id for profile in manager_profiles]
        self.fields['assigned_to'].queryset = User.objects.filter(id__in=manager_users)