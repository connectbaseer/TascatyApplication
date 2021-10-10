from tascaty.api.views import ListActivity, ListClient, ListMgrActivity, ListMgrClient, ListClientAct, ListHours, ListClientHour, TeamListActivity, TeamListClient, TeamListClientHour
from django.urls import path


urlpatterns = [
    path('api/listactivity', ListActivity.as_view(), name='list-view'),
    path('api/listclient', ListClient.as_view(), name='list-client'),
    path('api/listmgractivity', ListMgrActivity.as_view(), name='list-mgr-view'),
    path('api/listmgrclient', ListMgrClient.as_view(), name='list-mgr-client'),
    path('api/listclientact', ListClientAct.as_view(), name='list-clientact'),
    path('api/listhours', ListHours.as_view(), name='list-hours'),
    path('api/listclienthours', ListClientHour.as_view(), name='list-clienthours'),
    path('api/teamactivity', TeamListActivity.as_view(), name='list-teamactivity'),
    path('api/teamclient', TeamListClient.as_view(), name='list-teamclient'),
    path('api/teamclienthour', TeamListClientHour.as_view(), name='list-teamclienthour'),
]
