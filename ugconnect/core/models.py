
from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.urls import reverse

class Program(models.Model):
    """
    Represents the collaboration umbrella under which projects run.
    """
    program_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, help_text="Program name")
    description = models.TextField(blank=True, help_text="Overview of the program's purpose")
    national_alignment = models.TextField(blank=True, help_text="Link to NDPIII, Roadmap, or 4IR goals")
    focus_areas = models.CharField(max_length=255, blank=True, help_text="Domains such as IoT, automation, renewable energy (comma-separated)")
    phases = models.CharField(max_length=255, blank=True, help_text="E.g., Cross-Skilling, Collaboration, Prototyping (comma-separated)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        """
        Returns a string representation of the Program, which is useful in the Django admin site.
        """
        return self.name

    class Meta:
        ordering = ['name']



# FACILITY MODEL 


class Facility(models.Model):
    """
    Represents an innovation or collaboration space (physical or virtual)
    that supports technology programs.
    """
    facility_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True, help_text="Facility name e.g. Innovation Hub, IoT Lab")
    description = models.TextField(blank=True, help_text="Overview of the facility and what it offers")
    location = models.CharField(max_length=255, blank=True, help_text="City/District or GPS coordinates")
    type = models.CharField(max_length=100, blank=True, help_text="Type e.g. MakerSpace, Research Lab, University, Virtual Hub")
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Max number of people the facility can accommodate")
    resources = models.TextField(blank=True, help_text="Available equipment, tools, or services (comma-separated)")
    contact_email = models.EmailField(blank=True, help_text="Facility contact email")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Facility contact phone")

    # Relationship with Program (many-to-many)
    programs = models.ManyToManyField('Program', related_name="facilities", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Equipment(models.Model):
    """
    Represents machinery/tools available at a facility.
    Based on the capstone requirements.
    """
    
    USAGE_DOMAINS = [
        ('ELECTRONICS', 'Electronics'),
        ('MECHANICAL', 'Mechanical'),
        ('IOT', 'IoT'),
        ('SOFTWARE', 'Software'),
        ('TESTING', 'Testing'),
        ('FABRICATION', 'Fabrication'),
    ]
    
    SUPPORT_PHASES = [
        ('TRAINING', 'Training'),
        ('PROTOTYPING', 'Prototyping'),
        ('TESTING', 'Testing'),
        ('COMMERCIALIZATION', 'Commercialization'),
    ]
    
    equipment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        'Facility',  # Reference to your existing Facility model
        on_delete=models.CASCADE,
        related_name='equipment_set',
        help_text="Facility that owns this equipment"
    )
    name = models.CharField(
        max_length=200,
        help_text="Equipment name (e.g., '3D Printer', 'CNC Machine')"
    )
    capabilities = models.TextField(
        blank=True,
        help_text="Functions it can perform (e.g., 'PLA/ABS printing, 0.1mm precision')"
    )
    description = models.TextField(
        blank=True,
        help_text="Overview of equipment purpose and specifications"
    )
    inventory_code = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[A-Z0-9\-_]+$',
            message='Inventory code must contain only uppercase letters, numbers, hyphens, and underscores'
        )],
        help_text="Tracking code (e.g., 'EQ-CNC-001', 'PRINTER-3D-A2')"
    )
    usage_domain = models.CharField(
        max_length=20,
        choices=USAGE_DOMAINS,
        help_text="Primary domain this equipment serves"
    )
    support_phase = models.CharField(
        max_length=20,
        choices=SUPPORT_PHASES,
        help_text="Which project phase this equipment primarily supports"
    )
    is_operational = models.BooleanField(
        default=True,
        help_text="Whether equipment is currently operational"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.facility.name})"
    
    def clean(self):
        """Custom validation"""
        from django.core.exceptions import ValidationError
        
        if self.inventory_code:
            # Ensure inventory code is uppercase
            self.inventory_code = self.inventory_code.upper()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Equipment"
        ordering = ['facility__name', 'name']

class Project(models.Model):
    NATURE_CHOICES = [
        ('research', 'Research'),
        ('prototype', 'Prototype'),
        ('applied', 'Applied Work'),
    ]
    
    INNOVATION_CHOICES = [
        ('iot', 'IoT Devices'),
        ('smart_home', 'Smart Home'),
        ('renewable_energy', 'Renewable Energy'),
        ('other', 'Other'),
    ]
    
    STAGE_CHOICES = [
        ('concept', 'Concept'),
        ('prototype', 'Prototype'),
        ('mvp', 'MVP'),
        ('market_launch', 'Market Launch'),
    ]
    
    ProjectId = models.AutoField(primary_key=True)
    ProgramId = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='projects')
    FacilityId = models.ForeignKey('Facility', on_delete=models.CASCADE, related_name='projects')
    Title = models.CharField(max_length=200)
    NatureOfProject = models.CharField(max_length=20, choices=NATURE_CHOICES)
    Description = models.TextField()
    InnovationFocus = models.CharField(max_length=20, choices=INNOVATION_CHOICES)
    PrototypeStage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    TestingRequirements = models.TextField()
    CommercializationPlan = models.TextField()
    
    def __str__(self):
        return self.Title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.ProjectId})
    
class Service(models.Model):
    """
    Represents the types of work a facility can perform.
    """
    CATEGORY_CHOICES = [
        ('MACHINING', 'Machining'),
        ('TESTING', 'Testing'),
        ('TRAINING', 'Training'),
        ('FABRICATION', 'Fabrication'),
        ('CONSULTANCY', 'Consultancy'),
    ]

    SKILL_TYPE_CHOICES = [
        ('HARDWARE', 'Hardware'),
        ('SOFTWARE', 'Software'),
        ('INTEGRATION', 'Integration'),
        ('MULTIDISCIPLINARY', 'Multidisciplinary'),
    ]

    service_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.CASCADE,
        related_name='services',
        help_text="Facility that offers this service"
    )
    name = models.CharField(max_length=200, help_text="Service name (e.g., CNC machining, PCB fabrication)")
    description = models.TextField(blank=True, help_text="Details of what the service does")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, help_text="Category of the service")
    skill_type = models.CharField(max_length=50, choices=SKILL_TYPE_CHOICES, help_text="Skill type supported by this service")
    operating_hours = models.CharField(max_length=50, blank=True, null=True, help_text="E.g., 9:00 AM - 5:00 PM"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.facility.name})"

    class Meta:
        ordering = ['facility__name', 'name']
        
        

class Participant(models.Model):
    AFFILIATION_CHOICES = [
        ('CS', 'Computer Science'),
        ('SE', 'Software Engineering'),
        ('Engineering', 'Engineering'),
        ('Other', 'Other'),
    ]

    SPECIALIZATION_CHOICES = [
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Business', 'Business'),
    ]

    INSTITUTION_CHOICES = [
        ('SCIT', 'SCIT'),
        ('CEDAT', 'CEDAT'),
        ('UniPod', 'UniPod'),
        ('UIRI', 'UIRI'),
        ('Lwera', 'Lwera'),
    ]

    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Lecturer', 'Lecturer'),
        ('Contributor', 'Contributor'),
    ]

    SKILL_ROLE_CHOICES = [
        ('Developer', 'Developer'),
        ('Engineer', 'Engineer'),
        ('Designer', 'Designer'),
        ('Business Lead', 'Business Lead'),
    ]

    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='participants')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=50, choices=AFFILIATION_CHOICES)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    cross_skill_trained = models.BooleanField(default=False)
    institution = models.CharField(max_length=100, choices=INSTITUTION_CHOICES)
    role_on_project = models.CharField(max_length=50, choices=ROLE_CHOICES)
    skill_role = models.CharField(max_length=50, choices=SKILL_ROLE_CHOICES)

    def __str__(self):
        return self.full_name
