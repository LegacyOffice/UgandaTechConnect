
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Program, Facility, Equipment, Project
from .forms import ProjectForm


def home(request):
    return render(request, 'core/home.html')

class ProgramListView(ListView):
    model = Program
    template_name = 'core/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )
        return queryset
class ProgramDetailView(DetailView):
    model = Program
    template_name = 'core/program_detail.html'
    context_object_name = 'program'
class ProgramCreateView(CreateView):
    model = Program
    fields = ['name', 'description', 'national_alignment', 'focus_areas', 'phases']
    template_name = 'core/program_form.html'
    success_url = reverse_lazy('core:program_list')
class ProgramUpdateView(UpdateView):
    model = Program
    fields = ['name', 'description', 'national_alignment', 'focus_areas', 'phases']
    template_name = 'core/program_form.html'

    def get_success_url(self):
        return reverse_lazy('core:program_detail', kwargs={'pk': self.object.pk})


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'core/program_confirm_delete.html'
    context_object_name = 'program'
    success_url = reverse_lazy('core:program_list')



##FACILITY VIEWS##
class FacilityListView(ListView):
    model = Facility
    template_name = 'core/facility_list.html'
    context_object_name = 'facilities'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )
        return queryset


class FacilityDetailView(DetailView):
    model = Facility
    template_name = 'core/facility_detail.html'
    context_object_name = 'facility'


class FacilityCreateView(CreateView):
    model = Facility
    fields = [
        'name', 'description', 'location', 'type',
        'capacity', 'resources', 'contact_email',
        'contact_phone', 'programs'
    ]
    template_name = 'core/facility_form.html'
    success_url = reverse_lazy('core:facility_list')


class FacilityUpdateView(UpdateView):
    model = Facility
    fields = [
        'name', 'description', 'location', 'type',
        'capacity', 'resources', 'contact_email',
        'contact_phone', 'programs'
    ]
    template_name = 'core/facility_form.html'

    def get_success_url(self):
        return reverse_lazy('core:facility_detail', kwargs={'pk': self.object.pk})


class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = 'core/facility_confirm_delete.html'
    context_object_name = 'facility'
    success_url = reverse_lazy('core:facility_list')

class EquipmentListView(ListView):
    model = Equipment
    template_name = 'core/equipment_list.html'
    context_object_name = 'equipment_list'
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('facility')
        
        # Search functionality
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )
        
        # Filter by facility
        facility_filter = self.request.GET.get('facility')
        if facility_filter:
            queryset = queryset.filter(facility_id=facility_filter)
        
        # Filter by usage domain
        domain_filter = self.request.GET.get('domain')
        if domain_filter:
            queryset = queryset.filter(usage_domain=domain_filter)
        
        # Filter by support phase
        phase_filter = self.request.GET.get('phase')
        if phase_filter:
            queryset = queryset.filter(support_phase=phase_filter)
            
        # Filter by operational status
        operational_filter = self.request.GET.get('operational')
        if operational_filter == 'true':
            queryset = queryset.filter(is_operational=True)
        elif operational_filter == 'false':
            queryset = queryset.filter(is_operational=False)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = Facility.objects.all().order_by('name')
        context['usage_domains'] = Equipment.USAGE_DOMAINS
        context['support_phases'] = Equipment.SUPPORT_PHASES
        return context


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = 'core/equipment_detail.html'
    context_object_name = 'equipment'
    
    def get_queryset(self):
        return super().get_queryset().select_related('facility')


class EquipmentCreateView(CreateView):
    model = Equipment
    fields = [
        'facility', 'name', 'capabilities', 'description', 
        'inventory_code', 'usage_domain', 'support_phase', 'is_operational'
    ]
    template_name = 'core/equipment_form.html'
    success_url = reverse_lazy('core:equipment_list')


class EquipmentUpdateView(UpdateView):
    model = Equipment
    fields = [
        'facility', 'name', 'capabilities', 'description', 
        'inventory_code', 'usage_domain', 'support_phase', 'is_operational'
    ]
    template_name = 'core/equipment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('core:equipment_detail', kwargs={'pk': self.object.pk})


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'core/equipment_confirm_delete.html'
    context_object_name = 'equipment'
    success_url = reverse_lazy('core:equipment_list')


class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Title__icontains=search_query)
        return queryset

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'  # Add 'core/' prefix
    success_url = reverse_lazy('core:project_list')  # Add app namespace

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'  # Add 'core/' prefix
    success_url = reverse_lazy('core:project_list')  # Add app namespace

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('project_list')