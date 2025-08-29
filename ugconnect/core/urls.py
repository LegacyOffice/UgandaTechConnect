

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
]