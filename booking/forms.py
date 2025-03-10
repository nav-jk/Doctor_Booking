from django import forms
from .models import DoctorAvailability

class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['date']
