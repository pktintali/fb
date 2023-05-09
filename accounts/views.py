from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
from dj_rest_auth.views import UserDetailsView, PasswordResetView as prvdj
from allauth.account.views import LoginView, PasswordResetView as APasswordResetView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView, PasswordResetDoneView, ConfirmEmailView, LogoutView, EmailView, ConfirmEmailView, SignupView
from .serializers import CustomUserSerializer

from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from api.models import UserTasks


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
import uuid
from django.contrib.auth import authenticate, login

from api.models import User

from accounts.permissions import FullAccessWithoutAuthentication


@method_decorator(csrf_exempt, name='dispatch')
class CreateAnonymousUserView(APIView):
    permission_classes = [FullAccessWithoutAuthentication]

    def post(self, request):
        User = get_user_model()
        first_name = request.data.get('name1')
        last_name = request.data.get('name2')
        if first_name:
            username = '{}_{}'.format(first_name, uuid.uuid4())
        else:
            username = 'anonymous_{}'.format(uuid.uuid4())
        email = '{}@example.com'.format(username)
        if first_name and last_name:
            user = User.objects.create_user(
                username=username, email=email, first_name=first_name, last_name=last_name)
        elif first_name:
            user = User.objects.create_user(
                username=username, email=email, first_name=first_name)
        else:
            user = User.objects.create_user(username=username, email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'key': token.key}, status=status.HTTP_201_CREATED)


class ConvertAnonymousUserView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(username=request.user.username).first()

        if user is None:
            # The anonymous user doesn't exist, return an error response
            return Response({'error': 'Anonymous user not found'}, status=status.HTTP_404_NOT_FOUND)

        email_already_exist = EmailAddress.objects.filter(email=email).exists()
        email_already_exist2 = User.objects.filter(email=email).exists()
        if email_already_exist or email_already_exist2:
            return Response({'error': 'email already in use'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        # Set the user's email and password
        user.email = email
        user.set_password(password)
        user.save()

        # Create a new EmailAddress record for the user
        email_address = EmailAddress.objects.create(
            user=user, email=email, primary=True, verified=False)

        # Log the user in with their new credentials
        user = authenticate(
            request=request, username=user.username, password=password)
        if user is not None:
            login(request, user)

            # Generate a new token for the user
            # token, _ = Token.objects.get_or_create(user=user)

            #! Verify password reset link is working or not
            # Send an email verification link to the user's email address
            send_email_confirmation(
                self.request, user, email=email
            )

            # Return the new token in the response
            return Response({'success': True})

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserSerializer

    #! Linked with front-end streak and task number logic
    def retrieve(self, request, *args, **kwargs):
        # update user streak
        user = self.get_object()
        last_seen = user.last_seen
        now = datetime.now()
        if last_seen.date() < now.date():
            days_since_last_seen = (now.date() - last_seen.date()).days
            if days_since_last_seen == 1:
                # Increment streak if user was last seen yesterday
                user.streak += 1
            else:
                # Reset streak to zero if more than a day has passed and delete tasks
                user.streak = 0
                user_tasks = UserTasks.objects.filter(
                    user=user).exclude(task_number__in=[1, 2])
                user_tasks.delete()

            # Check if user has reached a milestone and set showAlert accordingly
            if user.streak in [5, 10, 20, 40, 80, 160, 320, 640]:
                showAlert = True
                user.coins += (user.streak*20)
                if user.streak == 5:
                    UserTasks.objects.create(user=user, task_number=3)
                elif user.streak == 10:
                    UserTasks.objects.create(user=user, task_number=4)
                elif user.streak == 20:
                    UserTasks.objects.create(user=user, task_number=5)
                elif user.streak == 40:
                    UserTasks.objects.create(user=user, task_number=6)
                elif user.streak == 80:
                    UserTasks.objects.create(user=user, task_number=7)
                elif user.streak == 160:
                    UserTasks.objects.create(user=user, task_number=8)
                elif user.streak == 320:
                    UserTasks.objects.create(user=user, task_number=9)
                elif user.streak == 640:
                    UserTasks.objects.create(user=user, task_number=10)
            else:
                showAlert = False

            # Serialize user data and add showAlert attribute
            serializer = self.get_serializer(user)
            response_data = serializer.data
            response_data['show_alert'] = showAlert
            # save the user
            user.save()

        else:
            # get serialized user data
            serializer = self.get_serializer(user)
            response_data = serializer.data
            user_model = self.get_queryset().model
            user_model.objects.filter(pk=user.pk).update(
                last_seen=timezone.now())
        return Response(response_data)


class ProfileView(TemplateView):
    template_name = 'custom/profile.html'


class CustomPasswordResetView(prvdj):
    pass


class MyConfirmEmailView(ConfirmEmailView):
    template_name = 'custom/email_confirm.html'


class MyLoginView(LoginView):
    template_name = 'custom/login.html'


class MySignUpView(SignupView):
    template_name = 'custom/signup.html'


class MyPasswordResetView(APasswordResetView):
    template_name = 'custom/password_reset.html'


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'custom/password_reset_done.html'


class MyPasswordResetKeyView(PasswordResetFromKeyView):
    template_name = 'custom/password_reset_from_key.html'


class MyPasswordResetKeyDoneView(PasswordResetFromKeyDoneView):
    template_name = 'custom/password_reset_from_key_done.html'


class MyLogoutView(LogoutView):
    template_name = 'custom/logout.html'


class MyEmailView(EmailView):
    template_name = 'custom/email.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/auth/login')
        return super().dispatch(request, *args, **kwargs)


def email_confirmation_done(request):
    message = "Your email address has been confirmed!"
    return render(request, 'custom/email_confirmation_done.html', {'message': message})


class MyConfirmEmailView(ConfirmEmailView):
    template_name = 'custom/email_confirm.html'
    success_url = 'account/auth/email/confirmation/done'
