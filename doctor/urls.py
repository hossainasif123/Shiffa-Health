from django.urls import path
from .views import DoctorProfileView, BookAppointmentView, BookingConfirmationView, LeaveReviewView,DoctorListView
from .views import BookingNotificationView,NotificationsView
from .views import VideoChatView,EndMeetingView,DailyRoomView
app_name = 'doctor'
urlpatterns = [
    # URL for viewing a doctor's profile
    path('doctors/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/<int:pk>/', DoctorProfileView.as_view(), name='doctor_profile'),
    # URL for booking an appointment
    path('doctor/book/<int:time_slot_id>/', BookAppointmentView.as_view(), name='book_appointment'),
    
    # URL for booking confirmation
    path('booking/confirmation/<int:pk>/', BookingConfirmationView.as_view(), name='booking_confirmation'),
    
    # URL for leaving a review for a doctor
   path('doctor/<int:doctor_id>/review/', LeaveReviewView.as_view(), name='leave_review'),

   path('send-notification/<int:doctor_id>/', BookingNotificationView.as_view(), name='send_booking_notification'),
    
   path('notifications/', NotificationsView.as_view(), name='notifications'), 
    path("video-chat/", VideoChatView.as_view(), name="video_chat"),
   path("end-meeting/<str:room_name>/", EndMeetingView.as_view(), name="end_meeting"),
   path("room/<str:room_name>/", DailyRoomView.as_view(), name="daily_room"),

]

