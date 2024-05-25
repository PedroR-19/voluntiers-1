from django import forms
from .models import Candidatura

class CandidaturaForm(forms.ModelForm):
    class Meta:
        model = Candidatura
        fields = ['curriculo']
