from rest_framework.views import APIView
from rest_framework.response import Response
from tascaty.models import activity_tracker
from tascaty.api.serializers import ActivitySerializer
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.db.models import F, Sum, Count, FloatField
from django.db.models.functions import Cast
from datetime import datetime, timedelta
from users.models import tascaty_user, team_leads


class ListMgrActivity(APIView):
    def get(self, request, format=None):
        #start_date = datetime.today()-timedelta(30)
        #end_date = datetime.today()
        #data = activity_tracker.objects.values(Activity_Name=F(
        #    'activity_name__activity_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(Activity_Count=Count('id'))
        #'2020-01-21'
        #'2020-01-01'
        uid=request.GET.get('uid', '');
        TeamLeadID = team_leads.objects.get(user_name=uid).id
        to_date=request.GET.get('to_date', '');
        from_date=request.GET.get('from_date', '');        
        data = activity_tracker.objects.values(Activity_Name=F('activity_name__activity_name')).annotate(Activity_Count=Count('id')).filter(approver=TeamLeadID,status=3).filter(date__lte=to_date, date__gte=from_date)       
        return Response(data)


class ListMgrClient(APIView):
    def get(self, request, format=None):
        #start_date = datetime.today()-timedelta(30)
        #end_date = datetime.today()
        #data = activity_tracker.objects.values(name=F(
        #'client_name__client_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(y=Count('id'))
        uid=request.GET.get('uid', '');
        TeamLeadID = team_leads.objects.get(user_name=uid).id
        to_date=request.GET.get('to_date', '');
        from_date=request.GET.get('from_date', '');
        data = activity_tracker.objects.values(name=F('client_name__client_name')).annotate(y=Count('id')).filter(approver=TeamLeadID,status=3).filter(date__lte=to_date, date__gte=from_date) 
        return Response(data)



class ListActivity(APIView):
    def get(self, request, format=None):
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(Activity_Name=F(
            'activity_name__activity_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(Activity_Count=Count('id'))
        return Response(data)


class ListClient(APIView):
    def get(self, request, format=None):
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(name=F(
            'client_name__client_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(y=Count('id'))
        return Response(data)


class ListClientAct(APIView):
    def get(self, request, format=None):
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(Client_Name=F(
            'client_name__client_name'), Activity_Name=F(
            'activity_name__activity_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(Count=Count('id'))
        return Response(data)


class ListHours(APIView):
    def get(self, request, format=None):
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values('date').filter(
            user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(hours=Cast(((Sum('hours')*60)+(Sum('mins')))/60.0, FloatField())).order_by('date')
        return Response(data)

class ListClientHour(APIView):
    def get(self, request, format=None):
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(label=F(
            'client_name__client_name')).filter(user_name=request.user, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(y=Cast(((Sum('hours')*60)+(Sum('mins')))/60.0, FloatField()))
        return Response(data)


# class ActivityList(ListAPIView):
#     queryset = activity_tracker.objects.all()
#     serializer_class = ActivitySerializer


# @api_view()
# def hello_world(request):
#     data = activity_tracker.objects.values(
#         'activity_name').annotate(ACount=Count('activity_name'))
#     return Response(data)

class TeamListActivity(APIView):
    def get(self, request, format=None):
        UserID = tascaty_user.objects.get(username=request.user).id
        TeamLeadID = team_leads.objects.get(user_name=UserID).id
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(Activity_Name=F(
            'activity_name__activity_name')).filter(approver=TeamLeadID, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(Activity_Count=Count('id'))
        return Response(data)


class TeamListClient(APIView):
    def get(self, request, format=None):
        UserID = tascaty_user.objects.get(username=request.user).id
        TeamLeadID = team_leads.objects.get(user_name=UserID).id
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(name=F(
            'client_name__client_name')).filter(approver=TeamLeadID, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(y=Count('id'))
        return Response(data)


class TeamListClientHour(APIView):
    def get(self, request, format=None):
        UserID = tascaty_user.objects.get(username=request.user).id
        TeamLeadID = team_leads.objects.get(user_name=UserID).id
        start_date = datetime.today()-timedelta(30)
        end_date = datetime.today()
        data = activity_tracker.objects.values(label=F(
            'client_name__client_name')).filter(approver=TeamLeadID, status=3).filter(date__gt=start_date, date__lt=end_date).annotate(y=Cast(((Sum('hours')*60)+(Sum('mins')))/60.0, FloatField()))
        return Response(data)
