from django.db import models
from django.conf import settings


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    department = models.CharField(max_length=100)

    year = models.PositiveIntegerField()

    register_number = models.CharField(
        max_length=50,
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(blank=True)

    skills = models.TextField(blank=True)

    profile_picture = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    resume = models.FileField(
        upload_to="student_resumes/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username