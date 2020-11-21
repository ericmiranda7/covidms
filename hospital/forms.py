from django import forms
from . import models

class SearchForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = [
            'name',
            'insurance',
        ]