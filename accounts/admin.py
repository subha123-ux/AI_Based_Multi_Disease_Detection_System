from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile


class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'get_name',
        'get_age',
        'role',
        'get_is_approved',
        'is_staff'
    )

    list_filter = ('is_staff', 'role')

    def get_name(self, obj):
        return getattr(obj.userprofile, 'name', "-")
    get_name.short_description = "Name"

    def get_age(self, obj):
        return getattr(obj.userprofile, 'age', "-")
    get_age.short_description = "Age"

    def get_is_approved(self, obj):
        return getattr(obj.userprofile, 'is_approved', False)
    get_is_approved.boolean = True
    get_is_approved.short_description = "Approved"


class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'name',
        'age',
        'get_email',
        'get_role', 
        'registration_number',
        'is_approved'
    )

    list_filter = ('is_approved',)
    search_fields = ('user__username', 'name')

    def get_role(self, obj):
        return obj.user.role
    get_role.short_description = "Role"

    def get_email(self, obj):
        return obj.user.email   
    get_email.short_description = "Email"


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)