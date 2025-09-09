#!/usr/bin/env python
"""
Create sample data for testing dropdowns
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ugconnect_project.settings')
django.setup()

from core.models import Program, Facility, Project, Equipment, Service, Participant, Outcome


def create_sample_data():
    print("Creating sample data for testing...")
    
    # Create sample programs
    programs_data = [
        {'name': 'Innovation Bootcamp 2025', 'description': 'Intensive innovation program for entrepreneurs'},
        {'name': 'Tech Skills Development', 'description': 'Technical skills training program'},
        {'name': 'Startup Incubation', 'description': 'Business incubation for early-stage startups'},
        {'name': 'Digital Health Initiative', 'description': 'Healthcare technology development program'},
        {'name': 'AgTech Innovation Hub', 'description': 'Agricultural technology advancement program'},
        {'name': 'FinTech Accelerator', 'description': 'Financial technology innovation program'},
        {'name': 'Green Tech Solutions', 'description': 'Environmental technology development initiative'},
        {'name': 'EdTech Platform', 'description': 'Educational technology innovation program'},
        {'name': 'Smart City Projects', 'description': 'Urban technology and IoT solutions program'},
        {'name': 'Cybersecurity Excellence', 'description': 'Information security and cyber defense program'}
    ]
    
    for prog_data in programs_data:
        program, created = Program.objects.get_or_create(
            name=prog_data['name'],
            defaults={'description': prog_data['description']}
        )
        if created:
            print(f"✓ Created program: {program.name}")
    
    # Create sample facilities
    facilities_data = [
        {
            'name': 'Makerere Innovation Lab',
            'location': 'Kampala, Uganda',
            'contact_person': 'Dr. Sarah Kanyesigye',
            'email': 'sarah@makerereinnovation.com',
            'phone': '+256700123456',
            'description': 'Primary innovation facility at Makerere University'
        },
        {
            'name': 'Outbox Hub',
            'location': 'Kampala, Uganda',
            'contact_person': 'John Birigwa',
            'email': 'john@outbox.co.ug',
            'phone': '+256700654321',
            'description': 'Technology and innovation hub in Kampala'
        },
        {
            'name': 'UIRI Research Center',
            'location': 'Nakawa, Uganda',
            'contact_person': 'Prof. Moses Musinguzi',
            'email': 'moses@uiri.org',
            'phone': '+256700987654',
            'description': 'Uganda Industrial Research Institute facility'
        },
        {
            'name': 'Kiira Motors Innovation Hub',
            'location': 'Jinja, Uganda',
            'contact_person': 'Eng. Paul Musasizi',
            'email': 'paul@kiira-motors.com',
            'phone': '+256700111222',
            'description': 'Automotive and mechanical engineering innovation facility'
        },
        {
            'name': 'Kampala Innovation City',
            'location': 'Nakawa, Kampala',
            'contact_person': 'Dr. Grace Mirembe',
            'email': 'grace@kic.ug',
            'phone': '+256700333444',
            'description': 'Modern tech incubation and co-working facility'
        },
        {
            'name': 'Mbarara Tech Hub',
            'location': 'Mbarara, Uganda',
            'contact_person': 'James Tumwebaze',
            'email': 'james@mbarara-tech.ug',
            'phone': '+256700555666',
            'description': 'Regional technology development center in Western Uganda'
        },
        {
            'name': 'Gulu Innovation Lab',
            'location': 'Gulu, Uganda',
            'contact_person': 'Mary Achola',
            'email': 'mary@gulu-innovation.ug',
            'phone': '+256700777888',
            'description': 'Northern Uganda technology and innovation facility'
        },
        {
            'name': 'Digital Health Lab - Mulago',
            'location': 'Mulago, Kampala',
            'contact_person': 'Dr. Robert Ssekitoleko',
            'email': 'robert@digitalhealth.ug',
            'phone': '+256700999000',
            'description': 'Specialized healthcare technology development facility'
        },
        {
            'name': 'Agricultural Innovation Center',
            'location': 'Entebbe, Uganda',
            'contact_person': 'Prof. Agnes Nabukenya',
            'email': 'agnes@agric-innovation.ug',
            'phone': '+256701111222',
            'description': 'Agricultural technology and innovation research center'
        },
        {
            'name': 'FinTech Development Lab',
            'location': 'Kololo, Kampala',
            'contact_person': 'Samuel Kayongo',
            'email': 'samuel@fintech-lab.ug',
            'phone': '+256701333444',
            'description': 'Financial technology development and testing facility'
        }
    ]
    
    for fac_data in facilities_data:
        facility, created = Facility.objects.get_or_create(
            name=fac_data['name'],
            defaults=fac_data
        )
        if created:
            print(f"✓ Created facility: {facility.name}")
    
    # Create sample projects
    programs = list(Program.objects.all())
    facilities = list(Facility.objects.all())
    
    if programs and facilities:
        projects_data = [
            {
                'Title': 'Smart Agriculture IoT System',
                'Description': 'IoT-based monitoring system for agricultural productivity',
                'ProgramId': programs[0] if len(programs) > 0 else programs[0],
                'FacilityId': facilities[0] if len(facilities) > 0 else facilities[0],
                'NatureOfProject': 'PROTOTYPE',
                'InnovationFocus': 'IoT sensors for soil moisture and crop health monitoring',
                'PrototypeStage': 'CONCEPT',
                'TestingRequirements': 'Field testing on multiple crop types',
                'CommercializationPlan': 'Partner with agricultural cooperatives'
            },
            {
                'Title': 'Mobile Health Platform',
                'Description': 'Digital health platform for rural communities',
                'ProgramId': programs[1] if len(programs) > 1 else programs[0],
                'FacilityId': facilities[1] if len(facilities) > 1 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Telemedicine and remote patient monitoring',
                'PrototypeStage': 'DEVELOPMENT',
                'TestingRequirements': 'Clinical trials and user acceptance testing',
                'CommercializationPlan': 'Licensing to healthcare providers'
            },
            {
                'Title': 'Blockchain Supply Chain Tracker',
                'Description': 'Transparent supply chain tracking using blockchain technology',
                'ProgramId': programs[2] if len(programs) > 2 else programs[0],
                'FacilityId': facilities[2] if len(facilities) > 2 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Blockchain for agricultural product traceability',
                'PrototypeStage': 'PROTOTYPE',
                'TestingRequirements': 'Integration testing with existing systems',
                'CommercializationPlan': 'SaaS model for export companies'
            },
            {
                'Title': 'Solar Water Pumping System',
                'Description': 'Solar-powered water pumping solution for rural areas',
                'ProgramId': programs[3] if len(programs) > 3 else programs[0],
                'FacilityId': facilities[3] if len(facilities) > 3 else facilities[0],
                'NatureOfProject': 'HARDWARE',
                'InnovationFocus': 'Renewable energy for water access',
                'PrototypeStage': 'TESTING',
                'TestingRequirements': 'Performance testing in various weather conditions',
                'CommercializationPlan': 'Direct sales and microfinance partnerships'
            },
            {
                'Title': 'E-Learning Platform for Primary Schools',
                'Description': 'Interactive digital learning platform with offline capabilities',
                'ProgramId': programs[4] if len(programs) > 4 else programs[0],
                'FacilityId': facilities[4] if len(facilities) > 4 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Educational technology for rural schools',
                'PrototypeStage': 'TESTING',
                'TestingRequirements': 'Pilot testing in 10 schools',
                'CommercializationPlan': 'Government partnerships and NGO distribution'
            },
            {
                'Title': 'Waste Management IoT Solution',
                'Description': 'Smart waste collection and management system',
                'ProgramId': programs[5] if len(programs) > 5 else programs[0],
                'FacilityId': facilities[5] if len(facilities) > 5 else facilities[0],
                'NatureOfProject': 'HARDWARE',
                'InnovationFocus': 'IoT sensors for waste bin monitoring',
                'PrototypeStage': 'PROTOTYPE',
                'TestingRequirements': 'Deployment in Kampala city areas',
                'CommercializationPlan': 'Municipal contracts and private sector sales'
            },
            {
                'Title': 'Financial Inclusion Mobile App',
                'Description': 'Mobile banking solution for unbanked populations',
                'ProgramId': programs[6] if len(programs) > 6 else programs[0],
                'FacilityId': facilities[6] if len(facilities) > 6 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Mobile money and micro-lending platform',
                'PrototypeStage': 'DEVELOPMENT',
                'TestingRequirements': 'Security testing and regulatory compliance',
                'CommercializationPlan': 'Partnership with telecom operators'
            },
            {
                'Title': 'Drone-based Crop Monitoring',
                'Description': 'Agricultural drone system for crop health assessment',
                'ProgramId': programs[7] if len(programs) > 7 else programs[0],
                'FacilityId': facilities[7] if len(facilities) > 7 else facilities[0],
                'NatureOfProject': 'HARDWARE',
                'InnovationFocus': 'AI-powered crop health analysis',
                'PrototypeStage': 'TESTING',
                'TestingRequirements': 'Flight testing and image analysis validation',
                'CommercializationPlan': 'Service provider model for large farms'
            },
            {
                'Title': 'Cybersecurity Training Platform',
                'Description': 'Online cybersecurity education and certification platform',
                'ProgramId': programs[8] if len(programs) > 8 else programs[0],
                'FacilityId': facilities[8] if len(facilities) > 8 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Interactive cybersecurity simulation training',
                'PrototypeStage': 'DEVELOPMENT',
                'TestingRequirements': 'Beta testing with IT professionals',
                'CommercializationPlan': 'Subscription model for enterprises'
            },
            {
                'Title': 'Smart Traffic Management System',
                'Description': 'AI-powered traffic flow optimization system',
                'ProgramId': programs[9] if len(programs) > 9 else programs[0],
                'FacilityId': facilities[9] if len(facilities) > 9 else facilities[0],
                'NatureOfProject': 'SOFTWARE',
                'InnovationFocus': 'Machine learning for traffic optimization',
                'PrototypeStage': 'CONCEPT',
                'TestingRequirements': 'Simulation testing and pilot deployment',
                'CommercializationPlan': 'Municipal government contracts'
            }
        ]
        
        created_projects = []
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                Title=proj_data['Title'],
                defaults=proj_data
            )
            if created:
                print(f"✓ Created project: {project.Title}")
                created_projects.append(project)
    
    # Create sample equipment
    equipment_data = [
        {
            'facility': facilities[0] if facilities else None,
            'name': '3D Printer - Ultimaker S5',
            'capabilities': 'Dual extrusion, multiple materials, high precision printing',
            'description': 'Professional-grade 3D printer for prototyping',
            'inventory_code': 'EQ-001',
            'usage_domain': 'PROTOTYPING',
            'support_phase': 'DESIGN_DEVELOPMENT',
            'is_operational': True
        },
        {
            'facility': facilities[1] if len(facilities) > 1 else facilities[0],
            'name': 'CNC Milling Machine',
            'capabilities': 'Precision machining, multi-axis control, metal and plastic',
            'description': 'Computer-controlled milling machine',
            'inventory_code': 'EQ-002',
            'usage_domain': 'MANUFACTURING',
            'support_phase': 'PROTOTYPING',
            'is_operational': True
        },
        {
            'facility': facilities[2] if len(facilities) > 2 else facilities[0],
            'name': 'Oscilloscope - Tektronix',
            'capabilities': 'Multi-channel analysis, high frequency, digital storage',
            'description': 'Digital oscilloscope for circuit analysis',
            'inventory_code': 'EQ-003',
            'usage_domain': 'ELECTRONICS',
            'support_phase': 'TESTING_VALIDATION',
            'is_operational': True
        },
        {
            'facility': facilities[3] if len(facilities) > 3 else facilities[0],
            'name': 'Solar Panel Tester',
            'capabilities': 'IV curve analysis, efficiency measurement, outdoor testing',
            'description': 'Equipment for testing solar panel performance',
            'inventory_code': 'EQ-004',
            'usage_domain': 'RENEWABLE_ENERGY',
            'support_phase': 'TESTING_VALIDATION',
            'is_operational': True
        },
        {
            'facility': facilities[4] if len(facilities) > 4 else facilities[0],
            'name': 'High-Performance Computing Cluster',
            'capabilities': 'Parallel processing, machine learning, data analysis',
            'description': 'Computing cluster for AI and data processing',
            'inventory_code': 'EQ-005',
            'usage_domain': 'SOFTWARE',
            'support_phase': 'DESIGN_DEVELOPMENT',
            'is_operational': True
        },
        {
            'facility': facilities[5] if len(facilities) > 5 else facilities[0],
            'name': 'IoT Sensor Development Kit',
            'capabilities': 'Multiple sensor types, wireless connectivity, data logging',
            'description': 'Comprehensive IoT development platform',
            'inventory_code': 'EQ-006',
            'usage_domain': 'IOT',
            'support_phase': 'PROTOTYPING',
            'is_operational': True
        },
        {
            'facility': facilities[6] if len(facilities) > 6 else facilities[0],
            'name': 'Network Security Appliance',
            'capabilities': 'Firewall, intrusion detection, traffic analysis',
            'description': 'Enterprise-grade security testing equipment',
            'inventory_code': 'EQ-007',
            'usage_domain': 'SOFTWARE',
            'support_phase': 'SECURITY_TESTING',
            'is_operational': True
        },
        {
            'facility': facilities[7] if len(facilities) > 7 else facilities[0],
            'name': 'Agricultural Drone',
            'capabilities': 'Crop monitoring, precision spraying, GPS mapping',
            'description': 'Professional agricultural drone system',
            'inventory_code': 'EQ-008',
            'usage_domain': 'AGRICULTURE',
            'support_phase': 'FIELD_TESTING',
            'is_operational': True
        },
        {
            'facility': facilities[8] if len(facilities) > 8 else facilities[0],
            'name': 'VR Development Headset',
            'capabilities': 'Immersive VR, motion tracking, development tools',
            'description': 'Virtual reality headset for educational content',
            'inventory_code': 'EQ-009',
            'usage_domain': 'SOFTWARE',
            'support_phase': 'USER_TESTING',
            'is_operational': True
        },
        {
            'facility': facilities[9] if len(facilities) > 9 else facilities[0],
            'name': 'Spectrum Analyzer',
            'capabilities': 'RF analysis, signal measurement, interference detection',
            'description': 'Radio frequency spectrum analyzer',
            'inventory_code': 'EQ-010',
            'usage_domain': 'ELECTRONICS',
            'support_phase': 'TESTING_VALIDATION',
            'is_operational': True
        }
    ]
    
    for eq_data in equipment_data:
        if eq_data['facility']:
            equipment, created = Equipment.objects.get_or_create(
                name=eq_data['name'],
                facility=eq_data['facility'],
                defaults=eq_data
            )
            if created:
                print(f"✓ Created equipment: {equipment.name}")
    
    # Create sample services
    services_data = [
        {
            'facility': facilities[0] if facilities else None,
            'name': '3D Printing Service',
            'description': 'Professional 3D printing for prototypes and custom parts',
            'category': 'FABRICATION',
            'skill_type': 'HARDWARE',
            'operating_hours': '8:00 AM - 6:00 PM'
        },
        {
            'facility': facilities[1] if len(facilities) > 1 else facilities[0],
            'name': 'CNC Machining Service',
            'description': 'Precision machining for metal and plastic components',
            'category': 'MACHINING',
            'skill_type': 'HARDWARE',
            'operating_hours': '7:00 AM - 5:00 PM'
        },
        {
            'facility': facilities[2] if len(facilities) > 2 else facilities[0],
            'name': 'Electronics Testing Lab',
            'description': 'Circuit testing and validation services',
            'category': 'TESTING',
            'skill_type': 'HARDWARE',
            'operating_hours': '8:00 AM - 6:00 PM'
        },
        {
            'facility': facilities[3] if len(facilities) > 3 else facilities[0],
            'name': 'Renewable Energy Consulting',
            'description': 'Solar and renewable energy system design consultation',
            'category': 'CONSULTANCY',
            'skill_type': 'MULTIDISCIPLINARY',
            'operating_hours': '8:00 AM - 5:00 PM'
        },
        {
            'facility': facilities[4] if len(facilities) > 4 else facilities[0],
            'name': 'AI/ML Training Workshop',
            'description': 'Machine learning and artificial intelligence training',
            'category': 'TRAINING',
            'skill_type': 'SOFTWARE',
            'operating_hours': '9:00 AM - 5:00 PM'
        },
        {
            'facility': facilities[5] if len(facilities) > 5 else facilities[0],
            'name': 'IoT Development Support',
            'description': 'Internet of Things development and consultation',
            'category': 'CONSULTANCY',
            'skill_type': 'SOFTWARE',
            'operating_hours': '8:00 AM - 6:00 PM'
        },
        {
            'facility': facilities[6] if len(facilities) > 6 else facilities[0],
            'name': 'Cybersecurity Assessment',
            'description': 'Security auditing and penetration testing services',
            'category': 'TESTING',
            'skill_type': 'SOFTWARE',
            'operating_hours': '24/7 - On demand'
        },
        {
            'facility': facilities[7] if len(facilities) > 7 else facilities[0],
            'name': 'Agricultural Tech Training',
            'description': 'Training on agricultural technology and smart farming',
            'category': 'TRAINING',
            'skill_type': 'MULTIDISCIPLINARY',
            'operating_hours': '8:00 AM - 5:00 PM'
        },
        {
            'facility': facilities[8] if len(facilities) > 8 else facilities[0],
            'name': 'VR/AR Development Service',
            'description': 'Virtual and augmented reality application development',
            'category': 'CONSULTANCY',
            'skill_type': 'SOFTWARE',
            'operating_hours': '9:00 AM - 6:00 PM'
        },
        {
            'facility': facilities[9] if len(facilities) > 9 else facilities[0],
            'name': 'Startup Incubation Program',
            'description': 'Comprehensive startup support and mentorship program',
            'category': 'TRAINING',
            'skill_type': 'MULTIDISCIPLINARY',
            'operating_hours': '8:00 AM - 8:00 PM'
        }
    ]
    
    for serv_data in services_data:
        if serv_data['facility']:
            service, created = Service.objects.get_or_create(
                name=serv_data['name'],
                facility=serv_data['facility'],
                defaults=serv_data
            )
            if created:
                print(f"✓ Created service: {service.name}")
    
    # Create sample participants
    all_projects = list(Project.objects.all())
    participants_data = [
        {
            'project': all_projects[0] if all_projects else None,
            'full_name': 'Dr. Sarah Nalugwa',
            'email': 'sarah.nalugwa@mak.ac.ug',
            'affiliation': 'Engineering',
            'specialization': 'Hardware',
            'cross_skill_trained': True,
            'institution': 'CEDAT',
            'role_on_project': 'Lecturer',
            'skill_role': 'Engineer'
        },
        {
            'project': all_projects[1] if len(all_projects) > 1 else all_projects[0] if all_projects else None,
            'full_name': 'James Okello',
            'email': 'james.okello@healthtech.ug',
            'affiliation': 'CS',
            'specialization': 'Software',
            'cross_skill_trained': False,
            'institution': 'SCIT',
            'role_on_project': 'Student',
            'skill_role': 'Developer'
        },
        {
            'project': all_projects[2] if len(all_projects) > 2 else all_projects[0] if all_projects else None,
            'full_name': 'Grace Namusoke',
            'email': 'grace.namusoke@blockchain.ug',
            'affiliation': 'CS',
            'specialization': 'Software',
            'cross_skill_trained': True,
            'institution': 'UniPod',
            'role_on_project': 'Contributor',
            'skill_role': 'Business Lead'
        },
        {
            'project': all_projects[3] if len(all_projects) > 3 else all_projects[0] if all_projects else None,
            'full_name': 'Moses Tugume',
            'email': 'moses.tugume@solar.ug',
            'affiliation': 'Engineering',
            'specialization': 'Hardware',
            'cross_skill_trained': True,
            'institution': 'Lwera',
            'role_on_project': 'Lecturer',
            'skill_role': 'Engineer'
        },
        {
            'project': all_projects[4] if len(all_projects) > 4 else all_projects[0] if all_projects else None,
            'full_name': 'Diana Atuhaire',
            'email': 'diana.atuhaire@edtech.ug',
            'affiliation': 'Other',
            'specialization': 'Software',
            'cross_skill_trained': False,
            'institution': 'SCIT',
            'role_on_project': 'Student',
            'skill_role': 'Designer'
        },
        {
            'project': all_projects[5] if len(all_projects) > 5 else all_projects[0] if all_projects else None,
            'full_name': 'Peter Ssemakula',
            'email': 'peter.ssemakula@waste.tech',
            'affiliation': 'SE',
            'specialization': 'Hardware',
            'cross_skill_trained': True,
            'institution': 'CEDAT',
            'role_on_project': 'Contributor',
            'skill_role': 'Engineer'
        },
        {
            'project': all_projects[6] if len(all_projects) > 6 else all_projects[0] if all_projects else None,
            'full_name': 'Mary Kiconco',
            'email': 'mary.kiconco@fintech.ug',
            'affiliation': 'CS',
            'specialization': 'Software',
            'cross_skill_trained': False,
            'institution': 'UniPod',
            'role_on_project': 'Student',
            'skill_role': 'Developer'
        },
        {
            'project': all_projects[7] if len(all_projects) > 7 else all_projects[0] if all_projects else None,
            'full_name': 'Robert Kiggundu',
            'email': 'robert.kiggundu@agridrone.ug',
            'affiliation': 'Engineering',
            'specialization': 'Hardware',
            'cross_skill_trained': True,
            'institution': 'Lwera',
            'role_on_project': 'Lecturer',
            'skill_role': 'Engineer'
        },
        {
            'project': all_projects[8] if len(all_projects) > 8 else all_projects[0] if all_projects else None,
            'full_name': 'Alice Namugga',
            'email': 'alice.namugga@cybersec.ug',
            'affiliation': 'CS',
            'specialization': 'Software',
            'cross_skill_trained': True,
            'institution': 'UIRI',
            'role_on_project': 'Contributor',
            'skill_role': 'Business Lead'
        },
        {
            'project': all_projects[9] if len(all_projects) > 9 else all_projects[0] if all_projects else None,
            'full_name': 'Emmanuel Byaruhanga',
            'email': 'emmanuel.byaruhanga@traffic.ai',
            'affiliation': 'CS',
            'specialization': 'Software',
            'cross_skill_trained': False,
            'institution': 'SCIT',
            'role_on_project': 'Student',
            'skill_role': 'Developer'
        }
    ]
    
    for part_data in participants_data:
        if part_data['project']:
            participant, created = Participant.objects.get_or_create(
                email=part_data['email'],
                defaults=part_data
            )
            if created:
                print(f"✓ Created participant: {participant.full_name}")
    
    # Create sample outcomes
    outcomes_data = [
        {
            'ProjectId': all_projects[0] if all_projects else None,
            'Title': 'IoT Agriculture Sensor Prototype',
            'Description': 'Working prototype of soil moisture and pH monitoring system',
            'ArtifactLink': 'https://github.com/agritech/iot-sensor-v1',
            'OutcomeType': 'PROTOTYPE',
            'QualityCertification': 'ISO 9001 Testing Completed',
            'CommercializationStatus': 'PILOT_TESTING'
        },
        {
            'ProjectId': all_projects[1] if len(all_projects) > 1 else all_projects[0] if all_projects else None,
            'Title': 'Telemedicine Mobile Application',
            'Description': 'Complete mobile app for remote healthcare consultations',
            'ArtifactLink': 'https://play.google.com/store/apps/details?id=ug.telehealth',
            'OutcomeType': 'SOFTWARE',
            'QualityCertification': 'Healthcare Data Security Certified',
            'CommercializationStatus': 'MARKET_READY'
        },
        {
            'ProjectId': all_projects[2] if len(all_projects) > 2 else all_projects[0] if all_projects else None,
            'Title': 'Blockchain Supply Chain Platform',
            'Description': 'Decentralized platform for agricultural product tracking',
            'ArtifactLink': 'https://supplychainblockchain.ug/platform',
            'OutcomeType': 'SOFTWARE',
            'QualityCertification': 'Blockchain Security Audit Passed',
            'CommercializationStatus': 'COMMERCIALIZED'
        },
        {
            'ProjectId': all_projects[3] if len(all_projects) > 3 else all_projects[0] if all_projects else None,
            'Title': 'Solar Water Pump Technical Specifications',
            'Description': 'Complete engineering drawings and specifications',
            'ArtifactLink': 'https://solarwater.ug/technical-docs',
            'OutcomeType': 'CAD_DESIGN',
            'QualityCertification': 'Engineering Design Review Completed',
            'CommercializationStatus': 'PRE_COMMERCIAL'
        },
        {
            'ProjectId': all_projects[4] if len(all_projects) > 4 else all_projects[0] if all_projects else None,
            'Title': 'E-Learning Content Package',
            'Description': 'Interactive educational content for primary mathematics',
            'ArtifactLink': 'https://edutech.ug/content-package',
            'OutcomeType': 'SOFTWARE',
            'QualityCertification': 'Educational Standards Compliance',
            'CommercializationStatus': 'PILOT_TESTING'
        },
        {
            'ProjectId': all_projects[5] if len(all_projects) > 5 else all_projects[0] if all_projects else None,
            'Title': 'Smart Waste Bin Prototype',
            'Description': 'IoT-enabled waste monitoring device prototype',
            'ArtifactLink': 'https://wastetech.ug/smart-bin-v1',
            'OutcomeType': 'PROTOTYPE',
            'QualityCertification': 'Environmental Impact Assessment',
            'CommercializationStatus': 'MARKET_READY'
        },
        {
            'ProjectId': all_projects[6] if len(all_projects) > 6 else all_projects[0] if all_projects else None,
            'Title': 'Mobile Banking Business Plan',
            'Description': 'Comprehensive business strategy for mobile financial services',
            'ArtifactLink': 'https://fintech.ug/business-plan',
            'OutcomeType': 'BUSINESS_PLAN',
            'QualityCertification': 'Financial Regulatory Review',
            'CommercializationStatus': 'PRE_COMMERCIAL'
        },
        {
            'ProjectId': all_projects[7] if len(all_projects) > 7 else all_projects[0] if all_projects else None,
            'Title': 'Agricultural Drone PCB Design',
            'Description': 'Custom PCB design for drone flight controller and sensors',
            'ArtifactLink': 'https://agridrone.ug/pcb-designs',
            'OutcomeType': 'PCB_DESIGN',
            'QualityCertification': 'EMC Compliance Testing',
            'CommercializationStatus': 'COMMERCIALIZED'
        },
        {
            'ProjectId': all_projects[8] if len(all_projects) > 8 else all_projects[0] if all_projects else None,
            'Title': 'Cybersecurity Training Manual',
            'Description': 'Comprehensive cybersecurity training curriculum and materials',
            'ArtifactLink': 'https://cybersec.ug/training-manual',
            'OutcomeType': 'DOCUMENTATION',
            'QualityCertification': 'Industry Standards Compliance',
            'CommercializationStatus': 'MARKET_READY'
        },
        {
            'ProjectId': all_projects[9] if len(all_projects) > 9 else all_projects[0] if all_projects else None,
            'Title': 'Traffic AI Algorithm Documentation',
            'Description': 'Machine learning algorithms for traffic flow optimization',
            'ArtifactLink': 'https://trafficai.ug/algorithm-docs',
            'OutcomeType': 'DOCUMENTATION',
            'QualityCertification': 'Algorithm Validation Completed',
            'CommercializationStatus': 'PILOT_TESTING'
        }
    ]
    
    for out_data in outcomes_data:
        if out_data['ProjectId']:
            outcome, created = Outcome.objects.get_or_create(
                Title=out_data['Title'],
                ProjectId=out_data['ProjectId'],
                defaults=out_data
            )
            if created:
                print(f"✓ Created outcome: {outcome.Title}")
    
    print("Sample data creation completed!")
    
    # Print counts
    print(f"\nCurrent entity counts:")
    print(f"Programs: {Program.objects.count()}")
    print(f"Facilities: {Facility.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Equipment: {Equipment.objects.count()}")
    print(f"Services: {Service.objects.count()}")
    print(f"Participants: {Participant.objects.count()}")
    print(f"Outcomes: {Outcome.objects.count()}")


if __name__ == "__main__":
    create_sample_data()
