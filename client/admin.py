from django.contrib import admin
from .models import ClientInformation

class ClientInformationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    list_filter = ('gender', 'date_of_birth')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('date_created', 'date_updated')

admin.site.register(ClientInformation, ClientInformationAdmin)
