from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Setup project with initial data'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create superuser if it doesn't exist
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@bethuelportfolio.com',
                    password='admin123',
                    is_active=True
                )
                self.stdout.write(
                    self.style.SUCCESS('Superuser created: admin/admin123')
                )
            else:
                self.stdout.write('Superuser already exists')
        
        self.stdout.write(
            self.style.SUCCESS('Project setup completed successfully!')
        )