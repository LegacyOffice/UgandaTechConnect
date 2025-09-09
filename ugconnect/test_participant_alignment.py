#!/usr/bin/env python
"""
Test Participant Form-Model-Template Alignment
"""
import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugconnect_project.settings')
django.setup()

from core.models import Participant
from core.forms import ParticipantForm

def test_participant_alignment():
    """Test participant form-model alignment"""
    print("🧪 Testing Participant Form-Model-Template Alignment")
    print("=" * 60)
    
    # Get model field info
    participant_fields = [f.name for f in Participant._meta.get_fields() 
                         if not f.many_to_many and not f.one_to_many and f.name != 'id']
    
    # Get form fields
    form = ParticipantForm()
    form_fields = list(form.fields.keys())
    
    print(f"📋 Participant Model Fields: {participant_fields}")
    print(f"📝 Participant Form Fields: {form_fields}")
    
    # Check choice fields
    choice_fields = ['affiliation', 'specialization', 'institution', 'role_on_project', 'skill_role']
    print(f"\n🎯 Choice Fields Validation:")
    
    for field_name in choice_fields:
        if field_name in form.fields:
            field = form.fields[field_name]
            print(f"  ✅ {field_name}: {type(field).__name__}")
            if hasattr(field, 'choices'):
                choices = list(field.choices)[:6]  # Show first 6 choices
                print(f"     Choices: {choices}")
        else:
            print(f"  ❌ {field_name}: Missing from form")
    
    # Check widget types
    print(f"\n🎨 Widget Types:")
    for field_name, field in form.fields.items():
        widget_type = type(field.widget).__name__
        print(f"  {field_name}: {widget_type}")
    
    # Check if all model choice fields are properly handled
    model_choice_fields = []
    for field in Participant._meta.get_fields():
        if hasattr(field, 'choices') and field.choices:
            model_choice_fields.append(field.name)
    
    print(f"\n🔍 Model Choice Fields: {model_choice_fields}")
    
    # Alignment check
    model_set = set(participant_fields)
    form_set = set(form_fields)
    
    missing_in_form = model_set - form_set
    extra_in_form = form_set - model_set
    
    if missing_in_form:
        print(f"\n⚠️  Fields missing in form: {missing_in_form}")
    if extra_in_form:
        print(f"⚠️  Extra fields in form: {extra_in_form}")
    
    if not missing_in_form and not extra_in_form:
        print(f"\n✅ Perfect Alignment! All model fields are in the form.")
    
    print(f"\n🎉 Participant form-model alignment test complete!")

if __name__ == '__main__':
    test_participant_alignment()
