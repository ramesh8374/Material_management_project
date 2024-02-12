from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegister, UserCreation, ProfileForm, FactoryForm, VendorForm, QuotationForm, PostForm
from users.models import Profile, Factory, Vendor, Quotation, Post
from django.contrib.auth import login, authenticate, logout
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .utils import send_email_to_user


@login_required
# Create your views here.
def register(request):
    if request.user.profile.role == "super_admin":
        u_form = UserRegister()
        p_form = ProfileForm()
        if request.method == 'POST':
            u_form = UserRegister(request.POST)
            p_form = ProfileForm(request.POST)
            if u_form.is_valid and p_form.is_valid:
                user = u_form.save()
                profile = p_form.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect(register)
            else:
                return render(request, 'register.html', {'u_form': u_form, "p_form": p_form})
        return render(request, 'register.html', {'u_form': u_form, "p_form": p_form})
    else:
        return HttpResponse("You dont  have access ")


@login_required
def profile(request):
    u_form = UserCreation(instance=request.user)
    p_form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        u_form = UserCreation(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST,
                             request.FILES,
                             instance=request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect(register)
    return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})


def delete(request, id):
    queryset = Profile.objects.get(id=id)
    queryset.delete()
    return redirect(register)


def factories(request):
    first_row = Factory.objects.first()
    context = {
        "factories": Factory.objects.all(),
        "vendors": Vendor.objects.all()
    }
    return render(request, template_name="factories.html", context=context)


def add_factory(request):
    if request.user.profile.role in ['factory', 'head_office', 'super_admin']:
        if request.method == "POST":
            form = FactoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Factory details are entered correctly")
                return redirect(factories)
            else:
                messages.error(request, "please provide valid details")
                return redirect(add_factory)
        else:
            form = FactoryForm()
            return render(request, template_name="add_factory.html", context={"factory_form": form})
    else:
        return HttpResponse('dont have permission to access this')


def factory_details(request, pk):
    if request.method == "GET":
        factory = Factory.objects.get(id=pk)
        form = FactoryForm(instance=factory)
        return render(request, template_name="update_factory.html", context={"factory_form": form})

    if request.method == "POST":
        factory = Factory.objects.get(id=pk)
        form = FactoryForm(instance=factory, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Factory details are entered correctly")
            return redirect(factories)
        else:
            messages.error(request, "please provide valid details")


def factory_delete(request, pk):
    factory = Factory.objects.get(id=pk)
    factory.delete()
    return redirect(factories)


def vendors(request):
    if request.user.profile.role in ['head_office', 'super_admin']:
        first_row = Vendor.objects.first()
        context = {
            "vendors": Vendor.objects.all()
        }
        return render(request, template_name="vendors.html", context=context)
    else:
        return HttpResponse('<h1>Dont have permission to access this page</h1>')


def add_vendor(request):
    if request.user.profile.role in ['head_office', 'super_admin']:
        if request.method == "POST":
            form = VendorForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Vendor details are entered correctly")
                return redirect(vendors)
            else:
                messages.error(request, "please provide valid details")
                return redirect(add_vendor)
        else:
            form = VendorForm()
            return render(request, template_name="add_vendor.html", context={"vendor_form": form})
    else:
        return HttpResponse('<h1>Dont have permission to access this page</h1>')


def vendor_details(request, pk):
    if request.user.profile.role in ['head_office', 'super_admin']:
        if request.method == "GET":
            vendor = Vendor.objects.get(id=pk)
            form = VendorForm(instance=vendor)
            return render(request, template_name="update_vendor.html", context={"vendor_form": form})
        if request.method == "POST":
            vendor = Vendor.objects.get(id=pk)
            form = VendorForm(instance=vendor, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Vendor details are entered correctly")
                return redirect(vendors)
            else:
                messages.error(request, "please provide valid details")
    else:
        return HttpResponse("<h1>Dont have permission to access this page</h1>")


def vendor_delete(request, pk):
    vendor = Vendor.objects.get(id=pk)
    vendor.delete()
    return redirect(vendors)


def send_indent(request):
    if request.user.profile.role in ['head_office', 'super_admin']:
        if request.method == "POST":
            meterials = request.POST.getlist("meterials")
            vendors = request.POST.getlist("vendors")
            factory_meterials = Factory.objects.filter(name_of_raw_material__in=meterials)
            vendor_emails = [vendor.email for vendor in Vendor.objects.all()]
            mail_body = render_to_string("material_details.html", {"meterials": factory_meterials})
            send_mail(subject="Factory Details", from_email=settings.EMAIL_HOST_USER, recipient_list=vendor_emails,
                      html_message=mail_body, message=mail_body)
        return HttpResponse("<h1> Indent sent Successfully to Vendor </h1>")
    else:
        return HttpResponse("<h1>Dont have permission to access this page</h1>")


def quotations(request):
    if request.user.profile.role in ['head_office', 'super_admin']:
        first_row = Quotation.objects.first()
        context = {
            "quotations": Quotation.objects.all(),
            "vendors": Vendor.objects.all()
        }
        return render(request, template_name="quotations.html", context=context)
    else:
        return HttpResponse("<h1>Dont have permission to access this page</h1>")


def add_quotation(request):
    if request.method == "POST":
        form = QuotationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Quotation details are entered correctly")
            return HttpResponse("<h1>Quotation Submitted Successfully</h1>")
        else:
            messages.error(request, "please provide valid details")
            return redirect(add_quotation)
    else:
        form = QuotationForm()
        return render(request, template_name="add_quotation.html", context={"quotation_form": form})


def quotation_details(request, pk):
    if request.user.profile.role in ['head_office', 'super_admin']:
        if request.method == "GET":
            quotation = Quotation.objects.get(id=pk)
            form = QuotationForm(instance=quotation)
            return render(request, template_name="update_quotation.html", context={"quotation_form": form})

        if request.method == "POST":
            quotation = Quotation.objects.get(id=pk)
            form = QuotationForm(instance=quotation, data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Quotation details are entered correctly")
                return redirect(quotations)
            else:
                messages.error(request, "please provide valid details")
    else:
        return HttpResponse("<h1>Dont have permission to access this page</h1>")


def quotation_delete(request, pk):
    factory = Quotation.objects.get(id=pk)
    factory.delete()
    return redirect(quotations)


def comparision(request):
    first_row = Factory.objects.first()
    context = {
        "materials": Factory.objects.all().distinct(),
        "vendors": Vendor.objects.all(),
        "quotations": Quotation.objects.all()
    }
    return render(request, "comparision.html", context=context)


def send_po(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            subject = request.POST.get('subject')
            body = request.POST.get('body')
            vendor_email = request.POST.get('vendor_email')

            send_mail(subject=subject, from_email=settings.EMAIL_HOST_USER, recipient_list=[vendor_email],
                      html_message=body, message=body)
            return HttpResponse('Email send successfully!!')
    return render(request, 'quotation_details.html', {'post_form': form})

