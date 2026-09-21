from django.contrib import admin

from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "company",
        "location",
        "posted_by",
        "created_at",
    )

    search_fields = (
        "title",
        "company",
        "location",
    )

    list_filter = (
        "created_at",
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        "job",
        "student",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "job__title",
        "job__company",
        "student__username",
    )

    list_select_related = (
        "job",
        "student",
    )