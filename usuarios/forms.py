from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email or Username')



