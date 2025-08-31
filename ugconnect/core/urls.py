

from django.urls import path
from . import views
app_name = 'core'

urlpatterns = [
     path('', views.home, name='home'),
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/new/', views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<uuid:pk>/', views.ProgramDetailView.as_view(), name='program_detail'),
    path('programs/<uuid:pk>/edit/', views.ProgramUpdateView.as_view(), name='program_update'),
    path('programs/<uuid:pk>/delete/', views.ProgramDeleteView.as_view(), name='program_delete'),


    # Facility URLs
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
]