from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Company, Shares, Transaction


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

    company_name = forms.CharField(
        max_length=100, required=True, help_text="Company Name", widget=forms.TextInput(attrs={'type': 'text'}))
    description = forms.CharField(
        max_length=200, required=True, help_text="Description", widget=forms.TextInput(attrs={'type': 'text'}))
    selling_price = forms.DecimalField(
        required=True, help_text="Rs.", widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = Company
        fields = ('company_name', 'description', 'selling_price', )


class CompanySharesUpdateForm(forms.ModelForm):

    class Meta:
        model = Shares
        fields = ('shares_count',)


class SharesSaleUpdateForm(forms.ModelForm):

    class Meta:
        model = Shares
        fields = ('shares_sale',)


class BuySharesUpdateForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('shares_count',)
