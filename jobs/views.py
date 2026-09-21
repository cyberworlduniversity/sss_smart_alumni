from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef, Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import alumni_required, student_required
from notifications.models import Notification

from .forms import JobApplicationForm
from .models import Job, JobApplication


@login_required
def job_list(request):
    jobs = Job.objects.select_related("posted_by").all()
    search = request.GET.get("search", "").strip()
    location = request.GET.get("location", "").strip()

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search)
            | Q(company__icontains=search)
            | Q(description__icontains=search)
            | Q(posted_by__first_name__icontains=search)
            | Q(posted_by__last_name__icontains=search)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)

    if request.user.role == "STUDENT":
        jobs = jobs.annotate(
            already_applied=Exists(
                JobApplication.objects.filter(
                    job=OuterRef("pk"),
                    student=request.user,
                )
            )
        )

    return render(request, "jobs/job_list.html", {
        "jobs": jobs,
        "search": search,
        "location": location,
    })


@alumni_required
def create_job(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        company = request.POST.get("company", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()

        if not title or not company or not description:
            messages.error(request, "Title, company and description are required.")
            return render(request, "jobs/create_job.html")

        Job.objects.create(
            title=title,
            company=company,
            location=location,
            description=description,
            posted_by=request.user,
        )
        messages.success(request, "Job posted successfully.")
        return redirect("jobs:job_list")

    return render(request, "jobs/create_job.html")


@alumni_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    # Alumni may delete only vacancies they posted.
    if job.posted_by != request.user:
        messages.error(request, "You can delete only your own job vacancies.")
        return redirect("jobs:job_list")

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("jobs:job_list")

    title = job.title
    job.delete()
    messages.success(request, f"Job vacancy '{title}' deleted successfully.")
    return redirect("jobs:job_list")


@student_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if JobApplication.objects.filter(job=job, student=request.user).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect("jobs:job_list")

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.status = "APPLIED"
            application.save()

            student_name = request.user.get_full_name() or request.user.username
            Notification.objects.create(
                user=job.posted_by,
                title="New Job Application",
                message=f"{student_name} has applied for your job '{job.title}'.",
            )
            messages.success(request, "Your application has been submitted successfully.")
            return redirect("jobs:job_list")
    else:
        form = JobApplicationForm()

    return render(request, "jobs/apply_job.html", {"job": job, "form": form})


def _applications_for_user(request):
    role = str(getattr(request.user, "role", "")).upper()
    qs = JobApplication.objects.select_related("job", "student", "job__posted_by")
    if request.user.is_staff or role == "ADMIN":
        return qs.all()
    if role == "ALUMNI":
        return qs.filter(job__posted_by=request.user)
    return None


@login_required
def application_list(request):
    applications = _applications_for_user(request)
    if applications is None:
        messages.error(request, "Students cannot view job applications.")
        return redirect("jobs:job_list")
    return render(request, "jobs/application_list.html", {"applications": applications})


def _can_manage_application(request, application):
    role = str(getattr(request.user, "role", "")).upper()
    return (
        request.user.is_staff
        or role == "ADMIN"
        or (role == "ALUMNI" and application.job.posted_by == request.user)
    )


@login_required
def view_application(request, pk):
    application = get_object_or_404(
        JobApplication.objects.select_related("job", "student", "job__posted_by"),
        pk=pk,
    )
    if not _can_manage_application(request, application):
        messages.error(request, "You do not have permission to view this application.")
        return redirect("jobs:job_list")
    return render(request, "jobs/view_application.html", {"application": application})


@login_required
def accept_application(request, pk):
    application = get_object_or_404(
        JobApplication.objects.select_related("job", "student"), pk=pk
    )
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("jobs:application_list")
    if not _can_manage_application(request, application):
        messages.error(request, "You do not have permission to accept this application.")
        return redirect("jobs:job_list")

    application.status = "SHORTLISTED"
    application.save(update_fields=["status", "updated_at"])
    Notification.objects.create(
        user=application.student,
        title="Application Accepted",
        message=f"Your application for '{application.job.title}' at '{application.job.company}' has been accepted.",
    )
    messages.success(request, "Application accepted successfully.")
    return redirect("jobs:application_list")


@login_required
def reject_application(request, pk):
    application = get_object_or_404(
        JobApplication.objects.select_related("job", "student"), pk=pk
    )
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("jobs:application_list")
    if not _can_manage_application(request, application):
        messages.error(request, "You do not have permission to reject this application.")
        return redirect("jobs:job_list")

    application.status = "REJECTED"
    application.save(update_fields=["status", "updated_at"])
    Notification.objects.create(
        user=application.student,
        title="Application Rejected",
        message=f"Your application for '{application.job.title}' at '{application.job.company}' has been rejected.",
    )
    messages.success(request, "Application rejected successfully.")
    return redirect("jobs:application_list")


@login_required
def delete_application(request, pk):
    application = get_object_or_404(
        JobApplication.objects.select_related("job"), pk=pk
    )
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("jobs:application_list")
    if not _can_manage_application(request, application):
        messages.error(request, "You do not have permission to delete this application.")
        return redirect("jobs:job_list")

    application.delete()
    messages.success(request, "Application deleted successfully.")
    return redirect("jobs:application_list")
