'''
from django.contrib import admin

from .models import BasicInformation

@admin.register(BasicInformation)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        #'age',
        #'address',
        #'contact_number'
    )
    search_fields = (
        'user__username',
        'user__email',
    )

'''
