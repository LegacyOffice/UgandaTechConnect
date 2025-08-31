
from django.contrib import admin
from .models import Program ,Equipment, Project, Service

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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Service model in the Django admin site
    """
    list_display = (
        'name', 
        'facility', 
        'created_at',
        'updated_at'
    )
    search_fields = (
        'name', 
        'description', 
        'facility__name'
    )
    list_filter = (
        'facility',
        'created_at'
    )
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'facility', 'description')
        }),
        ('Service Details', {
            'fields': (
                'operating_hours',
            )
        }),
    )
    raw_id_fields = ('facility',)  # Removed invalid 'required_equipment'
    ordering = ('facility__name', 'name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('facility')
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('ProjectId', 'Title', 'ProgramId', 'FacilityId', 'NatureOfProject', 'InnovationFocus')
    list_filter = ('NatureOfProject', 'InnovationFocus', 'PrototypeStage')
    search_fields = ('Title', 'Description')
    ordering = ('ProjectId',)
