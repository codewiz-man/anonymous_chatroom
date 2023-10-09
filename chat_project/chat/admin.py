# chat/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ChatUser

class ChatUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_activity', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'last_activity')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

# Register the ChatUser model with the custom admin class
admin.site.register(ChatUser, ChatUserAdmin)
