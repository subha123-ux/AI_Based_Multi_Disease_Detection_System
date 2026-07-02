# from .models import UserProfile

# def user_profile(request):
#     if request.user.is_authenticated:
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             return {'profile': profile}
#         except UserProfile.DoesNotExist:
#             return {}
#     return {}


from .models import UserProfile

def user_profile(request):
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        return {'profile': profile}
    return {}