from django import forms
from django.contrib.auth.hashers import make_password

from .models import Customers


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        fields = ["username", "email", "phone_number", "address", "is_lender", "is_renter"]


class CustomerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput, help_text="Enter a password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Enter the password again for confirmation",
    )

    class Meta:
        model = Customers
        fields = [
            "username",
            "email",
            "phone_number",
            "address",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Customers.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.password = make_password(self.cleaned_data["password1"])
        if commit:
            customer.save()
        return customer
