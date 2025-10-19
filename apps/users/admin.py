from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Login Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Profile', {
            'fields': ('first_name', 'last_name', 'role')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )