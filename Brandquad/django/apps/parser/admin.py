from django.contrib import admin
from apps.parser.models import Log

# Register your models here.
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date', 'ip', 'method', 'uri', 'status_code', 'content_length')
    list_display_links = ('date', 'ip')
    ordering = ('-date', )
    search_fields = ('ip', )
    list_filter = ('date', 'method', 'uri', 'status_code')
