from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import User
from jobs.models import Job, JobApplication
from mentorship.models import MentorshipRequest
from notifications.models import Notification
from accounts.forms import AdminUserCreateForm


@login_required
def dashboard(request):
    user = request.user
    role = str(getattr(user, "role", "")).upper()

    context = {
        "alumni_count": User.objects.filter(role="ALUMNI").count(),
        "student_count": User.objects.filter(role="STUDENT").count(),
        "job_count": Job.objects.count(),
        "admin_count": User.objects.filter(role="ADMIN").count(),
        "unread_count": Notification.objects.filter(
            user=user, is_read=False
        ).count(),
        "role": role,
        "recent_jobs": Job.objects.select_related("posted_by")[:5],
    }

    if role == "STUDENT":
        context["my_applications_count"] = JobApplication.objects.filter(
            student=user
        ).count()
        context["my_mentorship_count"] = MentorshipRequest.objects.filter(
            student=user
        ).count()
    elif role == "ALUMNI":
        context["my_jobs_count"] = Job.objects.filter(posted_by=user).count()
        context["pending_applications_count"] = JobApplication.objects.filter(
            job__posted_by=user, status="APPLIED"
        ).count()
        context["mentorship_requests_count"] = MentorshipRequest.objects.filter(
            alumni=user, status="Pending"
        ).count()

    return render(request, "dashboard/dashboard.html", context)



def _is_admin(user):
    return user.is_authenticated and (
        getattr(user, "is_superuser", False)
        or str(getattr(user, "role", "")).upper() == "ADMIN"
    )


@login_required
def admin_dashboard(request):
    """Admin dashboard. Only admins can access admin user-management actions."""
    if not _is_admin(request.user):
        messages.error(request, "Admin access is required.")
        return redirect("home")

    context = {
        "total_users": User.objects.count(),
        "total_alumni": User.objects.filter(role="ALUMNI").count(),
        "total_students": User.objects.filter(role="STUDENT").count(),
        "total_admins": User.objects.filter(role="ADMIN").count(),
        "total_jobs": Job.objects.count(),
        "total_mentorships": MentorshipRequest.objects.count(),
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@login_required
def admin_add_user(request):
    """Admin-only account creation. This is the only UI path that can create admins."""
    if not _is_admin(request.user):
        messages.error(request, "Only an admin can add users.")
        return redirect("home")

    if request.method == "POST":
        form = AdminUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"{user.get_role_display()} account '{user.username}' created successfully."
            )
            return redirect("admin_dashboard")
    else:
        requested_role = str(request.GET.get("role", "STUDENT")).upper()
        if requested_role not in {"STUDENT", "ALUMNI", "ADMIN"}:
            requested_role = "STUDENT"
        form = AdminUserCreateForm(initial={"role": requested_role})

    return render(
        request,
        "dashboard/admin_user_form.html",
        {"form": form, "title": "Add Student / Alumni / Admin"},
    )
