from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create default admin user if not exists"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "adminterminal"
        password = "adminterminal"
        email = "admin@example.com"

        if User.objects.filter(username=username).exists():
            self.stdout.write("Admin user already exists.")
            return

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write("Admin user created successfully.")
