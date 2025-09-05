from django import forms
from .models import Project, Participant

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
        
        


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'  
        widgets = {
            'cross_skill_trained': forms.CheckboxInput(),
        }