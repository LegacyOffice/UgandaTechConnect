
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Program, Facility 

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