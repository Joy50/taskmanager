from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer  # You need to create this serializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_registration_email(user)

    def send_registration_email(user):
        subject = 'Registration Confirmation'
        message = 'Thank you for registering on our site.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        return Response({'token': token})

class PasswordResetView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer  # You need to create this serializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_password_reset_email(user)

class PasswordResetView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = PasswordResetSerializer  # You need to create this serializer

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_password_reset_email(user)

    def send_password_reset_email(self, user):
        subject = 'Password Reset'
        message = f'Click the link to reset your password: {self.get_password_reset_link(user)}'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]

        send_mail(subject, message, from_email, to_email)

    def get_password_reset_link(self, user):
        # Use Django's built-in password reset functionality to generate the link
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f'http://your-frontend-url/reset-password/{uid}/{token}/'
        return reset_url
