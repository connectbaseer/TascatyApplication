from django import forms
from .models import activity, system, client, activity_tracker
import re

class ActivityTrackerModelForm(forms.ModelForm):
    date = forms.DateField(label='', widget=forms.DateInput(attrs={
                           "placeholder": "Select Date", 'id': 'datepicker', 'class': 'form-control w-100', 'autocomplete': 'off'}))
    activity_name = forms.ModelChoiceField(queryset=activity.objects.all().order_by(
        'activity_name'), label='', empty_label="Select Activity", widget=forms.Select(attrs={'class': 'form-control w-100'}))
    system_name = forms.ModelChoiceField(queryset=system.objects.all().order_by('system_name'), label='', empty_label="Select System", widget=forms.Select(attrs={'class': 'form-control w-100'}))
    client_name = forms.ModelChoiceField(queryset=client.objects.all().order_by(
        'client_name'), label='',  empty_label="Select Client", widget=forms.Select(attrs={'class': 'form-control w-100'}))
    hour_choice = [('', 'Choose Hours'), (0, 0), (1, 1), (2, 2),(3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
    hours = forms.ChoiceField(label='', choices=hour_choice, widget=forms.Select(
        attrs={'class': 'form-control w-100'}))
    min_choice = [('', 'Choose Mins'), (0, 0), (15, 15), (30, 30), (45, 45)]
    mins = forms.ChoiceField(label='', choices=min_choice, widget=forms.Select(attrs={'class': 'form-control w-100'}))
    no_of_records = forms.IntegerField(label='', required=False, widget=forms.NumberInput(
        attrs={"placeholder": "Enter no. of Records", 'class': 'form-control w-100', 'autocomplete': 'off'}))
    project_id = forms.CharField(label='', required=False, widget=forms.TextInput(
        attrs={"placeholder": "Project ID", 'class': 'form-control w-100', 'autocomplete': 'off'}))
    user_comments = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Enter Your Comments Here...",
                'rows': 6,
                'class': 'form-control w-100',
                'autocomplete': 'off'
            }
        )
    )


    
    class Meta:
        model = activity_tracker
        fields = ['date', 'activity_name', 'system_name', 'client_name',
                  'hours', 'mins', 'no_of_records', 'project_id', 'user_comments']

    def clean(self):
        cleaned_data = super(ActivityTrackerModelForm, self).clean()
        activity = cleaned_data.get('activity_name')
        project_1 = cleaned_data.get('project_id')
        if re.search("^New.Project.Activities$", str(activity)) and project_1 == "":
            self.add_error('project_id', "Please Add Project ID")
        return cleaned_data

    
