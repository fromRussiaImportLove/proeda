from django.contrib import admin

from users.models import CustomUser


class CustomUsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'is_banned', 'is_active','role')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUsersAdmin)
