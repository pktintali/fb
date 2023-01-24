from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
from dj_rest_auth.views import UserDetailsView,PasswordResetView as prvdj
from allauth.account.views import LoginView,PasswordResetView as APasswordResetView,PasswordResetFromKeyView,PasswordResetFromKeyDoneView,PasswordResetDoneView,ConfirmEmailView,LogoutView, EmailView,ConfirmEmailView,SignupView
from .serializers import CustomUserSerializer

class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserSerializer

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