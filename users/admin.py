from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path, reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect

from .models import User
from .forms import UserCreationFormAdmin
from .tokens import email_verification_token

class UserAdmin(admin.ModelAdmin):
    form = UserCreationFormAdmin
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-verification-email/<int:user_id>/', 
                 self.admin_site.admin_view(self.send_verification_email_view), 
                 name='send_verification_email'),
        ]
        return custom_urls + urls

    def send_verification_email_view(self, request, user_id, *args, **kwargs):
        user = self.get_object(request, user_id)
        if user is not None:
            token = email_verification_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{request.scheme}://{request.get_host()}{reverse('email-verify', kwargs={'uidb64': uid, 'token': token})}"
            
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            self.message_user(request, f'Verification email sent to {user.email}.')
        else:
            self.message_user(request, 'User not found.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_superuser:
            return self.readonly_fields + ('role',)
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.role == User.ADMIN):
            return True
        return super().has_change_permission(request, obj)
#Shanto0987
#asifalhossain2000@gmail.com
#Rawfa8923
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.role == User.ADMIN):
            return True
        return super().has_delete_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser or (obj and obj.role == User.ADMIN):
            return True
        return super().has_view_permission(request, obj)

admin.site.register(User, UserAdmin)
