
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