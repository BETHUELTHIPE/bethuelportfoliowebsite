# 🚀 Bethuel Portfolio - Deployment Ready

Your Django portfolio website is now configured for deployment with working registration, login, and email verification.

## 🔧 Quick Setup

### Windows:
```bash
# 1. Activate virtual environment
env\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup script
setup.bat
```

### Linux/Mac:
```bash
# 1. Activate virtual environment
source env/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run setup script
chmod +x setup.sh
./setup.sh
```

## 📧 Email Configuration

Update `.env` file with your email settings:

```env
# Gmail Example
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in `EMAIL_HOST_PASSWORD`

## 🔐 Authentication Features

✅ **User Registration** - `/register/`
- Custom form with additional fields (cell number, address)
- Email verification required
- Account inactive until verified

✅ **Email Verification** - `/verify-email/<token>/`
- Automatic email sending
- Secure UUID tokens
- Account activation on verification

✅ **Login System** - `/login/`
- Custom login view
- Verification status checking
- Redirect to resend verification if needed

✅ **Password Reset** - Built-in Django functionality
✅ **Logout** - `/logout/`

## 🌐 Deployment Options

### 1. Local Development
```bash
py manage.py runserver
```

### 2. Docker
```bash
docker build -t bethuel-portfolio .
docker run -p 8000:8000 bethuel-portfolio
```

### 3. Production
- Update `DJANGO_DEBUG=False` in `.env`
- Set proper `DJANGO_ALLOWED_HOSTS`
- Use production database (PostgreSQL)
- Configure proper email settings

## 🔑 Default Admin Access
- Username: `admin`
- Password: `admin123`
- Access: `/admin/`

## 📁 Project Structure
```
portfolio/
├── portfolio/          # Django project settings
├── resume/            # Main application
│   ├── models.py      # User profiles, contacts, email verification
│   ├── views.py       # Authentication views
│   ├── forms.py       # Contact and registration forms
│   └── templates/     # HTML templates
├── static/           # Static files (CSS, images)
├── .env             # Environment variables
└── requirements.txt # Dependencies
```

## 🛠️ Key Features Implemented

1. **Custom User Registration**
   - Extended user model with profile
   - Email verification workflow
   - Inactive users until verified

2. **Email System**
   - SMTP configuration
   - Console backend for development
   - Production-ready email sending

3. **Security**
   - CSRF protection
   - Secure password validation
   - Session management

4. **Database**
   - SQLite for development
   - PostgreSQL support for production
   - Proper migrations

## 🚨 Important Notes

- Change default admin password in production
- Update secret key for production
- Configure proper email credentials
- Set DEBUG=False for production
- Use HTTPS in production

Your portfolio is now ready for deployment with full authentication functionality!