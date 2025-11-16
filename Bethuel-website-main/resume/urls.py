from django.urls import path
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

from .views import (
    home,
    about,
    projects,
    experience,
    certificate,
    contact,
    success_view,
    resume,
    resume_page,
    email_resume,
    register,
    verify_email,
    resend_verification,
    CustomLoginView,
    verify_login_code,
    analytics_dashboard,
    blog_list,
    blog_detail,
    subscribe,
    unsubscribe,
    send_announcement,
)


urlpatterns = [
    path('', home, name='home'),
    path('test/', lambda request: HttpResponse('<h1>TEST PAGE WORKS!</h1><p>Django is working properly.</p>'), name='test'),
    path('about/', about, name='about'),
    path('projects/', projects, name='projects'),
    path('experience/', experience, name='experience'),
    path('contact/', contact, name='contact'),
    path('resume/', resume, name='resume'),
    path('resume-page/', resume_page, name='resume_page'),
    path('email-resume/', email_resume, name='email_resume'),
    path('register/', register, name='register'),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
    path('registration-success/', lambda request: __import__('django.shortcuts').shortcuts.render(request, 'registration_success.html'), name='registration_success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('verify-login-code/', verify_login_code, name='verify_login_code'),
    path('resend-verification/', resend_verification, name='resend_verification'),
    path('logout/',
        __import__('django.contrib.auth.views').contrib.auth.views.LogoutView.as_view(next_page='home'),
        name='logout'),
    
    # Password Reset URLs
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'),
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'),
    path('success/', success_view, name='success'),
    path('certificate/', certificate, name='certificate'),
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('blog/', blog_list, name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/<uuid:token>/', unsubscribe, name='unsubscribe'),
    path('send-announcement/', send_announcement, name='send_announcement'),
]





