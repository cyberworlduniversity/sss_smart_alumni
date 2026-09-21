from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("ALUMNI", "Alumni"),
        ("STUDENT", "Student"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="STUDENT",
    )

    phone = models.CharField(max_length=15, blank=True)

    profile_picture = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
    )

    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    company = models.CharField(
        max_length=100,
        blank=True,
    )

    designation = models.CharField(
        max_length=100,
        blank=True,
    )

    current_job = models.CharField(
        max_length=150,
        blank=True,
        help_text="Current job or profession",
    )

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return self.username