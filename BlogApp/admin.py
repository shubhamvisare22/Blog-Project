from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     model = models.User
#     list_display = ['username', 'email', 'user_role']


# admin.site.register(models.User, CustomUserAdmin)

admin.site.register(models.Blog)
admin.site.register(models.Comment)
admin.site.register(models.Response)
