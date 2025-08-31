
from django.contrib import admin
from .models import Program ,Equipment

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Program model in the Django admin site.
    """
    list_display = ('name', 'focus_areas', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'focus_areas')
    list_filter = ('created_at',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Equipment model in the Django admin site.
    """
    list_display = (
        'name', 
        'facility', 
        'usage_domain', 
        'support_phase', 
        'inventory_code',
        'is_operational',
        'created_at'
    )
    list_filter = (
        'facility', 
        'usage_domain', 
        'support_phase', 
        'is_operational',
        'created_at'
    )
    search_fields = (
        'name', 
        'inventory_code', 
        'capabilities', 
        'description',
        'facility__name'
    )
    ordering = ('facility__name', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'facility', 'inventory_code')
        }),
        ('Technical Details', {
            'fields': ('capabilities', 'description', 'usage_domain', 'support_phase')
        }),
        ('Status', {
            'fields': ('is_operational',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('facility')

