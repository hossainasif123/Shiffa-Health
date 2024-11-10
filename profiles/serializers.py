from rest_framework import serializers
from .models import Patient, VaccinationRecord


class VaccinationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationRecord
        fields = ['id', 'vaccine_name', 'date_given', 'next_due_date']


class PatientSerializer(serializers.ModelSerializer):
    vaccination_records = VaccinationRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 
            'owner', 
            'full_name', 
            'birthdate', 
            'gender', 
            'contact_number', 
            'email', 
            'address', 
            'emergency_contact_name', 
            'emergency_contact_relationship', 
            'emergency_contact_number', 
            'profile_photo', 
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
            'created_at', 
            'updated_at', 
            'vaccination_records'  # Nested vaccination records
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
