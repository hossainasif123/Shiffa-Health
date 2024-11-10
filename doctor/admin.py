from django.contrib import admin
from .models import DoctorProfile, TimeSlot, Booking, Review, Notification

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'years_of_experience', 'profile_picture')
    search_fields = ('user__username', 'specialization', 'license_number')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('doctor_profile', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('doctor_profile', 'day_of_week')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_slot', 'booking_time', 'payment_status', 'transaction_id', 'amount')
    list_filter = ('payment_status', 'user', 'time_slot')
    search_fields = ('user__username', 'transaction_id')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor_profile', 'rating', 'review_date')
    list_filter = ('rating', 'doctor_profile')
    search_fields = ('user__username', 'doctor_profile__user__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'user')
    search_fields = ('user__username', 'message')
