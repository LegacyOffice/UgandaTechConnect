from django.test import TestCase, Client
from django.urls import reverse
from core.models import Program, Facility, Project, Outcome, Participant
from core.forms import ProjectForm, OutcomeForm
import uuid


class ProjectModelTests(TestCase):
    """Test cases for the Project model"""
    
    def setUp(self):
        """Set up test data"""
        self.program = Program.objects.create(
            name='Innovation Program',
            description='Test program for innovation'
        )
        
        self.facility = Facility.objects.create(
            name='Tech Hub',
            location='Kampala',
            description='Technology hub',
            contact_email='test@techhub.com',
            contact_phone='+256700000000'
        )
    
    def test_project_creation(self):
        """Test creating a project"""
        project = Project.objects.create(
            Title='Smart IoT System',
            Description='An innovative IoT solution',
            ProgramId=self.program,
            FacilityId=self.facility,
            NatureOfProject='prototype',
            InnovationFocus='iot',
            PrototypeStage='mvp'
        )
        
        self.assertEqual(project.Title, 'Smart IoT System')
        self.assertEqual(project.ProgramId, self.program)
        self.assertEqual(project.FacilityId, self.facility)
        self.assertEqual(project.NatureOfProject, 'prototype')
        self.assertIsNotNone(project.ProjectId)
        print(f"✓ Project created successfully: {project.Title}")
    
    def test_project_without_optional_fields(self):
        """Test creating a project without optional program and facility"""
        project = Project.objects.create(
            Title='Basic Project',
            Description='A basic project',
            NatureOfProject='research'
        )
        
        self.assertEqual(project.Title, 'Basic Project')
        self.assertIsNone(project.ProgramId)
        self.assertIsNone(project.FacilityId)
        print(f"✓ Project created without optional fields: {project.Title}")
    
    def test_project_str_method(self):
        """Test the string representation of a project"""
        project = Project.objects.create(
            Title='Test Project',
            Description='Description',
            NatureOfProject='research'
        )
        self.assertEqual(str(project), 'Test Project')
        print(f"✓ Project string representation works: {str(project)}")


class ProjectFormTests(TestCase):
    """Test cases for the Project form"""
    
    def setUp(self):
        """Set up test data"""
        self.program = Program.objects.create(
            name='Innovation Program',
            description='Test program'
        )
        
        self.facility = Facility.objects.create(
            name='Tech Hub',
            location='Kampala'
        )
    
    def test_valid_project_form(self):
        """Test project form with valid data"""
        form_data = {
            'Title': 'Smart IoT System',
            'Description': 'An innovative IoT solution',
            'ProgramId': self.program.program_id,
            'FacilityId': self.facility.facility_id,
            'NatureOfProject': 'prototype',
            'InnovationFocus': 'iot',
            'PrototypeStage': 'mvp'
        }
        
        form = ProjectForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        print("✓ Project form validation passed")
    
    def test_project_form_missing_required_fields(self):
        """Test project form with missing required fields"""
        form_data = {
            'Description': 'Missing title'
        }
        
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Title', form.errors)
        print("✓ Project form correctly validates required fields")


class ProjectViewTests(TestCase):
    """Test cases for Project views"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        
        self.project = Project.objects.create(
            Title='Test Project',
            Description='Test Description',
            NatureOfProject='prototype'
        )
    
    def test_project_list_view(self):
        """Test the project list view"""
        response = self.client.get(reverse('core:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        print("✓ Project list view works correctly")
    
    def test_project_detail_view(self):
        """Test the project detail view"""
        response = self.client.get(
            reverse('core:project_detail', args=[self.project.ProjectId])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        print("✓ Project detail view works correctly")
    
    def test_project_create_view_get(self):
        """Test accessing the project create form"""
        response = self.client.get(reverse('core:project_create'))
        self.assertEqual(response.status_code, 200)
        print("✓ Project create view accessible")


class OutcomeModelTests(TestCase):
    """Test cases for the Outcome model"""
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            Title='Test Project',
            Description='Test Description',
            NatureOfProject='prototype'
        )
    
    def test_outcome_creation(self):
        """Test creating an outcome"""
        outcome = Outcome.objects.create(
            ProjectId=self.project,
            Title='IoT Prototype',
            Description='Successfully built IoT prototype',
            OutcomeType='Prototype',
            CommercializationStatus='Demoed'
        )
        
        self.assertEqual(outcome.ProjectId, self.project)
        self.assertEqual(outcome.OutcomeType, 'Prototype')
        self.assertEqual(outcome.CommercializationStatus, 'Demoed')
        self.assertIsNotNone(outcome.Outcomeld)
        print(f"✓ Outcome created successfully: {outcome.Title}")
    
    def test_outcome_with_optional_fields(self):
        """Test creating outcome with all fields"""
        outcome = Outcome.objects.create(
            ProjectId=self.project,
            Title='Research Paper',
            Description='Research paper published',
            OutcomeType='Report',
            CommercializationStatus='Demoed',
            ArtifactLink='https://example.com/paper.pdf',
            QualityCertification='ISO 9001'
        )
        
        self.assertIsNotNone(outcome.ArtifactLink)
        self.assertEqual(outcome.QualityCertification, 'ISO 9001')
        print(f"✓ Outcome created with optional fields")
    
    def test_outcome_str_method(self):
        """Test the string representation of an outcome"""
        outcome = Outcome.objects.create(
            ProjectId=self.project,
            Title='Patent Application',
            Description='Patent filed',
            OutcomeType='Report',
            CommercializationStatus='Market Linked'
        )
        expected_str = 'Patent Application'
        self.assertEqual(str(outcome), expected_str)
        print(f"✓ Outcome string representation works: {str(outcome)}")


class OutcomeFormTests(TestCase):
    """Test cases for the Outcome form"""
    
    def setUp(self):
        """Set up test data"""
        self.project = Project.objects.create(
            Title='Test Project',
            Description='Test Description',
            NatureOfProject='prototype'
        )
    
    def test_valid_outcome_form(self):
        """Test outcome form with valid data"""
        form_data = {
            'ProjectId': self.project.ProjectId,
            'Title': 'IoT Prototype',
            'Description': 'Successfully built IoT prototype',
            'OutcomeType': 'Prototype',
            'CommercializationStatus': 'Demoed'
        }
        
        form = OutcomeForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
        print("✓ Outcome form validation passed")
    
    def test_outcome_form_missing_required_fields(self):
        """Test outcome form with missing required fields"""
        form_data = {
            'Description': 'Missing title and project'
        }
        
        form = OutcomeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Title', form.errors)
        print("✓ Outcome form correctly validates required fields")


class OutcomeViewTests(TestCase):
    """Test cases for Outcome views"""
    
    def setUp(self):
        """Set up test client and data"""
        self.client = Client()
        
        self.project = Project.objects.create(
            Title='Test Project',
            Description='Test Description',
            NatureOfProject='prototype'
        )
        
        self.outcome = Outcome.objects.create(
            ProjectId=self.project,
            Title='Test Outcome',
            Description='Test outcome description',
            OutcomeType='Prototype',
            CommercializationStatus='Demoed'
        )
    
    def test_outcome_list_view(self):
        """Test the outcome list view"""
        response = self.client.get(reverse('core:outcome_list'))
        self.assertEqual(response.status_code, 200)
        print("✓ Outcome list view works correctly")
    
    def test_outcome_detail_view(self):
        """Test the outcome detail view"""
        response = self.client.get(
            reverse('core:outcome_detail', args=[self.outcome.Outcomeld])
        )
        self.assertEqual(response.status_code, 200)
        print("✓ Outcome detail view works correctly")
    
    def test_outcome_create_view_get(self):
        """Test accessing the outcome create form"""
        response = self.client.get(reverse('core:outcome_create'))
        self.assertEqual(response.status_code, 200)
        print("✓ Outcome create view accessible")
