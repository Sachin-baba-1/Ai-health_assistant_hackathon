# forms.py
from django import forms
from .models import FitnessReport

class FitnessReportForm(forms.ModelForm):
    class Meta:
        model = FitnessReport
        fields = ['bmi', 'body_fat_percentage', 'waist_to_hip_ratio']
