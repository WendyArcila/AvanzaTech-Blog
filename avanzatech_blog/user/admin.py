from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    # read
    list_display = (
        'nick_name',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
        'team')
    search_fields = ('email', 'team')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'team')
    # Edit a user
    fieldsets = (
        ('Personal Info', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Team', {'fields': ('team',)}),
    )
    # Create a user
    add_fieldsets = (
        ("Create New User", {
            'classes': ('wide',),
            'fields': ('nick_name', 'email', 'password1', 'password2', 'team'),
        }),
    )
    ordering = ['email']


admin.site.register(CustomUser, CustomUserAdmin)
