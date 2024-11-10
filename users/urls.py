from django.urls import path
from .views import PatientSignUpView, EmailVerificationView, LoginView, EmailVerificationSentView, HomeView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from profiles.views import PatientDetailView,PatientListView


app_name = 'users'  # This registers the namespace

urlpatterns = [
    path('', HomeView.as_view(), name='dashboard'),  
    path('signup/', PatientSignUpView.as_view(), name='signup'),  
    path('email-verification-sent/', EmailVerificationSentView.as_view(), name='email_verification_sent'),  # Confirmation after email verification sent
    path('verify/<uidb64>/<token>/', EmailVerificationView.as_view(), name='email-verify'),  # Email verification
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('login/', LoginView.as_view(), name='login'), 
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'), 
    path('password-reset/done/', TemplateView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),  # Password reset done confirmation
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Password reset confirmation link
    path('profiles/<int:pk>/', login_required(PatientDetailView.as_view()), name='show-profile'),
    path('list/', login_required(PatientListView.as_view()), name='patient-list'), 

]
