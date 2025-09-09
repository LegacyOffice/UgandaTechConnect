#!/usr/bin/env python
"""
Test form-model alignment for all entities
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugconnect_project.settings')
django.setup()

from core.models import Program, Facility, Equipment, Project, Service, Participant, Outcome
from core.forms import ProgramForm, FacilityForm, EquipmentForm, ProjectForm, ServiceForm, ParticipantForm, OutcomeForm


def test_form_model_alignment():
    print("=== Testing Form-Model Alignment ===")
    
    # 1. Test Program Form
    print("\n1. Testing ProgramForm...")
    program_data = {
        'name': 'Test Innovation Program',
        'description': 'A comprehensive innovation program',
        'national_alignment': 'Aligned with NDPIII and Vision 2040',
        'focus_areas': 'IoT, AI, Renewable Energy',
        'phases': 'Cross-Skilling, Collaboration, Prototyping'
    }
    
    program_form = ProgramForm(data=program_data)
    if program_form.is_valid():
        program = program_form.save()
        print(f"✓ Program created: {program.name}")
        print(f"  - Fields: name, description, national_alignment, focus_areas, phases")
    else:
        print(f"✗ Program form errors: {program_form.errors}")
        return False
    
    # 2. Test Facility Form
    print("\n2. Testing FacilityForm...")
    facility_data = {
        'name': 'Test Innovation Hub',
        'description': 'Modern innovation facility',
        'location': 'Kampala, Uganda',
        'type': 'Innovation Hub',
        'capacity': 50,
        'resources': '3D Printers, CNC Machines, IoT Kits',
        'contact_email': 'info@testhub.com',
        'contact_phone': '+256700123456',
        'programs': [program.program_id]
    }
    
    facility_form = FacilityForm(data=facility_data)
    if facility_form.is_valid():
        facility = facility_form.save()
        print(f"✓ Facility created: {facility.name}")
        print(f"  - Fields: name, description, location, type, capacity, resources, contact_email, contact_phone, programs")
    else:
        print(f"✗ Facility form errors: {facility_form.errors}")
        return False
    
    # 3. Test Equipment Form
    print("\n3. Testing EquipmentForm...")
    equipment_data = {
        'facility': facility.facility_id,
        'name': 'Ultimaker S3 3D Printer',
        'capabilities': 'PLA/ABS printing, 0.1mm precision',
        'description': 'Professional grade 3D printer',
        'inventory_code': 'ULT-S3-001',
        'usage_domain': 'ELECTRONICS',
        'support_phase': 'PROTOTYPING',
        'is_operational': True
    }
    
    equipment_form = EquipmentForm(data=equipment_data)
    if equipment_form.is_valid():
        equipment = equipment_form.save()
        print(f"✓ Equipment created: {equipment.name}")
        print(f"  - Fields: facility, name, capabilities, description, inventory_code, usage_domain, support_phase, is_operational")
    else:
        print(f"✗ Equipment form errors: {equipment_form.errors}")
        return False
    
    # 4. Test Project Form
    print("\n4. Testing ProjectForm...")
    project_data = {
        'ProgramId': program.program_id,
        'FacilityId': facility.facility_id,
        'Title': 'Smart Agriculture IoT System',
        'NatureOfProject': 'prototype',
        'Description': 'IoT-based agricultural monitoring system',
        'InnovationFocus': 'iot',
        'PrototypeStage': 'concept',
        'TestingRequirements': 'Field testing required',
        'CommercializationPlan': 'Partner with agricultural cooperatives'
    }
    
    project_form = ProjectForm(data=project_data)
    if project_form.is_valid():
        project = project_form.save()
        print(f"✓ Project created: {project.Title}")
        print(f"  - Fields: ProgramId, FacilityId, Title, NatureOfProject, Description, InnovationFocus, PrototypeStage, TestingRequirements, CommercializationPlan")
    else:
        print(f"✗ Project form errors: {project_form.errors}")
        return False
    
    # 5. Test Service Form
    print("\n5. Testing ServiceForm...")
    service_data = {
        'facility': facility.facility_id,
        'name': '3D Printing Service',
        'description': 'Professional 3D printing for prototypes',
        'category': 'FABRICATION',
        'skill_type': 'HARDWARE',
        'operating_hours': '9:00 AM - 5:00 PM'
    }
    
    service_form = ServiceForm(data=service_data)
    if service_form.is_valid():
        service = service_form.save()
        print(f"✓ Service created: {service.name}")
        print(f"  - Fields: facility, name, description, category, skill_type, operating_hours")
    else:
        print(f"✗ Service form errors: {service_form.errors}")
        return False
    
    # 6. Test Participant Form
    print("\n6. Testing ParticipantForm...")
    participant_data = {
        'project': project.ProjectId,
        'full_name': 'Alice Johnson',
        'email': 'alice.johnson@example.com',
        'affiliation': 'CS',
        'specialization': 'Software',
        'cross_skill_trained': False,
        'institution': 'SCIT',
        'role_on_project': 'Student',
        'skill_role': 'Developer'
    }
    
    participant_form = ParticipantForm(data=participant_data)
    if participant_form.is_valid():
        participant = participant_form.save()
        print(f"✓ Participant created: {participant.full_name}")
        print(f"  - Fields: project, full_name, email, affiliation, specialization, cross_skill_trained, institution, role_on_project, skill_role")
    else:
        print(f"✗ Participant form errors: {participant_form.errors}")
        return False
    
    # 7. Test Outcome Form
    print("\n7. Testing OutcomeForm...")
    outcome_data = {
        'ProjectId': project.ProjectId,
        'Title': 'IoT Prototype Device',
        'Description': 'Working prototype of the IoT monitoring system',
        'ArtifactLink': 'https://github.com/example/iot-prototype',
        'OutcomeType': 'Prototype',
        'QualityCertification': 'ISO 9001 certified',
        'CommercializationStatus': 'Demoed'
    }
    
    outcome_form = OutcomeForm(data=outcome_data)
    if outcome_form.is_valid():
        outcome = outcome_form.save()
        print(f"✓ Outcome created: {outcome.Title}")
        print(f"  - Fields: ProjectId, Title, Description, ArtifactLink, OutcomeType, QualityCertification, CommercializationStatus")
    else:
        print(f"✗ Outcome form errors: {outcome_form.errors}")
        return False
    
    print("\n=== Form-Model Alignment Test Summary ===")
    print(f"Programs: {Program.objects.count()}")
    print(f"Facilities: {Facility.objects.count()}")
    print(f"Equipment: {Equipment.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Services: {Service.objects.count()}")
    print(f"Participants: {Participant.objects.count()}")
    print(f"Outcomes: {Outcome.objects.count()}")
    
    print("\n✅ All forms are properly aligned with their models!")
    return True


if __name__ == "__main__":
    success = test_form_model_alignment()
    sys.exit(0 if success else 1)
