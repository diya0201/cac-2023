from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    join_code = forms.CharField(max_length=6, required=True,
                                help_text="Enter the group join code provided by your educator.")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'join_code', 'password1', 'password2')
