from django.contrib import admin
from .models import Patient, VaccinationRecord ,MediaUpload

# Inline model for VaccinationRecord
class VaccinationRecordInline(admin.TabularInline):
    model = VaccinationRecord
    extra = 1  
    fields = ('vaccine_name', 'date_given', 'next_due_date')  
    readonly_fields = ('vaccine_name',)  
    can_delete = True 

# Admin class for Patient

class MediaUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'upload_type', 'upload_date', 'image', 'video')  
    search_fields = ('user__username', 'upload_type')  
    list_filter = ('upload_type', 'upload_date')  


from django.contrib import admin
from .models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'owner', 
        'gender', 
        'contact_number', 
        'birthdate', 
        'profile_photo_display'
    )
    search_fields = ('full_name', 'owner__username', 'contact_number', 'email')
    list_filter = ('gender', 'birthdate', 'smoking_status')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'owner', 
                'full_name', 
                'birthdate', 
                'gender', 
                'contact_number', 
                'email', 
                'address', 
                'profile_photo'
            )
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 
                'emergency_contact_relationship', 
                'emergency_contact_number'
            )
        }),
        ('Medical History', {
            'fields': (
                'past_medical_conditions', 
                'allergies', 
                'current_medications', 
                'family_medical_history', 
                'immunization_records'
            )
        }),
        ('Lifestyle Information', {
            'fields': (
                'occupation', 
                'smoking_status', 
                'alcohol_consumption', 
                'physical_activity_level', 
                'dietary_preferences'
            )
        }),
        ('Current Health Status', {
            'fields': (
                'recent_health_issues', 
                'vital_signs', 
                'lab_results'
            )
        }),
        ('Consultation History', {
            'fields': (
                'previous_appointments', 
                'upcoming_appointments', 
                'medical_notes'
            )
        }),
        ('Treatment Plans', {
            'fields': (
                'ongoing_treatments', 
                'specialist_referrals', 
                'follow_up_care_instructions'
            )
        }),
        ('Insurance Information', {
            'fields': (
                'insurance_provider', 
                'policy_number', 
                'coverage_details'
            )
        }),
        ('Patient Preferences', {
            'fields': (
                'preferred_communication_method', 
                'preferred_pharmacy'
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 
                'updated_at'
            )
        }),
    )

    def profile_photo_display(self, obj):
        if obj.profile_photo:
            return f"<img src='{obj.profile_photo.url}' width='50' height='50' style='border-radius: 50%;' />"
        return "No Photo"
    profile_photo_display.short_description = 'Profile Photo'
    profile_photo_display.allow_tags = True




admin.site.register(MediaUpload, MediaUploadAdmin)
admin.site.register(Patient, PatientAdmin)