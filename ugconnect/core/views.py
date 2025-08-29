
from django.urls import reverse_lazy
from django.shortcuts import render 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Program

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