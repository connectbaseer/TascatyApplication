from .models import leaves
from django import forms

class LeavesForm(forms.ModelForm):

    start_date = forms.DateField(label='', widget=forms.DateInput(
        attrs={"placeholder": "Start Date", 'class': 'form-control', 'id': 'datepicker'}))
    end_date = forms.DateField(label='', widget=forms.DateInput(
        attrs={"placeholder": "End Date", 'class': 'form-control', 'id': 'datepicker2'}))

    class Meta:
        model = leaves
        fields = ['start_date', 'end_date']
