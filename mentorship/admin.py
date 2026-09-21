from django.contrib import admin
from .models import MentorshipRequest


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "alumni",
        "status",
        "requested_at",
    )

    list_filter = ("status",)

    search_fields = (
        "student__username",
        "alumni__username",
    )