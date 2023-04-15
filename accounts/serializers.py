from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomUserSerializer(UserDetailsSerializer):
    show_alert = serializers.BooleanField(default=False)
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'premium'):
            extra_fields.append('premium')
        if hasattr(UserModel, 'redeemedPremium'):
            extra_fields.append('redeemedPremium')
        if hasattr(UserModel, 'coins'):
            extra_fields.append('coins')
        if hasattr(UserModel, 'avtar'):
            extra_fields.append('avtar')
        if hasattr(UserModel, 'streak'):
            extra_fields.append('streak')
        if hasattr(UserModel, 'last_seen'):
            extra_fields.append('last_seen')
        if hasattr(UserModel, 'premium_start_date'):
            extra_fields.append('premium_start_date')
        if hasattr(UserModel, 'premium_end_date'):
            extra_fields.append('premium_end_date')
        if hasattr(UserModel, 'shared_fact_counts'):
            extra_fields.append('shared_fact_counts')
        if hasattr(UserModel, 'is_staff'):
            extra_fields.append('is_staff')
        extra_fields.append('show_alert')
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)