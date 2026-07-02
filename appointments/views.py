
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from accounts.models import UserProfile
from .models import Appointment

from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, from_email, recipient_list, fail_silently=False):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently
    )


@login_required
def book_appointment(request):

    doctors = UserProfile.objects.filter(
        user__role="DOCTOR",
        is_approved=True
    )

    if request.method == "POST":

        patient_age = request.POST.get("patient_age")
        doctor_reg = request.POST.get("doctor_reg")
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message")

        try:
            doctor_profile = UserProfile.objects.get(
                registration_number=doctor_reg,
                is_approved=True
            )
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid doctor selected.")
            return redirect("book_appointment")

        Appointment.objects.create(
            patient=request.user,
            doctor=doctor_profile.user,
            patient_age=patient_age,
            date=date,
            time=time,
            message=message,
            status="Pending"
        )

        patienr_subject = "Appointment Booking Confirmation"
        patient_message = f"Dear {request.user.first_name},\n\nYour appointment with Dr. {doctor_profile.user.first_name} {doctor_profile.user.last_name} has been booked successfully for {date} at {time}. with the message: {message}\n\nThank you."
        send_email(
            subject=patienr_subject,
            message=patient_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False
        )

        doctor_subject = "New Appointment Booking"
        doctor_message = f"Dear Dr. {doctor_profile.user.first_name} {doctor_profile.user.last_name},\n\nYou have a new appointment booked by {request.user.first_name} {request.user.last_name} for {date} at {time}. with the message: {message}\n\nPlease confirm the appointment in your dashboard."
        send_email(
            subject=doctor_subject,
            message=doctor_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[doctor_profile.user.email],
            fail_silently=False
        )

        messages.success(request, "Appointment booked successfully!")
        return redirect("patient_dashboard")

    return render(request, "appointments/book.html", {
        "doctors": doctors
    })



@login_required
def confirm_appointment(request, id):

    appointment = get_object_or_404(Appointment, id=id)

    if request.user != appointment.doctor:
        return HttpResponseForbidden("Not allowed")

    appointment.status = "Confirmed"
    appointment.save()

    try:
        patient_subject = "Appointment Confirmation"
        patient_message = f"Dear {appointment.patient.first_name},\n\nYour appointment with Dr. {appointment.doctor.first_name} {appointment.doctor.last_name} on {appointment.date} at {appointment.time} has been confirmed.\n\nThank you."
        send_email(
            subject=patient_subject,
            message=patient_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient.email],
            fail_silently=False
        )
    except Exception as e:
        messages.error(request, f"Failed to send email notification: {str(e)}")
        return redirect("doctor_dashboard")

    messages.success(request, "Appointment confirmed.")
    return redirect("doctor_dashboard")



@login_required
def patient_dashboard(request):

    appointments = Appointment.objects.filter(
        patient=request.user
    ).order_by("-date", "-time")

    return render(request, "appointments/patient_dashboard.html", {
        "appointments": appointments
    })



@login_required
def doctor_dashboard(request):

    if request.user.role != "DOCTOR":
        return HttpResponseForbidden("You are not allowed here.")

    appointments = Appointment.objects.filter(
        doctor=request.user
    ).order_by("-date", "-time")

    return render(request, "appointments/doctor_dashboard.html", {
        "appointments": appointments
    })



@login_required
def update_appointment_status(request, appointment_id):

    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user != appointment.doctor:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in dict(Appointment.STATUS_CHOICES):
            appointment.status = new_status
            appointment.save()

        return redirect("doctor_dashboard")

    return render(request, "appointments/update_status.html", {
        "appointment": appointment
    })