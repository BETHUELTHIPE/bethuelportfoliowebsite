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
            form.save()  # Save the form data to the database
            return redirect('success')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



# Resume download view (login required)
@login_required(login_url='/login/')
def resume(request):
    resume_path = "myapp/resume.pdf"
    if staticfiles_storage.exists(resume_path):
        with staticfiles_storage.open(resume_path, 'rb') as resume_file:
            body = resume_file.read()
            response = HttpResponse(
                body,
                content_type="application/pdf"
            )
            response['Content-Disposition'] = (
                'attachment; filename="resume.pdf"'
            )
            return response
    else:
        return HttpResponse(
            "Resume not found",
            status=404
        )



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
            from_email = settings.EMAIL_HOST_USER or 'noreply@bethuelportfolio.com'
            send_mail(
                subject,
                message,
                from_email,
                [user.email],
                fail_silently=False,
            )
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
                from_email = settings.EMAIL_HOST_USER or 'noreply@bethuelportfolio.com'
                send_mail(subject, message, from_email, [user.email], fail_silently=False)
                return render(request, 'check_email.html', {'email': user.email, 'resent': True})
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
            messages.error(self.request, 'Please verify your email before logging in. <a href="/resend-verification/">Resend verification email</a>.')
            return self.form_invalid(form)
        return super().form_valid(form)


# Success view
def success_view(request):
    return render(request, 'success.html')
