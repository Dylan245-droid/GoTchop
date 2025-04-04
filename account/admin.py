from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'date_joined')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        })
    )

    add_fieldsets = (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
    })


@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')
    search_fields = ('user__email', 'user__username')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'code', 'created_at')
        }),
    )

    add_fieldsets = (None, {
        'classes': ('wide',),
        'fields': ('user', 'code')
    })

    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = generate_serie(6)
        super().save_model(request, obj, form, change)