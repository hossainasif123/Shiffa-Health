from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
import os

from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings
import os

class Patient(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    birthdate = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='other')
    
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)

    # Profile Photo
    profile_photo = models.ImageField(upload_to='uploads/patient_photos/', null=True, blank=True)
    
    # Medical History
    past_medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    current_medications = models.TextField(blank=True, null=True)
    family_medical_history = models.TextField(blank=True, null=True)
    immunization_records = models.TextField(blank=True, null=True)

    # Lifestyle Information
    occupation = models.CharField(max_length=100, blank=True, null=True)
    
    SMOKING_STATUS_CHOICES = [
        ('smoker', 'Smoker'),
        ('non_smoker', 'Non-Smoker'),
        ('former_smoker', 'Former Smoker'),
    ]
    smoking_status = models.CharField(max_length=15, choices=SMOKING_STATUS_CHOICES, default='non_smoker')
    
    alcohol_consumption = models.TextField(blank=True, null=True)
    physical_activity_level = models.CharField(max_length=50, blank=True, null=True)
    dietary_preferences = models.TextField(blank=True, null=True)

    # Current Health Status
    recent_health_issues = models.TextField(blank=True, null=True)
    vital_signs = models.JSONField(blank=True, null=True)
    lab_results = models.TextField(blank=True, null=True)

    # Consultation History
    previous_appointments = models.TextField(blank=True, null=True)
    upcoming_appointments = models.TextField(blank=True, null=True)
    medical_notes = models.TextField(blank=True, null=True)

    # Treatment Plans
    ongoing_treatments = models.TextField(blank=True, null=True)
    specialist_referrals = models.TextField(blank=True, null=True)
    follow_up_care_instructions = models.TextField(blank=True, null=True)

    # Insurance Information
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    policy_number = models.CharField(max_length=50, blank=True, null=True)
    coverage_details = models.TextField(blank=True, null=True)

    # Patient Preferences
    preferred_communication_method = models.CharField(max_length=50, blank=True, null=True)
    preferred_pharmacy = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.owner.username}"





class VaccinationRecord(models.Model):
    patient = models.ForeignKey(
        Patient, 
        on_delete=models.CASCADE, 
        related_name='vaccination_records'  
    )
    vaccine_name = models.CharField(max_length=100)
    date_given = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.vaccine_name} for {self.patient.full_name}'

# models.py


# models.py



class MediaUpload(models.Model):
    UPLOAD_TYPE_CHOICES = [
        ('personal', 'Personal'),
        ('prescription', 'Prescription'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_type = models.CharField(max_length=15, choices=UPLOAD_TYPE_CHOICES)
    image = models.ImageField(upload_to='uploads/images/', null=True, blank=True)
    video = models.FileField(upload_to='uploads/videos/', null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.video:
            if os.path.isfile(self.video.path):
                os.remove(self.video.path)
        super().delete(*args, **kwargs)  

    def __str__(self):
        return f'{self.upload_type} upload by {self.user}'
