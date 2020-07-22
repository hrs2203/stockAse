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
    company_code = forms.CharField(
        max_length=100, required=True, help_text="Company Code", widget=forms.TextInput(attrs={'type': 'text'}))
    company_key = forms.CharField(max_length=100, required=True,
                                  help_text="Company Key", widget=forms.TextInput(attrs={'type': 'text'}))
    description = forms.CharField(max_length=200, required=True,
                                  help_text="Description", widget=forms.TextInput(attrs={'type': 'text'}))
    selling_price = forms.DecimalField(
        required=True, help_text="Rs.", widget=forms.NumberInput(attrs={'type': 'number'}))

    class Meta:
        model = Company
        fields = ('company_name', 'description', 'selling_price',
                  'company_code', 'company_key', )


class CompanySharesUpdateForm(forms.ModelForm):

    price = forms.DecimalField()

    class Meta:
        model = Shares
        fields = ('shares_count', 'price',)

    def get_price(self, obj):
        return obj.company.selling_price


class SharesSaleUpdateForm(forms.ModelForm):

    class Meta:
        model = Shares
        fields = ('shares_sale',)


class BuySharesUpdateForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('shares_count',)
