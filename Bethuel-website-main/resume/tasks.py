from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import time

@shared_task
def send_email_async(subject, message, from_email, recipient_list):
    """Send email asynchronously using Celery"""
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return f"Email sent successfully to {recipient_list}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

@shared_task
def send_verification_email(user_id, verification_url):
    """Send verification email asynchronously"""
    from django.contrib.auth.models import User
    
    try:
        user = User.objects.get(id=user_id)
        subject = 'Welcome to Bethuel Portfolio - Verify Your Email'
        message = f"""Hi {user.first_name},

Thank you for registering at Bethuel Portfolio!

Please verify your email address by clicking the link below:
{verification_url}

If you did not register, please ignore this email.

Best regards,
Bethuel Portfolio Team"""
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
        send_mail(subject, message, from_email, [user.email], fail_silently=False)
        return f"Verification email sent to {user.email}"
    except Exception as e:
        return f"Failed to send verification email: {str(e)}"

@shared_task
def process_contact_form(name, email, phone, message):
    """Process contact form submission asynchronously"""
    # Simulate processing time
    time.sleep(2)
    
    # Send notification email to admin
    subject = f'New Contact Form Submission from {name}'
    admin_message = f"""
    New contact form submission:
    
    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'bethuelmoukangwe8@gmail.com')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bethuelportfolio.com')
    
    send_mail(subject, admin_message, from_email, [admin_email], fail_silently=False)
    return f"Contact form processed for {name}"