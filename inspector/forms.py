# inspector/forms.py
from django import forms
from .models import Inspection

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['improvements_needed', 'comments']
