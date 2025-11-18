# ---- Builder Stage ----
# This stage installs python dependencies into a virtual environment.
FROM python:3.10-slim as builder

# Set environment variables to prevent writing .pyc files and to run python in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and activate a virtual environment
WORKDIR /opt/venv
RUN python -m venv .
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies into the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
# This stage copies the installed dependencies and application code.
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Create a non-root user and group for security
RUN addgroup --system app && adduser --system --ingroup app app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the path to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application source code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create mediafiles directory and change ownership
RUN mkdir -p /app/mediafiles && \
    chown -R app:app /app/staticfiles && \
    chown -R app:app /app/mediafiles && \
    chown -R app:app .

# Switch to the non-root user
USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "portfolio.wsgi:application"]