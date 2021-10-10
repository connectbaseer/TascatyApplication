from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import tascaty_user
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = tascaty_user
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = tascaty_user
        fields = '__all__'


class UserLoginForm(forms.Form):
    username = forms.CharField(label='',
                               widget=forms.TextInput(
                                   attrs={
                                       "type": "username",
                                       "id": "inputusername",
                                       "class": "form-control form-border-top",
                                       "placeholder": "Username"
                                   }))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "type": "password",
                                       "id": "inputPassword",
                                       "class": "form-control form-border-bottom",
                                       "placeholder": "Password"
                                   }))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid Username/Password')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Passowrd')
            if not user.is_active:
                raise forms.ValidationError('This User is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)
