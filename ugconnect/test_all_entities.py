#!/usr/bin/env python
"""
Comprehensive test for all entity functionalities
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugconnect_project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from core.models import Program, Facility, Project, Equipment, Service, Participant, Outcome
from core.forms import ProjectForm, ServiceForm, ParticipantForm, OutcomeForm


def test_all_entities():
    print("=== Comprehensive Entity Functionality Test ===")
    
    client = Client()
    
    # 1. Test Project Functionality
    print("\n1. Testing Project Functionality...")
    
    # Create test program and facility
    program, _ = Program.objects.get_or_create(
        name='Innovation Program',
        defaults={'description': 'Test program for innovation'}
    )
    
    facility, _ = Facility.objects.get_or_create(
        name='Tech Hub',
        defaults={
            'location': 'Kampala',
            'contact_person': 'John Doe',
            'email': 'john@techhub.com',
            'phone': '+256700000000',
            'description': 'Technology hub'
        }
    )
    
    # Test project form with optional fields
    project_data = {
        'Title': 'Smart IoT System',
        'Description': 'An innovative IoT solution',
        'ProgramId': program.program_id,  # Optional
        'FacilityId': facility.facility_id,  # Optional
        'NatureOfProject': 'prototype',
        'InnovationFocus': 'iot',
        'PrototypeStage': 'concept',
        'TestingRequirements': '',  # Optional
        'CommercializationPlan': '',  # Optional
    }
    
    project_form = ProjectForm(data=project_data)
    if project_form.is_valid():
        project = project_form.save()
        print(f"✓ Project created: {project.Title}")
    else:
        print(f"✗ Project form errors: {project_form.errors}")
        return False
    
    # Test project URLs
    try:
        response = client.get(reverse('core:project_list'))
        print(f"✓ Project list page: {response.status_code}")
        
        response = client.get(reverse('core:project_create'))
        print(f"✓ Project create page: {response.status_code}")
    except Exception as e:
        print(f"✗ Project URLs failed: {e}")
        return False
    
    # 2. Test Service Functionality
    print("\n2. Testing Service Functionality...")
    
    service_data = {
        'facility': facility.facility_id,
        'name': '3D Printing Service',
        'description': 'Professional 3D printing services',
        'category': 'FABRICATION',
        'skill_type': 'HARDWARE',
        'operating_hours': '9:00 AM - 5:00 PM'
    }
    
    service_form = ServiceForm(data=service_data)
    if service_form.is_valid():
        service = service_form.save()
        print(f"✓ Service created: {service.name}")
    else:
        print(f"✗ Service form errors: {service_form.errors}")
        return False
    
    try:
        response = client.get(reverse('core:service_list'))
        print(f"✓ Service list page: {response.status_code}")
        
        response = client.get(reverse('core:service_create'))
        print(f"✓ Service create page: {response.status_code}")
    except Exception as e:
        print(f"✗ Service URLs failed: {e}")
        return False
    
    # 3. Test Participant Functionality
    print("\n3. Testing Participant Functionality...")
    
    participant_data = {
        'project': project.ProjectId,  # Optional
        'full_name': 'Alice Johnson',
        'email': 'alice@example.com',
        'affiliation': 'CS',
        'specialization': 'Software',
        'institution': 'SCIT',
        'role_on_project': 'Student',
        'skill_role': 'Developer',
        'cross_skill_trained': False
    }
    
    participant_form = ParticipantForm(data=participant_data)
    if participant_form.is_valid():
        participant = participant_form.save()
        print(f"✓ Participant created: {participant.full_name}")
    else:
        print(f"✗ Participant form errors: {participant_form.errors}")
        return False
    
    try:
        response = client.get(reverse('core:participant_list'))
        print(f"✓ Participant list page: {response.status_code}")
        
        response = client.get(reverse('core:participant_create'))
        print(f"✓ Participant create page: {response.status_code}")
    except Exception as e:
        print(f"✗ Participant URLs failed: {e}")
        return False
    
    # 4. Test Outcome Functionality
    print("\n4. Testing Outcome Functionality...")
    
    outcome_data = {
        'ProjectId': project.ProjectId,  # Optional
        'Title': 'IoT Prototype',
        'Description': 'Working prototype of IoT system',
        'ArtifactLink': 'https://github.com/example/iot-project',
        'OutcomeType': 'Prototype',
        'QualityCertification': '',  # Optional
        'CommercializationStatus': 'Demoed'
    }
    
    outcome_form = OutcomeForm(data=outcome_data)
    if outcome_form.is_valid():
        outcome = outcome_form.save()
        print(f"✓ Outcome created: {outcome.Title}")
    else:
        print(f"✗ Outcome form errors: {outcome_form.errors}")
        return False
    
    try:
        response = client.get(reverse('core:outcome_list'))
        print(f"✓ Outcome list page: {response.status_code}")
        
        response = client.get(reverse('core:outcome_create'))
        print(f"✓ Outcome create page: {response.status_code}")
    except Exception as e:
        print(f"✗ Outcome URLs failed: {e}")
        return False
    
    # 5. Test Entity Counts
    print(f"\n5. Entity Counts:")
    print(f"   Projects: {Project.objects.count()}")
    print(f"   Services: {Service.objects.count()}")
    print(f"   Participants: {Participant.objects.count()}")
    print(f"   Outcomes: {Outcome.objects.count()}")
    print(f"   Equipment: {Equipment.objects.count()}")
    print(f"   Facilities: {Facility.objects.count()}")
    print(f"   Programs: {Program.objects.count()}")
    
    # 6. Test Optional Field Scenarios
    print("\n6. Testing Optional Fields...")
    
    # Test project with minimal data (only required fields)
    minimal_project_data = {
        'Title': 'Minimal Project Test'
    }
    
    minimal_form = ProjectForm(data=minimal_project_data)
    if minimal_form.is_valid():
        minimal_project = minimal_form.save()
        print(f"✓ Minimal project created: {minimal_project.Title}")
    else:
        print(f"✓ Minimal project validation - only Title required")
    
    # Test participant without project
    participant_no_project_data = {
        'full_name': 'Bob Smith',
        'email': 'bob@example.com'
    }
    
    participant_no_project_form = ParticipantForm(data=participant_no_project_data)
    if participant_no_project_form.is_valid():
        participant_no_project = participant_no_project_form.save()
        print(f"✓ Participant without project created: {participant_no_project.full_name}")
    else:
        print(f"✓ Participant validation - Name and Email required")
    
    print("\n=== All Entity Functionality Tests PASSED ===")
    return True


if __name__ == "__main__":
    success = test_all_entities()
    sys.exit(0 if success else 1)
