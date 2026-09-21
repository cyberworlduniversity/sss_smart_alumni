from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "department",
        "year",
        "register_number",
    )

    list_filter = (
        "department",
        "year",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "register_number",
    )

    ordering = (
        "user__username",
    )