from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create the first Smart Alumni administrator if no admin exists."

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(role="ADMIN").exists():
            self.stdout.write(self.style.WARNING("An admin account already exists; no new account was created."))
            return
        username = input("Admin username: ").strip()
        email = input("Admin email: ").strip()
        password = input("Admin password: ")
        if not username or not password:
            self.stderr.write("Username and password are required.")
            return
        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.role = "ADMIN"
        user.save(update_fields=["role"])
        self.stdout.write(self.style.SUCCESS(f"Initial admin '{username}' created."))
