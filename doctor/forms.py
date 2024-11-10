from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import DoctorProfile, TimeSlot, Booking, Review

User = get_user_model()

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'license_number', 'years_of_experience', 'qualifications', 'profile_picture']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # Fields are managed in the view; this form will be used without default fields

    def __init__(self, *args, **kwargs):
        self.time_slot = kwargs.pop('time_slot', None)  # Ensure time_slot is passed
        self.user = kwargs.pop('user', None)  # Ensure user is passed if needed
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.time_slot:
            raise forms.ValidationError("Time slot must be provided.")
        if not self.user:
            raise forms.ValidationError("User must be provided.")
        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.time_slot = self.time_slot
        booking.user = self.user  # Set user explicitly
        booking.booking_time = timezone.now()
        booking.payment_status = 'Pending'  # Default payment status
        booking.amount = 50.00  # Example amount, adjust as needed

        if commit:
            booking.save()
        return booking

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.doctor_profile = kwargs.pop('doctor_profile', None)  # Ensure doctor_profile is passed
        self.user = kwargs.pop('user', None)  # Ensure user is passed
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.doctor_profile:
            raise forms.ValidationError("Doctor profile must be provided.")
        if not self.user:
            raise forms.ValidationError("User must be provided.")
        return cleaned_data

    def save(self, commit=True):
        review = super().save(commit=False)
        review.doctor_profile = self.doctor_profile
        review.user = self.user  # Set user explicitly
        review.review_date = timezone.now()

        if commit:
            review.save()
        return review
