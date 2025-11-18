# Bethuel Portfolio Website - Setup Instructions

## Quick Start Guide

### Step 1: Activate Virtual Environment
Open Command Prompt and navigate to the project directory, then activate the virtual environment:

```bash
cd c:\Users\Bethuel\Downloads\Bethuel-website-main\Bethuel-website-main
env\Scripts\activate
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 4: Start Development Server
```bash
python manage.py runserver
```

### Step 5: Access the Website
Open your browser and go to:
- **Home**: http://127.0.0.1:8000/
- **About**: http://127.0.0.1:8000/about/
- **Projects**: http://127.0.0.1:8000/projects/
- **Experience**: http://127.0.0.1:8000/experience/
- **Contact**: http://127.0.0.1:8000/contact/
- **Resume**: http://127.0.0.1:8000/resume/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'celery'"
**Solution**: The Celery import has been made optional for development. The app will work without Redis/Celery.

### Issue: "ModuleNotFoundError: No module named 'django_redis'"
**Solution**: Django-redis is optional. The app uses local memory cache in development mode.

### Issue: Python not found
**Solution**: Make sure you're using the virtual environment. Run `env\Scripts\activate` first.

## Project Structure

```
Bethuel-website-main/
├── portfolio/          # Django project settings
├── resume/             # Main Django app
├── static/             # CSS, JS, images
├── templates/          # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Features Available

✅ Home page with portfolio overview
✅ About section
✅ Projects showcase
✅ Experience timeline
✅ Contact form
✅ Resume download
✅ User registration and login
✅ Email verification
✅ Admin dashboard
✅ Blog functionality
✅ Newsletter subscription

## Environment Variables

The `.env` file contains:
- `DJANGO_DEBUG=True` - Development mode
- `DJANGO_ALLOWED_HOSTS` - Allowed domains
- `EMAIL_HOST_USER` - Email for contact form
- `POSTGRES_DB` - Database name (optional for production)

## Next Steps

1. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin panel at http://127.0.0.1:8000/admin/

3. Customize content through the admin panel or by editing templates in the `templates/` directory

4. For production deployment, see `DEPLOY_MANUAL.md`
