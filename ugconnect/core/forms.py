from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'ProgramId', 'FacilityId', 'Title', 'NatureOfProject', 
            'Description', 'InnovationFocus', 'PrototypeStage', 
            'TestingRequirements', 'CommercializationPlan'
        ]
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 4}),
            'TestingRequirements': forms.Textarea(attrs={'rows': 4}),
            'CommercializationPlan': forms.Textarea(attrs={'rows': 4}),
        }