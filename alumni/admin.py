from django.contrib import admin
from .models import AlumniProfile


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "company",
        "designation",
        "graduation_year",
    )

    search_fields = (
        "user__username",
        "company",
        "designation",
    )