from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import PetOwnerSignUpSerializer, LoginSerializer
from .tokens import email_verification_token
from .models import User

class PetOwnerSignUpView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PetOwnerSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(commit=False) 
            user.is_active = False  
            user.save()
            
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
            return Response({'message': 'Please check your email to confirm your registration.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({'message': 'Account already activated'}, status=status.HTTP_200_OK)
        
        if email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email successfully verified. You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'role': user.role}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
