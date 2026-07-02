from django.urls import path
from . import views

urlpatterns = [
    path('download/<int:report_id>/', views.download_report, name='download_report'),
    path('admin-reports/', views.admin_all_reports, name='admin_reports'),
]