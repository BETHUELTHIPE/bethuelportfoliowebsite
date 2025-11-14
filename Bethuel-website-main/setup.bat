@echo off
echo 🚀 Setting up Bethuel Portfolio Website...

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo 🗄️ Running migrations...
python manage.py makemigrations
python manage.py migrate

echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo 👤 Setting up admin user...
python manage.py setup_project

echo ✅ Setup complete!
echo.
echo 📋 Next steps:
echo 1. Update .env file with your email credentials
echo 2. Run: python manage.py runserver
echo 3. Visit: http://127.0.0.1:8000
echo.
pause