from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Officer
from .forms import SignupForm


class UserLayout(UserAdmin):
    model = User
    add_form = SignupForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide"),
                "fields": (
                    'username', 
                    'email', 
                    'mobile_no', 
                    'gender', 
                    'dob', 
                    'password1', 
                    'password2', 
                    'is_officer', 
                    'is_roadsafetystaff'
                )
            }
        ),
    )
    list_display = ['username', 'email', 'gender', 'national_id', 'county', 'sub_county', 'date_joined']
    readonly_fields = [
        'first_name', 
        'last_name', 
        'username', 
        'email', 
        'gender', 
        'dob', 
        'mobile_no', 
        'national_id', 
        'county', 
        'sub_county', 
        'profile_pic', 
        'last_login', 
        'date_joined'
    ]

    fieldsets = (
        ('Personal Info', {
            'fields': (
                'first_name', 
                'last_name', 
                'username', 
                'email', 
                'gender', 
                'dob', 
                'mobile_no', 
                'national_id', 
                'county', 
                'sub_county', 
                'profile_pic',
            )
        }),
        ('User category', {'fields': ('is_officer', 'is_roadsafetystaff')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(User, UserLayout)


@admin.register(Officer)
class OfficersTable(admin.ModelAdmin):
    list_display = ['name', 'station', 'rank']