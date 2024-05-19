# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Customer

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(
        max_length=254,
        required=True,
        label="Username (Email)"
    )
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],  # Gunakan alamat email sebagai username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        customer = super(RegisterForm, self).save(commit=False)
        customer.user = user
        if commit:
            customer.save()
        return customer