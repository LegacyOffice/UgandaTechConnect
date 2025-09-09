from django.urls import reverse_lazy
from django.shortcuts import render 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Program, Facility, Equipment, Project, Service, Participant, Outcome
from .forms import (
    ProgramForm, FacilityForm, EquipmentForm, ProjectForm, 
    ServiceForm, ParticipantForm, OutcomeForm
)
from django.db.models import Q



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
    form_class = ProgramForm
    template_name = 'core/program_form.html'
    success_url = reverse_lazy('core:program_list')
class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
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
    form_class = FacilityForm
    template_name = 'core/facility_form.html'
    success_url = reverse_lazy('core:facility_list')


class FacilityUpdateView(UpdateView):
    model = Facility
    form_class = FacilityForm
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
    form_class = EquipmentForm
    template_name = 'core/equipment_form.html'
    
    def get_success_url(self):
        return reverse_lazy('core:equipment_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Equipment "{self.object.name}" was created successfully!')
        return response


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
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
    
    def get_success_url(self):
        return reverse_lazy('core:project_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Project "{self.object.Title}" was created successfully!')
        return response

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'core/project_form.html'  # Add 'core/' prefix
    success_url = reverse_lazy('core:project_list')  # Add app namespace

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('project_list')


# Service view
class ServiceListView(ListView):
    model = Service
    template_name = 'core/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search', '')
        facility = self.request.GET.get('facility')
        category = self.request.GET.get('category')

        if search:
            qs = qs.filter(name__icontains=search)
        if facility:
            qs = qs.filter(facility__facility_id=facility)
        if category:
            qs = qs.filter(category=category)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facilities'] = Facility.objects.all()
        context['service_categories'] = Service.CATEGORY_CHOICES  
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'
    context_object_name = 'service'

    def get_queryset(self):
        return super().get_queryset().select_related('facility')


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_form.html'

    def get_success_url(self):
        return reverse_lazy('core:service_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Service "{self.object.name}" was created successfully!')
        return response

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_form.html'

    def get_success_url(self):
        return reverse_lazy('core:service_detail', kwargs={'pk': self.object.pk})


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'core/service_confirm_delete.html'
    context_object_name = 'service'
    success_url = reverse_lazy('core:service_list')
    
    

class ParticipantListView(ListView):
    model = Participant
    template_name = 'core/participant_list.html'
    context_object_name = 'participants'

class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'core/participant_detail.html'

class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'core/participant_form.html'
    
    def get_success_url(self):
        return reverse_lazy('core:participant_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Participant "{self.object.full_name}" was added successfully!')
        return response

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'core/participant_form.html'
    success_url = reverse_lazy('core:participant_list')

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'core/participant_confirm_delete.html'
    success_url = reverse_lazy('core:participant_list')
    

class UnifiedSearchView(ListView):
    template_name = 'core/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        # Example: search only Programs by name
        return Program.objects.filter(name__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.results_dict)
        context['query'] = self.request.GET.get('q', '')
        return context
class OutcomeListView(ListView):
    model = Outcome
    template_name = 'core/outcome_list.html'
    context_object_name = 'outcomes'
    
    def get_queryset(self):
        # You can add filtering/sorting here if needed
        return Outcome.objects.all().select_related('ProjectId')

class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = 'core/outcome_detail.html'
    context_object_name = 'outcome'

class OutcomeCreateView(CreateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = 'core/outcome_form.html'
    
    def get_success_url(self):
        return reverse_lazy('core:outcome_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Outcome "{self.object.Title}" was created successfully!')
        return response

class OutcomeUpdateView(UpdateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = 'core/outcome_form.html'
    
    def get_success_url(self):
        return reverse_lazy('outcome_detail', kwargs={'pk': self.object.pk})

class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = 'core/outcome_confirm_delete.html'
    success_url = reverse_lazy('outcome_list')