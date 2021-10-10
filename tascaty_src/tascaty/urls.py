from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('mytask/', views.MyTask, name='mytask'),
    path('myteam/', views.MyTeam, name='myteam'),
    path('activity/<int:pk>/update', views.ActivityUpdateView.as_view(),name='updateview'),
    path('activity/<int:pk>/delete', views.ActivityDeleteView.as_view(),name='deleteview'),
    path('teamdashboard/', views.TeamDashboard, name='team-dashboard'),
    path('teamreport/', views.TeamReport, name='team-report'),
    path('teamreportdownload/', views.TeamReportDownload, name='team-report-download'),
]
