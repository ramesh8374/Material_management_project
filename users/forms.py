from django import forms
from django.contrib.auth.models import User
from .models import Profile, Factory, Vendor, Quotation, Post
from django.contrib.auth.forms import UserCreationForm
from ckeditor.fields import RichTextField


class UserRegister(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserCreation(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['employee_id', 'role', 'mobile_number']


class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = ("name_of_raw_material", "UoM", "previous_supplier", "estimated_delivery_time", "vendor_location",
                  "minimum_stock_required_for_15days", "current_stock", "total_quantity_required",
                  "last_purchase_price", "last_purchase_value")


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ("name", "address", "phone_number", "GST", "bank_details", "email")


class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = (
        "name_of_raw_material", "name_of_vendor", "purchase_rate_per_kg", "delivery", "payment_terms", "freight", "gst",
        "phone_number")


class PostForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput(), required=True, max_length=256)
    body = RichTextField()
    vendor_email = forms.CharField(widget=forms.TextInput(), required=True, max_length=256)

    class Meta:
        model = Post
        fields = ('subject', 'body', 'vendor_email')
