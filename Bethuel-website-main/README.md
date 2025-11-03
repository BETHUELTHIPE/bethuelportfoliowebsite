
# Bethuel Portfolio Website

A professional Django-based portfolio website for Bethuel, featuring a modern design, animated header/footer, and responsive layout.

---

## 🚀 Local Development Setup (Windows PowerShell)

1. **Clone the repository and enter the project directory:**
	```powershell
	cd 'C:\Users\Bethuel\Downloads\Bethuel-website-main\Bethuel-website-main'
	```

2. **Create and activate a virtual environment:**
	```powershell
	python -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```

3. **Install dependencies:**
	```powershell
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	```

4. **Apply migrations and create a superuser:**
	```powershell
	python manage.py migrate
	python manage.py createsuperuser
	```

5. **Collect static files:**
	```powershell
	python manage.py collectstatic --noinput
	```

6. **Run the development server:**
	```powershell
	python manage.py runserver
	```
	Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🐳 Docker Setup

1. **Build and start all services:**
	```powershell
	docker compose up --build
	```
	- The app will be available at [http://localhost:8000](http://localhost:8000)
	- pgAdmin at [http://localhost:5050](http://localhost:5050) (login: admin@admin.com / admin)

2. **Stop services:**
	```powershell
	docker compose down
	```

---

## 🧪 Tests & Quality Checks

- **Run Django tests:**
  ```powershell
  python manage.py test
  ```
- **Check for issues:**
  ```powershell
  python manage.py check
  ```
- **Lint code (PEP8):**
  ```powershell
  python -m pycodestyle . --exclude=env,.venv,env/*,venv/*,*/site-packages/*,*/migrations/*
  ```

---

## ⚙️ Configuration & Environment
- Python version: 3.11.x (see `runtime.txt`)
- Environment variables for production (see `portfolio/settings.py`):
  - `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, etc.
- For local dev, SQLite is used by default if Postgres is not running.

---

## ✨ Features
- Modern, animated header and footer
- Responsive, mobile-friendly design
- Professional color palette and typography
- Social/contact links in the footer

---

## 📄 License
Copyright © 2024 Bethuel. All rights reserved.
