

from django.urls import path
from . import views
from .views import (
    ParticipantListView, ParticipantDetailView, ParticipantCreateView,
    ParticipantUpdateView, ParticipantDeleteView
)
from .views import UnifiedSearchView
app_name = 'core'

urlpatterns = [
     path('', views.home, name='home'),
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/new/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<uuid:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/<uuid:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<uuid:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),


    path('facilities/', views.FacilityListView.as_view(), name='facility_list'),
    path('facilities/new/', views.FacilityCreateView.as_view(), name='facility_create'),
    path('facilities/<uuid:pk>/', views.FacilityDetailView.as_view(), name='facility_detail'),
    path('facilities/<uuid:pk>/edit/', views.FacilityUpdateView.as_view(), name='facility_update'),
    path('facilities/<uuid:pk>/delete/', views.FacilityDeleteView.as_view(), 
    name='facility_delete'),

    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/<uuid:pk>/', views.EquipmentDetailView.as_view(), name='equipment_detail'),
    path('equipment/create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    path('equipment/<uuid:pk>/update/', views.EquipmentUpdateView.as_view(), name='equipment_update'),
    path('equipment/<uuid:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),

    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

  
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<uuid:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<uuid:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<uuid:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    path('participants/', ParticipantListView.as_view(), name='participant_list'),
    path('participants/<int:pk>/', ParticipantDetailView.as_view(), name='participant_detail'),
    path('participants/create/', ParticipantCreateView.as_view(), name='participant_create'),
    path('participants/<int:pk>/update/', ParticipantUpdateView.as_view(), name='participant_update'),
    path('participants/<int:pk>/delete/', ParticipantDeleteView.as_view(), name='participant_delete'),
    path('search/', UnifiedSearchView.as_view(), name='unified_search'),

    path('outcomes/', views.OutcomeListView.as_view(), name='outcome_list'),
    path('outcome/<int:pk>/', views.OutcomeDetailView.as_view(), name='outcome_detail'),
    path('outcome/new/', views.OutcomeCreateView.as_view(), name='outcome_create'),
    path('outcome/<int:pk>/edit/', views.OutcomeUpdateView.as_view(), name='outcome_update'),
    path('outcome/<int:pk>/delete/', views.OutcomeDeleteView.as_view(), name='outcome_delete'),
]

