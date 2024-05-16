from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    search_fields = ('email',)

admin.site.register(User, UserAdmin)