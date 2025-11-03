
# Base Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Copy wait-for-db script
COPY wait_for_db.py .

# Expose port
EXPOSE 8000

# Command: wait for DB, apply migrations, start Gunicorn
CMD ["sh", "-c", "python wait_for_db.py && python manage.py migrate && gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000"]
