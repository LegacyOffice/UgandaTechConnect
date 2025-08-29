
from django.db import models
import uuid

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
