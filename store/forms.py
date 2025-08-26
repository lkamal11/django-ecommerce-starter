from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    phone = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        # All fields except email/phone are required by default
        for field in ['username', 'first_name', 'last_name', 'password', 'confirm_password']:
            if not cleaned_data.get(field):
                self.add_error(field, "This field is required.")

        # At least one of email or phone is required
        if not email and not phone:
            raise forms.ValidationError("At least one of Email or Phone number is required.")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    address = forms.CharField(max_length=300)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20)

class EmailOrPhoneLoginForm(forms.Form):
    username = forms.CharField(label="Email or Phone")
    password = forms.CharField(widget=forms.PasswordInput)
