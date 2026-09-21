from django.db import models
from django.conf import settings


class AlumniProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alumni_profile"
    )

    graduation_year = models.PositiveIntegerField()

    department = models.CharField(max_length=100)

    company = models.CharField(
        max_length=150,
        blank=True
    )

    designation = models.CharField(
        max_length=150,
        blank=True
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    bio = models.TextField(blank=True)

    skills = models.TextField(blank=True)

    linkedin = models.URLField(blank=True)

    github = models.URLField(blank=True)

    portfolio = models.URLField(blank=True)

    profile_picture = models.ImageField(
        upload_to="alumni/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username