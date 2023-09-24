from django import forms
from .models import Job, Candidate

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('owner',)

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'
        exclude = ('job',)
