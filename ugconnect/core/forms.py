from django import forms
from .models import Program, Facility, Equipment, Project, Service, Participant, Outcome

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'description', 'national_alignment', 'focus_areas', 'phases']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter program name...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Overview of the program\'s purpose...'}),
            'national_alignment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Link to NDPIII, Roadmap, or 4IR goals...'}),
            'focus_areas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IoT, automation, renewable energy (comma-separated)'}),
            'phases': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cross-Skilling, Collaboration, Prototyping (comma-separated)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark optional fields based on model
        self.fields['description'].required = False
        self.fields['national_alignment'].required = False
        self.fields['focus_areas'].required = False
        self.fields['phases'].required = False

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'description', 'location', 'type', 'capacity', 'resources', 'contact_email', 'contact_phone', 'programs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Innovation Hub, IoT Lab...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Overview of the facility and what it offers...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/District or GPS coordinates...'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MakerSpace, Research Lab, University, Virtual Hub...'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max number of people...'}),
            'resources': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Available equipment, tools, or services (comma-separated)...'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'facility@example.com'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+256700000000'}),
            'programs': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark optional fields based on model
        self.fields['description'].required = False
        self.fields['location'].required = False
        self.fields['type'].required = False
        self.fields['capacity'].required = False
        self.fields['resources'].required = False
        self.fields['contact_email'].required = False
        self.fields['contact_phone'].required = False
        self.fields['programs'].required = False

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['facility', 'name', 'capabilities', 'description', 'inventory_code', 'usage_domain', 'support_phase', 'is_operational']
        widgets = {
            'facility': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3D Printer, CNC Machine'}),
            'capabilities': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe what this equipment can do...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Overview of equipment purpose and specifications...'}),
            'inventory_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., EQ-001, PRINTER-3D-A1'}),
            'usage_domain': forms.Select(attrs={'class': 'form-control'}),
            'support_phase': forms.Select(attrs={'class': 'form-control'}),
            'is_operational': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_inventory_code(self):
        inventory_code = self.cleaned_data.get('inventory_code')
        if inventory_code:
            # Convert to uppercase for consistency
            inventory_code = inventory_code.upper()
            # Check if another equipment has this code (excluding current instance during updates)
            existing = Equipment.objects.filter(inventory_code=inventory_code)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('This inventory code is already in use.')
        return inventory_code

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['facility', 'name', 'description', 'category', 'skill_type', 'operating_hours']
        widgets = {
            'facility': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service name...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the service...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'skill_type': forms.Select(attrs={'class': 'form-control'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 9:00 AM - 5:00 PM (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make dropdown fields have proper empty labels
        self.fields['facility'].empty_label = "Select Facility"
        self.fields['category'].empty_label = "Select Category"
        self.fields['skill_type'].empty_label = "Select Skill Type"
        
        # Mark optional fields
        self.fields['description'].required = False
        self.fields['operating_hours'].required = False

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['ProjectId', 'Title', 'Description', 'ArtifactLink', 'OutcomeType', 'QualityCertification', 'CommercializationStatus']
        widgets = {
            'ProjectId': forms.Select(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter outcome title...'}),
            'Description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the outcome...'}),
            'ArtifactLink': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://... (optional)'}),
            'OutcomeType': forms.Select(attrs={'class': 'form-control'}),
            'QualityCertification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quality certification details (optional)...'}),
            'CommercializationStatus': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make dropdown fields optional with empty choice
        self.fields['ProjectId'].empty_label = "Select Project (Optional)"
        self.fields['OutcomeType'].empty_label = "Select Outcome Type"
        self.fields['CommercializationStatus'].empty_label = "Select Status (Optional)"
        
        # Mark optional fields
        self.fields['ProjectId'].required = False
        self.fields['Description'].required = False
        self.fields['ArtifactLink'].required = False
        self.fields['QualityCertification'].required = False
        self.fields['CommercializationStatus'].required = False

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'ProgramId', 'FacilityId', 'Title', 'NatureOfProject', 
            'Description', 'InnovationFocus', 'PrototypeStage', 
            'TestingRequirements', 'CommercializationPlan'
        ]
        widgets = {
            'ProgramId': forms.Select(attrs={'class': 'form-control'}),
            'FacilityId': forms.Select(attrs={'class': 'form-control'}),
            'Title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title...'}),
            'NatureOfProject': forms.Select(attrs={'class': 'form-control'}),
            'Description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe the project goals and objectives...'}),
            'InnovationFocus': forms.Select(attrs={'class': 'form-control'}),
            'PrototypeStage': forms.Select(attrs={'class': 'form-control'}),
            'TestingRequirements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe testing requirements (optional)...'}),
            'CommercializationPlan': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Describe commercialization plan (optional)...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make dropdown fields optional with empty choice
        self.fields['ProgramId'].empty_label = "Select Program (Optional)"
        self.fields['FacilityId'].empty_label = "Select Facility (Optional)"
        self.fields['NatureOfProject'].empty_label = "Select Nature (Optional)"
        self.fields['InnovationFocus'].empty_label = "Select Focus (Optional)"
        self.fields['PrototypeStage'].empty_label = "Select Stage (Optional)"
        
        # Mark optional fields
        self.fields['ProgramId'].required = False
        self.fields['FacilityId'].required = False
        self.fields['NatureOfProject'].required = False
        self.fields['Description'].required = False
        self.fields['InnovationFocus'].required = False
        self.fields['PrototypeStage'].required = False
        self.fields['TestingRequirements'].required = False
        self.fields['CommercializationPlan'].required = False

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'project', 'full_name', 'email', 'affiliation', 'specialization',
            'cross_skill_trained', 'institution', 'role_on_project', 'skill_role'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name...'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address...'}),
            'affiliation': forms.Select(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.Select(attrs={'class': 'form-control'}),
            'role_on_project': forms.Select(attrs={'class': 'form-control'}),
            'skill_role': forms.Select(attrs={'class': 'form-control'}),
            'cross_skill_trained': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make dropdown fields optional with empty choice
        self.fields['project'].empty_label = "Select Project (Optional)"
        self.fields['affiliation'].empty_label = "Select Affiliation (Optional)"
        self.fields['specialization'].empty_label = "Select Specialization (Optional)"
        self.fields['institution'].empty_label = "Select Institution (Optional)"
        self.fields['role_on_project'].empty_label = "Select Role (Optional)"
        self.fields['skill_role'].empty_label = "Select Skill Role (Optional)"
        
        # Mark optional fields
        self.fields['project'].required = False
        self.fields['affiliation'].required = False
        self.fields['specialization'].required = False
        self.fields['institution'].required = False
        self.fields['role_on_project'].required = False
        self.fields['skill_role'].required = False