from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import tascaty_user, team_leads


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (('tascaty_users'), {'fields': ('username', 'password')}),
        (('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'approver')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_team_lead', 'is_manager',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = settings.AUTH_USER_MODEL
    list_display = ['username', 'email', 'approver', 'is_team_lead']


admin.site.register(tascaty_user, CustomUserAdmin)

admin.site.register(team_leads)


#admin.site.register(User, UserAdmin)
