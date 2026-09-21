from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update the SSS College administrator account."

    def handle(self, *args, **options):
        User = get_user_model()
        username = "SSSCOLLEGE"
        password = "SSS@555"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": "SSS",
                "last_name": "COLLEGE",
                "role": "ADMIN",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.set_password(password)
        user.role = "ADMIN"
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"SSS College administrator '{username}' {action} successfully."
            )
        )
