from django.contrib import admin
from .models import Log, SourceLog

class LogAdmin(admin.ModelAdmin):
    list_display = ('log_key', 'user', 'start_time', 'end_time', 'is_public', 'deleted_at')
    search_fields = ('description', 'log_key', 'user__username')
    list_filter = ('is_public', 'user')

class SourceLogAdmin(admin.ModelAdmin):
    list_display = ('log', 'url', 'is_digital')
    search_fields = ('url', 'text')
    list_filter = ('is_digital',)


admin.site.register(Log, LogAdmin)
admin.site.register(SourceLog, SourceLogAdmin)
