from django.contrib import admin
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple

class BetterUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # Get form from original UserAdmin.
        form = super(BetterUserAdmin, self).get_form(request, obj, **kwargs)
        groups = form.base_fields['groups']
        groups.widget = FilteredSelectMultiple("Groups", False)
        return form


admin.site.unregister(User)
admin.site.register(User, BetterUserAdmin)
