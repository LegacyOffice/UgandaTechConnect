import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_project'),  # adjust if your last migration is different
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                (
                    'service_id',
                    models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False,
                        serialize=False
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=200,
                        help_text='Service name (e.g., CNC machining, PCB fabrication)'
                    ),
                ),
                (
                    'description',
                    models.TextField(
                        blank=True,
                        help_text='Details of what the service does'
                    ),
                ),
                (
                    'category',
                    models.CharField(
                        max_length=50,
                        choices=[
                            ('MACHINING', 'Machining'),
                            ('TESTING', 'Testing'),
                            ('TRAINING', 'Training'),
                            ('FABRICATION', 'Fabrication'),
                            ('CONSULTANCY', 'Consultancy'),
                        ],
                        help_text='Category of the service'
                    ),
                ),
                (
                    'skill_type',
                    models.CharField(
                        max_length=50,
                        choices=[
                            ('HARDWARE', 'Hardware'),
                            ('SOFTWARE', 'Software'),
                            ('INTEGRATION', 'Integration'),
                            ('MULTIDISCIPLINARY', 'Multidisciplinary'),
                        ],
                        help_text='Skill type supported by this service'
                    ),
                ),
                ('operating_hours', models.CharField(max_length=50, blank=True, null=True, help_text='E.g., 9:00 AM - 5:00 PM')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'facility',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='services',
                        to='core.facility',
                        help_text='Facility that offers this service'
                    ),
                ),
            ],
            options={
                'ordering': ['facility__name', 'name'],
            },
        ),
    ]
