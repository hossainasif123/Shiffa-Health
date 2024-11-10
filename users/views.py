from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, smart_bytes, smart_str
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages

from .models import User
from .tokens import email_verification_token
from .forms import PasswordResetRequestForm, SetNewPasswordForm, PatientSignUpForm, LoginForm

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'users/home.html'
    login_url = 'users:login'


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'users/main.html'
    login_url = 'users:login'

class PatientSignUpView(View):
    template_name = 'users/signup.html'

    def get(self, request, *args, **kwargs):
        form = PatientSignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet, to modify before saving
            user.is_active = False  # Deactivate until email verification
            user.save()
            
            token = email_verification_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_url = f"{request.scheme}://{request.get_host()}{reverse('users:email-verify', kwargs={'uidb64': uid, 'token': token})}"
            
            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('users:email_verification_sent')  # Redirect to a confirmation page
        return render(request, self.template_name, {'form': form})


class EmailVerificationView(View):
    template_name = 'users/email_verification.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, self.template_name, {'error': 'Invalid request'})
        
        if user.is_active:
            return render(request, self.template_name, {'message': 'Account already activated'})

        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('users:dashboard')
        else:
            return render(request, self.template_name, {'error': 'Invalid or expired token.'})


class EmailVerificationSentView(TemplateView):
    template_name = 'users/email_verification_sent.html'
    


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # Authenticate using username (which is actually the email in this case)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:dashboard')  # Redirect to a user dashboard after login
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    login_url = 'users:login'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('users:login')
    
    


class PasswordResetRequestView(View):
    template_name = 'users/password_reset_request.html'

    def get(self, request, *args, **kwargs):
        form = PasswordResetRequestForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = email_verification_token.make_token(user)
                uid = urlsafe_base64_encode(smart_bytes(user.pk))
                reset_url = f"{request.scheme}://{request.get_host()}{reverse('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

                # Email content
                mail_subject = 'Reset your password'
                message = render_to_string('users/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                
                send_mail(
                    mail_subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "Password reset email has been sent.")
                return redirect('users:password_reset_done')
            else:
                form.add_error('email', 'No account found with this email.')
        return render(request, self.template_name, {'form': form})


class PasswordResetConfirmView(View):
    template_name = 'users/password_reset_confirm.html'

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            form = SetNewPasswordForm(user=user)
            return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'The password reset link was invalid or expired.')
            return redirect('users:password_reset_request')

    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            form = SetNewPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('users:login')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'The password reset link was invalid or expired.')
            return redirect('users:password_reset_request')


