#!/usr/bin/env python
"""
Equipment functionality test script
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugconnect_project.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from core.models import Facility, Equipment
from core.forms import EquipmentForm


def test_equipment_functionality():
    print("=== Equipment Functionality Test ===")
    
    # 1. Test Model Creation
    print("\n1. Testing Equipment Model...")
    
    # Create a facility first
    facility, created = Facility.objects.get_or_create(
        name='Test Innovation Lab',
        defaults={
            'location': 'Kampala, Uganda',
            'contact_person': 'John Doe',
            'email': 'john@lab.com',
            'phone': '+256700123456',
            'description': 'A test innovation laboratory'
        }
    )
    print(f"✓ Using facility: {facility.name} ({'created' if created else 'existing'})")
    
    # Test equipment creation
    try:
        equipment = Equipment.objects.create(
            facility=facility,
            name='3D Printer Ultimaker S3',
            capabilities='PLA/ABS/PETG printing, 0.1mm layer resolution, 230x190x200mm build volume',
            description='Professional 3D printer for rapid prototyping and small batch production',
            inventory_code='ULT-S3-001',
            usage_domain='ELECTRONICS',
            support_phase='PROTOTYPING',
            is_operational=True
        )
        print(f"✓ Created equipment: {equipment.name} (ID: {equipment.equipment_id})")
    except Exception as e:
        print(f"✗ Equipment creation failed: {e}")
        return False
    
    # 2. Test Form Validation
    print("\n2. Testing Equipment Form...")
    
    form_data = {
        'facility': facility.facility_id,
        'name': 'CNC Milling Machine',
        'capabilities': 'Aluminum/Steel machining, ±0.05mm precision',
        'description': 'Computer-controlled milling machine for precision parts',
        'inventory_code': 'cnc-mill-001',  # Test case conversion
        'usage_domain': 'MECHANICAL',
        'support_phase': 'PROTOTYPING',
        'is_operational': True
    }
    
    form = EquipmentForm(data=form_data)
    if form.is_valid():
        equipment2 = form.save()
        print(f"✓ Form validation passed. Created: {equipment2.name}")
        print(f"✓ Inventory code converted to: {equipment2.inventory_code}")
    else:
        print(f"✗ Form validation failed: {form.errors}")
        return False
    
    # 3. Test URL Access
    print("\n3. Testing Equipment URLs...")
    
    client = Client()
    
    # Test equipment list
    try:
        response = client.get(reverse('core:equipment_list'))
        print(f"✓ Equipment list page: {response.status_code}")
    except Exception as e:
        print(f"✗ Equipment list failed: {e}")
        return False
    
    # Test equipment detail
    try:
        response = client.get(reverse('core:equipment_detail', kwargs={'pk': equipment.equipment_id}))
        print(f"✓ Equipment detail page: {response.status_code}")
    except Exception as e:
        print(f"✗ Equipment detail failed: {e}")
        return False
    
    # Test equipment create
    try:
        response = client.get(reverse('core:equipment_create'))
        print(f"✓ Equipment create page: {response.status_code}")
    except Exception as e:
        print(f"✗ Equipment create failed: {e}")
        return False
    
    # 4. Test Equipment Count
    print(f"\n4. Total Equipment Count: {Equipment.objects.count()}")
    
    # 5. Test Equipment List with Filters
    print("\n5. Testing Equipment Queries...")
    electronics_equipment = Equipment.objects.filter(usage_domain='ELECTRONICS').count()
    mechanical_equipment = Equipment.objects.filter(usage_domain='MECHANICAL').count()
    operational_equipment = Equipment.objects.filter(is_operational=True).count()
    
    print(f"✓ Electronics equipment: {electronics_equipment}")
    print(f"✓ Mechanical equipment: {mechanical_equipment}")
    print(f"✓ Operational equipment: {operational_equipment}")
    
    print("\n=== Equipment Functionality Test PASSED ===")
    return True


if __name__ == "__main__":
    success = test_equipment_functionality()
    sys.exit(0 if success else 1)
