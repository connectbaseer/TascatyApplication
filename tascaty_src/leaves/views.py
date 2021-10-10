from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .models import leaves
from .forms import LeavesForm
from users.models import tascaty_user, team_leads
from tascaty.models import activity_status
from django.contrib.auth.mixins import LoginRequiredMixin



class MyLeaves(LoginRequiredMixin, CreateView):
    model = leaves
    form_class = LeavesForm
    template_name = 'leaves/leaves.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.instance.approver = tascaty_user.objects.get(
            username=self.request.user).approver
        return super().form_valid(form)


    
