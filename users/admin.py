from django.contrib import admin
from .models import Profile, Factory, Vendor, Quotation, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(Factory)
admin.site.register(Vendor)
admin.site.register(Quotation)
admin.site.register(Post)