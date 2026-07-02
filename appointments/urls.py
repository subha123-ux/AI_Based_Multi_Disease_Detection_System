
from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),  
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointment/update/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
]