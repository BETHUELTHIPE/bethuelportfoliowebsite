#!/bin/bash

echo "🔧 Fixing Bethuel Portfolio on EC2..."

# Create templates directory
mkdir -p templates

# Create base template
cat > templates/base.html << 'EOF'
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Bethuel Portfolio{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Bethuel Portfolio</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'home' %}">Home</a>
                <a class="nav-link" href="{% url 'projects' %}">Projects</a>
                <a class="nav-link" href="{% url 'contact' %}">Contact</a>
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'resume' %}">Resume</a>
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Login</a>
                    <a class="nav-link" href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>
    {% if messages %}
        <div class="container mt-5 pt-4">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">{{ message|safe }}</div>
            {% endfor %}
        </div>
    {% endif %}
    <main class="mt-5 pt-4">{% block content %}{% endblock %}</main>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
EOF

# Create login template
cat > templates/login.html << 'EOF'
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header"><h3>Login</h3></div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        {{ form.as_p }}
                        <button type="submit" class="btn btn-primary">Login</button>
                    </form>
                    <p class="mt-3">Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Create register template
cat > templates/register.html << 'EOF'
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header"><h3>Register</h3></div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        {{ form.as_p }}
                        <button type="submit" class="btn btn-success">Register</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Create registration success template
cat > templates/registration_success.html << 'EOF'
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-success text-white text-center">
                    <h3>Registration Successful!</h3>
                </div>
                <div class="card-body text-center">
                    <h4 class="text-success mb-4">Welcome to Bethuel Portfolio!</h4>
                    <div class="alert alert-info">
                        <strong>Check Your Email</strong><br>
                        We've sent you a verification email. Please click the link to activate your account.
                    </div>
                    <div class="mt-4">
                        <a href="{% url 'login' %}" class="btn btn-primary me-3">Go to Login</a>
                        <a href="{% url 'resend_verification' %}" class="btn btn-outline-secondary">Resend Email</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Create email verified template
cat > templates/email_verified.html << 'EOF'
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header bg-success text-white text-center">
                    <h3>Email Verified Successfully!</h3>
                </div>
                <div class="card-body text-center">
                    <h4 class="text-success mb-4">Welcome, {{ user.first_name }}!</h4>
                    <div class="alert alert-success">
                        <strong>Account Activated</strong><br>
                        Your email has been verified and your account is now active.
                    </div>
                    <div class="mt-4">
                        <a href="{% url 'login' %}" class="btn btn-primary btn-lg me-3">Login Now</a>
                        <a href="{% url 'home' %}" class="btn btn-outline-primary btn-lg">Go Home</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Create resend verification template
cat > templates/resend_verification.html << 'EOF'
{% extends 'base.html' %}
{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-warning text-dark">
                    <h3>Resend Verification Email</h3>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        <div class="form-group mb-3">
                            <label for="email" class="form-label">Email Address</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        <button type="submit" class="btn btn-warning w-100">Resend Verification Email</button>
                    </form>
                    <div class="text-center mt-3">
                        <p><a href="{% url 'login' %}">Back to Login</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF

# Update email settings
echo "
# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bethuelmoukangwe8@gmail.com'
EMAIL_HOST_PASSWORD = 'drlk qyno yvep mjkj'
DEFAULT_FROM_EMAIL = 'bethuelmoukangwe8@gmail.com'
ADMIN_EMAIL = 'bethuelmoukangwe8@gmail.com'" >> portfolio/settings.py

# Create static directories and basic CSS
mkdir -p static/css static/js

cat > static/css/style.css << 'EOF'
.card {
    transition: transform 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.2);
}

.btn {
    transition: all 0.3s ease;
}

.btn:hover {
    transform: translateY(-2px);
}

.navbar-brand {
    font-weight: bold;
}

.alert {
    border-radius: 10px;
}
EOF

# Restart containers
echo "🔄 Restarting containers..."
docker-compose down
docker-compose up -d --build

echo "✅ Fix completed!"
echo "🌐 Your website is now available at: http://34.252.250.140:8090"
echo "📧 Email functionality is configured with Gmail"
echo "🔐 Login/Registration system is ready"