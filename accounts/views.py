from datetime import datetime
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
from dj_rest_auth.views import UserDetailsView, PasswordResetView as prvdj
from allauth.account.views import LoginView, PasswordResetView as APasswordResetView, PasswordResetFromKeyView, PasswordResetFromKeyDoneView, PasswordResetDoneView, ConfirmEmailView, LogoutView, EmailView, ConfirmEmailView, SignupView
from .serializers import CustomUserSerializer

from api.models import UserTasks

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
                if user.streak == 5:
                    user.coins += 100
                elif user.streak == 10:
                    user.coins += 200
                elif user.streak == 20:
                    user.coins += 400
                elif user.streak == 40:
                    user.coins += 800
                elif user.streak == 80:
                    user.coins += 1600
                elif user.streak == 160:
                    user.coins += 3200
                elif user.streak == 320:
                    user.coins += 6400
                elif user.streak == 640:
                    user.coins += 12800
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
        return Response(serializer.data)


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
