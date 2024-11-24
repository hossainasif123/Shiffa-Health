from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DoctorProfile, TimeSlot, Booking, Review
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

class DoctorProfileView(DetailView):
    model = DoctorProfile
    template_name = 'doctor/doctor_profile.html'
    context_object_name = 'doctorprofile'

    def get_object(self, queryset=None):
        # Override get_object to handle potential issues
        pk = self.kwargs.get('pk')
        if not pk:
            # If no pk is provided in the URL, return a 404 response
            return HttpResponse("No primary key provided in URL.", status=404)
        try:
            return DoctorProfile.objects.get(pk=pk)
        except DoctorProfile.DoesNotExist:
            # If the object is not found, return a 404 response
            return HttpResponse("DoctorProfile not found.", status=404)
   



from .utils import send_websocket_notification  # Import the utility function

class BookAppointmentView(LoginRequiredMixin, CreateView):
    model = Booking
    fields = []
    template_name = 'doctor/book_appointment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_slot'] = get_object_or_404(TimeSlot, id=self.kwargs['time_slot_id'])
        return context

    def form_valid(self, form):
        time_slot = get_object_or_404(TimeSlot, id=self.kwargs['time_slot_id'])
        booking = Booking(
            user=self.request.user,
            time_slot=time_slot,
            booking_time=timezone.now(),
            payment_status='Pending',
            amount=50.00  
        )
        booking.save()

        # Get the doctor related to the time slot
        doctor = time_slot.doctor_profile.user

        # Create the notification message
        message = f"New booking from {self.request.user.username} for {time_slot.start_time} - {time_slot.end_time}."

        # Use the utility function to send the WebSocket notification and save it to the database
        send_websocket_notification(doctor, message, event_type='booking_notification')

        return redirect('doctor:booking_confirmation', pk=booking.id)


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = 'doctor/booking_confirmation.html'
    context_object_name = 'booking'

from django.urls import reverse
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Review, DoctorProfile

class LeaveReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'doctor/leave_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the doctor profile based on the doctor_id passed in the URL
        context['doctorprofile'] = get_object_or_404(DoctorProfile, id=self.kwargs['doctor_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.doctor_profile = get_object_or_404(DoctorProfile, id=self.kwargs['doctor_id'])
        form.instance.review_date = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the doctor's profile after successful review submission
        return reverse('doctor:doctor_profile', kwargs={'pk': self.kwargs['doctor_id']})



class DoctorListView(ListView):
    model = DoctorProfile
    template_name = 'doctor/doctor_list.html'
    context_object_name = 'doctors'




from django.views.generic import TemplateView
from .models import Notification

from django.views.generic import TemplateView
from .models import Notification

class NotificationsView(TemplateView):
    template_name = 'doctor/notifications.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch unread notifications for the user
        unread_notifications = Notification.objects.filter(user=self.request.user, is_read=False)
        
        # Mark them as read
        unread_notifications.update(is_read=True)
        
        # Fetch all notifications for the user, including read and unread
        context['notifications'] = Notification.objects.filter(user=self.request.user).order_by('-created_at')
        context['unread_count'] = Notification.objects.filter(user=self.request.user, is_read=False).count()
        return context

from .models import DoctorProfile
from django.views import View
class BookingNotificationView(LoginRequiredMixin, View):
    def post(self, request, doctor_id, *args, **kwargs):
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        user = request.user
        
        # Customize your message content
        message = f'New booking from {user.username}'

        # Get the channel layer
        channel_layer = get_channel_layer()

        # Send the message to the doctor's notification group
        async_to_sync(channel_layer.group_send)(
            f'notifications_{doctor.user.username}',  # Room group name based on the doctor's username
            {
                'type': 'booking_notification',
                'message': message
            }
        )

        return JsonResponse({'status': 'Notification sent'}, status=200)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
from django.shortcuts import render
from .daily_utils import create_daily_room

# views.py
from django.views.generic import TemplateView
from doctor.daily_utils import create_daily_room

class VideoChatView(TemplateView):
    template_name = "doctor/video_chat.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_info = create_daily_room()  # No argument needed
        
        if room_info:
            context["join_url"] = room_info.get("url")
        else:
            context["error"] = "Unable to create room."
        
        return context


# views.py
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .daily_utils import end_daily_room

class EndMeetingView(LoginRequiredMixin, View):
    def post(self, request, room_name):
        # Ensure that only the host can end the meeting (assuming `is_host` is a property on the user model)
        if request.user.is_host:
            success = end_daily_room(room_name)
            if success:
                return JsonResponse({"message": "Meeting ended successfully"}, status=200)
            else:
                return JsonResponse({"error": "Failed to end the meeting"}, status=500)
        else:
            return JsonResponse({"error": "Unauthorized access"}, status=403)


# views.py
from django.shortcuts import render
from django.views import View
from django.conf import settings
from doctor.daily_utils import create_daily_room, create_host_token

class DailyRoomView(LoginRequiredMixin,View):
    def get(self, request, room_name):
        # Generate or fetch the host token for this room
        host_token = create_host_token(room_name)

        # If token creation failed, handle it
        if not host_token:
            return render(request, "error.html", {"message": "Failed to create host token"})

        # Render the room template with room details
        return render(request, "daily_room.html", {
            "room_name": room_name,
            "host_token": host_token,
        })


