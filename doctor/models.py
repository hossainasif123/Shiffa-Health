from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model() 
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    years_of_experience = models.IntegerField()
    qualifications = models.TextField()  # For storing qualifications
    profile_picture = models.ImageField(upload_to='doctor_pictures/', null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"

class TimeSlot(models.Model):
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='time_slots')
    day_of_week = models.CharField(max_length=9)  # Example: 'Monday', 'Tuesday', etc.
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor_profile', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.day_of_week} {self.start_time} - {self.end_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who made the booking
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField(auto_now_add=True)  # When the booking was made
    payment_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded')
    ])  # Track payment status
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Store payment transaction ID
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Amount to be paid

    """class Meta:
        unique_together = ('user', 'time_slot')"""

    def __str__(self):
        return f"Booking by {self.user} for {self.time_slot} on {self.booking_time}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who gives the review
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()  # Rating out of 5
    comment = models.TextField()  # Review comments
    review_date = models.DateTimeField(auto_now_add=True)

    """class Meta:
        unique_together = ('user', 'doctor_profile')"""

    def __str__(self):
        return f"Review by {self.user} for {self.doctor_profile}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"