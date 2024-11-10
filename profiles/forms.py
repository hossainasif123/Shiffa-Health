from django import forms
from django.forms import inlineformset_factory
from .models import Patient, VaccinationRecord
from datetime import date  

from .models import MediaUpload
from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'full_name',
            'birthdate',
            'gender',
            'contact_number',
            'email',
            'address',
            'emergency_contact_name',
            'emergency_contact_relationship',
            'emergency_contact_number',
            'past_medical_conditions',
            'allergies',
            'current_medications',
            'family_medical_history',
            'immunization_records',
            'occupation',
            'smoking_status',
            'alcohol_consumption',
            'physical_activity_level',
            'dietary_preferences',
            'recent_health_issues',
            'vital_signs',
            'lab_results',
            'previous_appointments',
            'upcoming_appointments',
            'medical_notes',
            'ongoing_treatments',
            'specialist_referrals',
            'follow_up_care_instructions',
            'insurance_provider',
            'policy_number',
            'coverage_details',
            'preferred_communication_method',
            'preferred_pharmacy',
            'profile_photo',
        ]

        # Customizing widgets
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact name'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Relationship'}),
            'emergency_contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Emergency contact number'}),
            'past_medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List past medical conditions'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List allergies'}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List current medications'}),
            'family_medical_history': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Family medical history'}),
            'immunization_records': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Immunization records'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'smoking_status': forms.Select(attrs={'class': 'form-control'}),
            'alcohol_consumption': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe alcohol consumption'}),
            'physical_activity_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Physical activity level'}),
            'dietary_preferences': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Dietary preferences'}),
            'recent_health_issues': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Recent health issues'}),
            'vital_signs': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Vital signs'}),
            'lab_results': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Lab results'}),
            'previous_appointments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Previous appointments'}),
            'upcoming_appointments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Upcoming appointments'}),
            'medical_notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Medical notes'}),
            'ongoing_treatments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ongoing treatments'}),
            'specialist_referrals': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Specialist referrals'}),
            'follow_up_care_instructions': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Follow-up care instructions'}),
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance provider'}),
            'policy_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Policy number'}),
            'coverage_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Coverage details'}),
            'preferred_communication_method': forms.Select(attrs={'class': 'form-control'}),
            'preferred_pharmacy': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred pharmacy'}),
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    # Custom validation (if needed)
    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number and not contact_number.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        return contact_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not forms.EmailField().clean(email):
            raise forms.ValidationError("Invalid email address.")
        return email

    def clean_vital_signs(self):
        vital_signs = self.cleaned_data.get('vital_signs')
        # Implement custom validation for vital signs if needed
        return vital_signs


class VaccinationRecordForm(forms.ModelForm):
    class Meta:
        model = VaccinationRecord
        fields = ['vaccine_name', 'date_given', 'next_due_date']
        widgets = {
            'date_given': forms.DateInput(attrs={'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Custom validation for date fields
    def clean(self):
        cleaned_data = super().clean()
        date_given = cleaned_data.get('date_given')
        next_due_date = cleaned_data.get('next_due_date')

        if next_due_date and date_given and next_due_date <= date_given:
            self.add_error('next_due_date', "Next due date must be after the date the vaccine was given.")

        return cleaned_data

# Create a formset for VaccinationRecord
VaccinationRecordFormSet = inlineformset_factory(
    Patient,
    VaccinationRecord,
    form=VaccinationRecordForm,
    extra=1,
    can_delete=True
)
# forms.py


class MediaUploadForm(forms.ModelForm):
    class Meta:
        model = MediaUpload
        fields = ['image', 'video']
