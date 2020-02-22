from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Company


class CustomUserCreationForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)


class CustomUserChangeForm(UserChangeForm):

    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email',)


class CompanyRegistrationForm(forms.ModelForm):

    company_name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Company
        fields = ('company_name', 'description', 'selling_price', )
