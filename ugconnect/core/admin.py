
from django.contrib import admin
from .models import Program

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Program model in the Django admin site.
    """
    list_display = ('name', 'focus_areas', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'focus_areas')
    list_filter = ('created_at',)