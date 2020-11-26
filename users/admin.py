from django.contrib import admin

from users.models import CustomUser


class CustomUsersAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'is_banned',
                    'is_active', 'role')
    list_filter = ('role', 'is_banned')
    list_display_links = ('pk', 'username')
    search_fields = ('username', 'email', 'first_name', 'second_name')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUsersAdmin)
