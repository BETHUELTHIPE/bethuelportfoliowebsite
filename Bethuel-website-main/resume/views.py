from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import ContactForm, SubscriptionForm
from .models import Contact, EmailVerification, LoginVerification, UserRegistrationAnalytics, ResumeDownloadAnalytics, BlogPost, Testimonial, Skill, EmailSubscriber, Announcement
from .forms_registration import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.cache import cache


# Home view
def home(request):
    testimonials = Testimonial.objects.filter(is_featured=True)[:3]
    skills = Skill.objects.filter(is_featured=True)
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    context = {
        'testimonials': testimonials,
        'skills': skills,
        'recent_posts': recent_posts,
    }
    return render(request, "home_v3.html", context)


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
            
            # Track resume download analytics
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip
            
            ResumeDownloadAnalytics.objects.create(
                user=request.user,
                ip_address=get_client_ip(request)
            )
            
            return response
    else:
        messages.error(request, 'Resume file not found. Please contact administrator.')
        return redirect('home')


# Email resume delivery
@login_required(login_url='/login/')
def email_resume(request):
    # Check if user is verified
    if not request.user.is_active:
        messages.error(request, 'Please verify your email before requesting resume.')
        return redirect('resend_verification')
    
    try:
        verification = EmailVerification.objects.get(user=request.user)
        if not verification.is_verified:
            messages.error(request, 'Please verify your email before requesting resume.')
            return redirect('resend_verification')
    except EmailVerification.DoesNotExist:
        messages.error(request, 'Email verification required.')
        return redirect('register')
    
    # Send resume via email
    from django.core.mail import EmailMessage
    from django.contrib.staticfiles.storage import staticfiles_storage
    
    resume_path = "myapp/resume.pdf"
    if staticfiles_storage.exists(resume_path):
        subject = 'Your Requested Resume - Bethuel Moukangwe'
        message = f"""Dear {request.user.first_name or request.user.username},

Thank you for your interest in my professional profile! Please find my resume attached to this email.

🌐 Website: http://ec2-34-252-250-140.eu-west-1.compute.amazonaws.com
📍 Office Address: 27 Tshivhase Street, Atteridgeville 0008
📱 Cell: 071 415 6665
📧 Email: bethuelmoukangwe8@gmail.com

I would be delighted to discuss potential opportunities with you. Please feel free to:
• Contact me via phone or email for any inquiries
• Visit my office for a face-to-face consultation
• Explore my portfolio website for detailed project information
• Connect with me on LinkedIn for professional networking

As Director of AmarisLearningHub, I am passionate about leveraging technology to solve real-world problems and providing quality education through innovative solutions. I would welcome the opportunity to contribute to your organization's success.

Looking forward to hearing from you soon!

Best regards,
Bethuel Moukangwe
Director - AmarisLearningHub
Python (Django) Developer & Online Maths Tutor

---
This email was sent from my professional portfolio website.
For more information, visit: http://ec2-34-252-250-140.eu-west-1.compute.amazonaws.com"""
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'bethuelmoukangwe8@gmail.com')
        
        # Create email with attachment
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[request.user.email],
        )
        
        # Attach resume PDF
        with staticfiles_storage.open(resume_path, 'rb') as resume_file:
            email.attach('Bethuel_Moukangwe_Resume.pdf', resume_file.read(), 'application/pdf')
        
        try:
            email.send()
            
            # Track email delivery analytics
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip
            
            ResumeDownloadAnalytics.objects.create(
                user=request.user,
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, f'Resume has been sent to {request.user.email}! Please check your inbox.')
        except Exception as e:
            messages.error(request, f'Failed to send resume via email. Error: {str(e)}')
    else:
        messages.error(request, 'Resume file not found. Please contact administrator.')
    
    return redirect('resume_page')



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
            # Send verification email
            try:
                send_mail(subject, message, from_email, [user.email], fail_silently=False)
                messages.success(request, 'Registration successful! Please check your email to verify your account.')
            except Exception as e:
                messages.warning(request, f'Registration successful, but email could not be sent. Error: {str(e)}')
            
            # Track registration analytics
            from django.utils import timezone
            today = timezone.now().date()
            analytics, created = UserRegistrationAnalytics.objects.get_or_create(
                date=today,
                defaults={'count': 1}
            )
            if not created:
                analytics.count += 1
                analytics.save()
            
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


# Custom login view with 2FA
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
        
        # Generate and send 6-digit code
        verification = LoginVerification.generate_code(user)
        subject = 'Login Verification Code - Bethuel Portfolio'
        message = (
            f"Hi {user.first_name},\n\n"
            f"Your login verification code is: {verification.code}\n\n"
            f"This code will expire in 10 minutes.\n\n"
            f"If you did not attempt to login, please ignore this email.\n\n"
            f"Best regards,\nBethuel Portfolio Team"
        )
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
        
        try:
            send_mail(subject, message, from_email, [user.email], fail_silently=False)
            # Store user in session for verification step
            self.request.session['pending_user_id'] = user.id
            messages.success(self.request, 'Verification code sent to your email!')
            return redirect('verify_login_code')
        except Exception as e:
            messages.error(self.request, f'Could not send verification code. Error: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)


# Resume page view
def resume_page(request):
    return render(request, 'resume_protected.html')

# Verify login code view
def verify_login_code(request):
    if 'pending_user_id' not in request.session:
        messages.error(request, 'No pending login verification.')
        return redirect('login')
    
    if request.method == 'POST':
        code = request.POST.get('code')
        user_id = request.session['pending_user_id']
        
        try:
            user = User.objects.get(id=user_id)
            verification = LoginVerification.objects.filter(
                user=user, code=code, is_used=False
            ).first()
            
            if verification and not verification.is_expired():
                verification.is_used = True
                verification.save()
                auth_login(request, user)
                del request.session['pending_user_id']
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid or expired verification code.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid session.')
            return redirect('login')
    
    return render(request, 'verify_login_code.html')


# Analytics dashboard view (admin only)
@login_required
def analytics_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta
    
    # Get last 30 days of registration data
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    registration_data = UserRegistrationAnalytics.objects.filter(
        date__gte=thirty_days_ago
    ).order_by('date')
    
    # Get resume download stats
    total_downloads = ResumeDownloadAnalytics.objects.count()
    downloads_today = ResumeDownloadAnalytics.objects.filter(
        downloaded_at__date=timezone.now().date()
    ).count()
    
    # Get recent downloads
    recent_downloads = ResumeDownloadAnalytics.objects.select_related('user').order_by('-downloaded_at')[:10]
    
    # Get total users
    total_users = User.objects.count()
    verified_users = User.objects.filter(is_active=True).count()
    
    context = {
        'registration_data': registration_data,
        'total_downloads': total_downloads,
        'downloads_today': downloads_today,
        'recent_downloads': recent_downloads,
        'total_users': total_users,
        'verified_users': verified_users,
    }
    
    return render(request, 'analytics_dashboard.html', context)


# Blog views
def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save()
    return render(request, 'blog_detail.html', {'post': post})

# Subscription views
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            try:
                subscriber = form.save()
                # Send welcome email
                subject = 'Welcome to Bethuel Portfolio Newsletter!'
                message = f"""Hi {subscriber.name or 'there'},

Thank you for subscribing to my newsletter! You'll receive updates about:
- New blog posts and insights
- Project announcements
- Career updates and achievements
- Technical tutorials and tips

You can unsubscribe anytime using the link in our emails.

Best regards,
Bethuel Moukangwe"""
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
                send_mail(subject, message, from_email, [subscriber.email], fail_silently=False)
                messages.success(request, 'Successfully subscribed! Check your email for confirmation.')
            except Exception as e:
                if 'UNIQUE constraint' in str(e):
                    messages.info(request, 'You are already subscribed to our newsletter.')
                else:
                    messages.error(request, 'Subscription failed. Please try again.')
            return redirect('home')
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

def unsubscribe(request, token):
    try:
        subscriber = EmailSubscriber.objects.get(unsubscribe_token=token)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, 'Successfully unsubscribed from newsletter.')
    except EmailSubscriber.DoesNotExist:
        messages.error(request, 'Invalid unsubscribe link.')
    return render(request, 'unsubscribe.html')

@login_required
def send_announcement(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            announcement = Announcement.objects.create(title=title, content=content)
            
            # Send to all active subscribers
            subscribers = EmailSubscriber.objects.filter(is_active=True)
            recipient_emails = [sub.email for sub in subscribers]
            
            if recipient_emails:
                subject = f'Announcement: {title}'
                message = f"""{content}

---
Best regards,
Bethuel Moukangwe

Unsubscribe: {{unsubscribe_url}}"""
                
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
                
                # Send emails with unsubscribe links
                for subscriber in subscribers:
                    unsubscribe_url = request.build_absolute_uri(f'/unsubscribe/{subscriber.unsubscribe_token}/')
                    personalized_message = message.replace('{unsubscribe_url}', unsubscribe_url)
                    send_mail(subject, personalized_message, from_email, [subscriber.email], fail_silently=True)
                
                announcement.is_sent = True
                announcement.sent_at = timezone.now()
                announcement.recipients_count = len(recipient_emails)
                announcement.save()
                
                messages.success(request, f'Announcement sent to {len(recipient_emails)} subscribers!')
            else:
                messages.warning(request, 'No active subscribers found.')
        else:
            messages.error(request, 'Title and content are required.')
    
    return render(request, 'send_announcement.html')

# Success view
def success_view(request):
    return render(request, 'success.html')
