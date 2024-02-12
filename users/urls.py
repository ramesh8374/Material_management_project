from django.contrib import admin
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

admin.site.site_header = "Amik Metals Admin"
admin.site.site_title = "Amik Metals Admin Portal"
admin.site.index_title = "Welcome to Amik Metals"

urlpatterns = [
    path('register',views.register,name='register'),
    path('',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('profile/',views.profile,name='profile'),
    path("factories/", views.factories, name="factories"),
    path("vendors/", views.vendors, name="vendors"),
    path("quotations/", views.quotations, name="quotations"),
    path("add_factory/", views.add_factory, name="add_factory"),
    path("add_vendor/", views.add_vendor, name="add_vendor"),
    path("add_quotation/", views.add_quotation, name="add_quotation"),
    path('factory/<int:pk>/' ,views.factory_details, name='factory_details'),
    path('vendor/<int:pk>/' ,views.vendor_details, name='vendor_details'),
    path('quotation/<int:pk>/' ,views.quotation_details, name='quotation_details'),
    path('factory/<int:pk>/delete' ,views.factory_delete, name='factory_delete'),
    path('vendor/<int:pk>/delete' ,views.vendor_delete, name='vendor_delete'),
    path('vendor/<int:pk>/delete' ,views.vendor_delete, name='vendor_delete'),
    path('quotation/<int:pk>/delete' ,views.quotation_delete, name='quotation_delete'),
    path('send-indent' ,views.send_indent, name='send_indent'),
    path('comparision' ,views.comparision, name='comparision'),
    path('send_po' ,views.send_po, name='send_po'),
]