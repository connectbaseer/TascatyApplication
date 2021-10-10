from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import  ActivityTrackerModelForm #,ActivityTrackerForm
from tascaty.models import activity_tracker, activity_status
from users.models import tascaty_user, team_leads
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.urls import reverse
from django.contrib import messages
from collections import namedtuple
from django.db import connection
import csv
from django.http import HttpResponse
from datetime import datetime


@login_required
def Home(request):
    context = {
        'title': 'TasCaty|Home'
    }

    if (request.user.is_manager):
      team_leads=tascaty_user.objects.filter(is_team_lead=True).order_by('-id');
      context = {
        'title': 'TasCaty|Home',
        'team_lead': team_leads
        }
      return render(request, 'tascaty/managerHome.html', context)
    else:
      return render(request, 'tascaty/home.html', context)     
    
@login_required
def MyTask(request):
    form = ActivityTrackerModelForm(request.POST or None)
    if request.method == 'POST':
        form = ActivityTrackerModelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_name = request.user
            obj.approver = tascaty_user.objects.get(
                username=request.user).approver
            if request.user.is_team_lead:
                obj.status = activity_status.objects.get(pk=3)
            obj.save()
            messages.success(request, 'New Entry Created')
            return redirect('mytask')

    queryset1_PA = activity_tracker.objects.filter(
        user_name=request.user).filter(status__in=[1, 2, 4]).order_by('-id')
    queryset1_AP = activity_tracker.objects.filter(
        user_name=request.user).filter(status=3).order_by('-date', '-id')
    paginator_RA = Paginator(queryset1_AP, 10)
    paginator_PA = Paginator(queryset1_PA, 20)
    page = request.GET.get('page')

    context = {
        'title': 'TasCaty|My Task',
        'activity_form': form,
        'post_page_RA': paginator_RA.get_page(page),
        'post_page_PA': paginator_PA.get_page(page),
    }
    return render(request, "tascaty/mytask.html", context)

@login_required
def MyTeam(request):
    if request.method == 'POST':
        from_id = request.POST['id']
        form_status = request.POST['status']
        activity_tracker.objects.filter(
            pk=from_id).update(status=form_status)  
    UserID = tascaty_user.objects.get(username=request.user).id
    TeamLeadID = team_leads.objects.get(user_name=UserID).id
    Paginator_TAL = Paginator(activity_tracker.objects.filter(approver_id=TeamLeadID).filter(status__in=[3]).order_by('-date'),100)
    page = request.GET.get('page')
   
    context = {
        'title': 'TasCaty|My Team',
        'MyTeamActivity': activity_tracker.objects.filter(approver_id=TeamLeadID).filter(status__in=[1, 4]),
        'TeamActivityList': Paginator_TAL.get_page(page)
    }
    return render(request, "tascaty/myteam.html", context)



class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = activity_tracker
    form_class = ActivityTrackerModelForm
    template_name = 'tascaty/update_task.html'

    def form_valid(self, form):
        if form.instance.status.id == 2:
            form.instance.status = activity_status.objects.get(pk=4)
        elif form.instance.status.id == 4:
            form.instance.status = activity_status.objects.get(pk=4)

        return super().form_valid(form)

    def test_func(self):
        user = self.get_object()
        if self.request.user == user.user_name:
            return True
        return False


class ActivityDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = activity_tracker
    template_name = 'tascaty/confirm_delete.html'

    def test_func(self):
        user = self.get_object()
        if self.request.user == user.user_name:
            return True
        return False

    def get_success_url(self):
        return reverse('mytask')


@login_required
def TeamDashboard(request):
    context = {
        'title': 'TasCaty | Team Dashboard'
    }
    return render(request, 'tascaty/teamdahboard.html', context)


@login_required
def TeamReport(request): 
    context = {
         'title': 'TasCaty | Team Report'        
    }
    return render(request, 'tascaty/teamreport.html', context)
    

@login_required
def TeamReportDownload(request):
    output = []
    response = HttpResponse (content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=approved-tasks-report.xls'
    class dia2(csv.Dialect):
        delimiter = '\t' # delimiter should be only 1-char
        quotechar = '"'
        escapechar = None
        doublequote = True
        skipinitialspace = False
        lineterminator = '\r\n'
        quoting = 1

    writer = csv.writer(response,dialect=dia2)
    userObj = tascaty_user.objects.get(username=request.user);     

    print(request.user);
    print(userObj);
    print("isManager:"+str(userObj.is_manager))
    print("isTeamLead:"+str(userObj.is_team_lead))

    rows = extractReportData(userObj, request);
    #Header
    writer.writerow(['ID', 'Team Lead', 'Team Member', 'Date', 'Client Name', 'System Name', 'Activity Name', 'Status Name','Hours', 'Minutes', 'No of Records','User Comments', 'Project Id'])
    for row in rows:
        output.append([row[0],row[1],row[2]+' '+row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13]])
    #CSV Data
    writer.writerows(output)
    return response


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def extractReportData(userObj,request):
    
    toDate=request.GET.get('toDate', '');
    fromDate=request.GET.get('fromDate', '');
    tlId=request.GET.get('tlId', '');
    
    print("from_date:"+fromDate+"\n");
    print("to_date:"+toDate+"\n"); 
    print("tlId:"+tlId+"\n");

    if userObj.is_team_lead:
        teamLeadId = team_leads.objects.get(user_name=userObj.id).id;
    elif userObj.is_manager:
        teamLeadId = "";
        if tlId != "":
            teamLeadId=team_leads.objects.get(user_name=tlId).id

    print("teamLeadId:"+str(teamLeadId)+"\n");

    with connection.cursor() as cursor:
        query_str = '''
        SELECT tat.id,tl.full_name, u.first_name, u.last_name,tat.date,tc.client_name,ts.system_name,ta.activity_name,tas.status_name,tat.hours,tat.mins,tat.no_of_records,tat.user_comments, tat.project_id
        FROM
        tascaty_activity_tracker tat,
        tascaty_activity ta,
        users_team_leads tl,
        tascaty_client tc,
        tascaty_activity_status tas,
        tascaty_system ts,
        users_tascaty_user u
        WHERE
        tat.activity_name_id = ta.id
        and tat.approver_id = tl.id
        and tat.client_name_id = tc.id
        and tat.status_id = tas.id
        and tat.system_name_id = ts.id
        and tat.user_name_id = u.id ''' + (" and tl.id = "+str(teamLeadId) if str(teamLeadId)!="" else " ") +  " and tat.`date` BETWEEN '"+ fromDate +"' AND '"+ toDate +"'" + " and tat.status_id = 3 "
     
        print(query_str);

        cursor.execute(query_str);

        rows = namedtuplefetchall(cursor)
    return rows
    
    

