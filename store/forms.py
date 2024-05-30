# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Customer, Product
from django.core.exceptions import ValidationError

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

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        # Autofill initial values for full name and phone using Customer model
        user = kwargs.pop('user', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            try:
                customer = Customer.objects.get(user=user)
                self.fields['full_name'].initial = customer.get_full_name()
                self.fields['phone'].initial = customer.phone
            except Customer.DoesNotExist:
                pass

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category', 'stock']
