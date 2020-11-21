from django import forms
from . import models

class SearchForm(forms.ModelForm):

    class Meta:
        model = models.Patient
        fields = [
            'name',
            'insurance',
        ]

    severities = [
        (1, 'Name'),
        (2, 'Severity'),
    ]

    severity = forms.ChoiceField(choices=severities, widget=forms.RadioSelect, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['insurance'].required = False
