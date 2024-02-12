from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ckeditor.fields import RichTextField


# Create your models here.

class Profile(models.Model):
    USER_TYPES = [
        ("factory", "Factory"),
        ("accounts", "Accounts"),
        ("head_office", "Head Office"),
        ("super_admin", "Super Admin"),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='images/default.jpeg', upload_to='profile_pics')
    employee_id = models.CharField(max_length=256, blank=True)
    mobile_number = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(choices=USER_TYPES, max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user.username

    # reducing the image size
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Factory(models.Model):
    # unit_measurements=(("KG","KG"),("MT","MT"))
    name_of_raw_material = models.CharField(max_length=256)
    UoM = models.CharField(max_length=100)
    previous_supplier = models.CharField(max_length=256)
    estimated_delivery_time = models.CharField(max_length=256)
    vendor_location = models.CharField(max_length=256)
    minimum_stock_required_for_15days = models.CharField(max_length=100)
    current_stock = models.CharField(max_length=100)
    total_quantity_required = models.CharField(max_length=100)
    last_purchase_price = models.CharField(max_length=100, null=True, blank=True)
    last_purchase_value = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.previous_supplier


class Vendor(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)
    GST = models.CharField(max_length=100)
    bank_details = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name


class Quotation(models.Model):
    name_of_raw_material = models.CharField(max_length=256)
    purchase_rate_per_kg = models.CharField(max_length=256)
    delivery = models.CharField(max_length=256)
    payment_terms = models.CharField(max_length=256)
    freight = models.CharField(max_length=256)
    gst = models.CharField(max_length=256)
    name_of_vendor = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name_of_raw_material


class Post(models.Model):
    subject = models.CharField(max_length=256)
    body = RichTextField(blank=True, null=True)
    vendor_email = models.CharField(max_length=256)

    def __str__(self):
        return self.subject