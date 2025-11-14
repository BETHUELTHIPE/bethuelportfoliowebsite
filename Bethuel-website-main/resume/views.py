from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import ContactForm
from .models import Contact, EmailVerification
from .forms_registration import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.cache import cache


# Home view
def home(request):
    return render(request, "home.html")


# About view
def about(request):
    return render(request, "about.html")


# Projects view
def projects(request):
    projects_show = [
        {
            'title': 'cloud-computing-project',
            'path': 'images/serverless_DESIGN_project.png',
            'link': (
                'https://github.com/BETHUELTHIPE/cloud-computing-predict'
            ),
        },
        {
            'title': 'moving-big-data-project-airflow',
            'path': 'images/Streaming data.png',
            'link': (
                'https://github.com/BETHUELTHIPE/moving-big-data-predict-airflow'
            ),
        },
        {
            'title': 'data-migration-on-premise-to-aws',
            'path': 'images/Storingbigdata.png',
            'link': (
                'https://github.com/BETHUELTHIPE/data-migration-on-premise-to-aws'
            ),
        },
        {
            'title': 'Integrated-project',
            'path': 'images/etl_insurance_pipeline.jpg',
            'link': (
                'https://github.com/BETHUELTHIPE/Integrated-project'
            ),
        },
        {
            'title': 'processing-big-data-predict',
            'path': 'images/end-to-end-pipeline.jpg',
            'link': (
                'https://github.com/BETHUELTHIPE/processing-big-data-predict'
            ),
        },
        {
            'title': 'Store-BIG-DATA-PROJECT01',
            'path': 'images/end-to-end-pipeline.jpg',
            'link': (
                'https://github.com/BETHUELTHIPE/Store-BIG-DATA-PROJECT01'
            ),
        },
    ]
    context = {"projects_show": projects_show}
    return render(
        request,
        "projects.html",
        context
    )


# Experience view
def experience(request):
    experience = [
        {
            "company": "EXPLOREAI Cape Town South Africa",
            "position": "Data Engineer Intern",
        },
        {
            "company": "Department of Higher Education and Training",
            "position": "Mathematics and Physics Lecturer",
        },
        {
            "company": "Umalusi Quality Council",
            "position": (
                "Evaluator/Subject Specialist/Team Leader"
            ),
        },
        {
            "company": "Audrin Developers",
            "position": "Web Applications Developer",
        },
    ]
    context = {"experience": experience}
    return render(
        request,
        "experience.html",
        context
    )


# Certificate view
def certificate(request):
    return render(request, "certificate.html")


# Contact view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_obj = form.save()  # Save the form data to the database
            
            # Process contact form asynchronously
            from .tasks import process_contact_form
            process_contact_form.delay(
                contact_obj.name,
                contact_obj.email,
                contact_obj.phone,
                contact_obj.message
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



# Resume download view (verified login required)
@login_required(login_url='/login/')
def resume(request):
    # Check if user is verified
    if not request.user.is_active:
        messages.error(request, 'Please verify your email before downloading the resume.')
        return redirect('resend_verification')
    
    # Check if user has verified email
    try:
        verification = EmailVerification.objects.get(user=request.user)
        if not verification.is_verified:
            messages.error(request, 'Please verify your email before downloading the resume.')
            return redirect('resend_verification')
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Email verification required. Please complete registration.')
        return redirect('register')
    
    resume_path = "myapp/resume.pdf"
    if staticfiles_storage.exists(resume_path):
        with staticfiles_storage.open(resume_path, 'rb') as resume_file:
            body = resume_file.read()
            response = HttpResponse(
                body,
                content_type="application/pdf"
            )
            response['Content-Disposition'] = (
                'attachment; filename="Bethuel_Moukangwe_Resume.pdf"'
            )
            return response
    else:
        messages.error(request, 'Resume file not found. Please contact administrator.')
        return redirect('home')



# Custom registration with email verification
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            verification = EmailVerification.objects.create(user=user)
            verification_url = request.build_absolute_uri(
                f"/verify-email/{verification.token}/"
            )
            subject = 'Welcome to Bethuel Portfolio - Verify Your Email'
            message = (
                f"Hi {user.first_name},\n\n"
                f"Thank you for registering at Bethuel Portfolio!\n\n"
                f"Please verify your email address by clicking the link below:\n"
                f"{verification_url}\n\n"
                f"If you did not register, please ignore this email.\n\n"
                f"Best regards,\nBethuel Portfolio Team"
            )
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
            # Send verification email asynchronously
            from .tasks import send_verification_email
            try:
                send_verification_email.delay(user.id, verification_url)
                messages.success(request, 'Registration successful! Please check your email to verify your account.')
            except Exception as e:
                messages.warning(request, f'Registration successful, but email could not be sent. Error: {str(e)}')
            return redirect('registration_success')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Email verification view
# Email verification view
def verify_email(request, token):
    verification = get_object_or_404(EmailVerification, token=token)
    if not verification.is_verified:
        verification.is_verified = True
        verification.save()
        user = verification.user
        user.is_active = True
        user.save()
        return render(request, 'email_verified.html', {'user': user})
    else:
        return render(request, 'email_already_verified.html')


# Resend verification email view
def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                verification, created = EmailVerification.objects.get_or_create(user=user)
                verification_url = request.build_absolute_uri(f"/verify-email/{verification.token}/")
                subject = 'Resend: Verify Your Email for Bethuel Portfolio'
                message = (
                    f"Hi {user.first_name},\n\n"
                    f"Please verify your email address by clicking the link below:\n"
                    f"{verification_url}\n\n"
                    f"If you did not register, please ignore this email.\n\n"
                    f"Best regards,\nBethuel Portfolio Team"
                )
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
                try:
                    send_mail(subject, message, from_email, [user.email], fail_silently=False)
                    messages.success(request, 'Verification email sent successfully!')
                    return render(request, 'check_email.html', {'email': user.email, 'resent': True})
                except Exception as e:
                    messages.error(request, f'Could not send email. Error: {str(e)}')
            else:
                messages.info(request, 'This account is already active. Please login.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'resend_verification.html')


# Custom login view to check for verification
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(
                self.request, 
                'Please verify your email before logging in. '
                '<a href="/resend-verification/">Resend verification email</a>.'
            )
            return self.form_invalid(form)
        messages.success(self.request, f'Welcome back, {user.first_name}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


# Resume page view
def resume_page(request):
    return render(request, 'resume_protected.html')

# Success view
def success_view(request):
    return render(request, 'success.html')
