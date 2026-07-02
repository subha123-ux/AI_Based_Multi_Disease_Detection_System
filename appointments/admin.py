
from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'get_patient',
        'patient_age',
        'get_doctor',
        'date',
        'time',
        'status',
    )

    list_filter = ('status', 'date')
    search_fields = ('patient__username', 'doctor__username')

    def get_patient(self, obj):
        return obj.patient.username

    get_patient.short_description = "Patient"

    def get_doctor(self, obj):
        return obj.doctor.username

    get_doctor.short_description = "Doctor"