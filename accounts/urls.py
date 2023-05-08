
from django.urls import path,re_path, include
from .views import *

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('anonymous/create/', CreateAnonymousUserView.as_view()),
    path('anonymous/convert/', ConvertAnonymousUserView.as_view()),
    path('auth/login/', MyLoginView.as_view(), name='account_login'),
    path('auth/signup/', MySignUpView.as_view(), name='account_signup'),
    path('auth/password/reset/', MyPasswordResetView.as_view(), name='account_reset_password'),
    path('auth/password/reset/key/done/', MyPasswordResetKeyDoneView.as_view(), name='account_reset_password_key_done'),
    re_path(
        r"^auth/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        MyPasswordResetKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path('auth/password/reset/done/', MyPasswordResetDoneView.as_view(), name='account_reset_password_done'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('auth/confirm-email/<str:key>/', MyConfirmEmailView.as_view(), name='account_confirm_email'),
    path('auth/logout/', MyLogoutView.as_view(), name='logout'),
    path('auth/email/confirmation/done/', email_confirmation_done, name='email_confirmation_done'),
    path('accounts/email/confirm/<str:key>/', MyConfirmEmailView.as_view(), name='account_confirm_email'),
    path('auth/email/', MyEmailView.as_view(), name='email'),
    path('auth/', include('allauth.urls')),
    path('current-user/', CustomUserDetailsView.as_view(), name='user_details'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    re_path(r"password_reset_confirm/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", MyPasswordResetKeyView.as_view(), name='password_reset_confirm'),
]