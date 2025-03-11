from django.contrib import admin
from .models import Client

# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
 
 
admin.site.register(Client,ClientAdmin)