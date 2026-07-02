from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserProfile

User = get_user_model()


def register_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        name = request.POST.get("name")
        email = request.POST.get("email")
        age = request.POST.get("age")
        role = request.POST.get("role")  
        registration_number = request.POST.get("registration_number")

        if not username or not password:
            messages.error(request, "Username and password required.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        age=int(age) if age else None
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )


        is_approved = False if role == "DOCTOR" else True

        UserProfile.objects.create(
            user=user,
            name=name,
            age=age,
            registration_number=registration_number,
            is_approved=is_approved
        )

        if role == "DOCTOR":
            messages.success(request, "Registered! Wait for admin approval.")
        else:
            messages.success(request, "Registered successfully. You can login.")

        return redirect("login")

    return render(request, "register.html")



def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
            return redirect("login")


        if user.is_superuser:
            login(request, user)
            return redirect("/admin/")

        profile = UserProfile.objects.filter(user=user).first()

        if not profile:
            messages.error(request, "Profile not found. Contact admin.")
            return redirect("login")


        if user.role == "DOCTOR" and not profile.is_approved:
            messages.error(request, "Your doctor account is not approved yet.")
            return redirect("login")

        login(request, user)
        messages.success(request, "Login successful!")
        return redirect("predict")

    return render(request, "login.html")



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")