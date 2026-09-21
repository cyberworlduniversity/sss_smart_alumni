from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from .models import MentorshipRequest


@login_required
def mentorship_list(request):

    # =========================
    # STUDENT
    # =========================
    if request.user.role == "STUDENT":

        # All alumni who can be mentors
        alumni = User.objects.filter(
            role="ALUMNI"
        ).order_by("username")

        # Student's existing requests
        my_requests = MentorshipRequest.objects.filter(
            student=request.user
        ).select_related("alumni").order_by("-requested_at")

        return render(
            request,
            "mentorship/list.html",
            {
                "alumni": alumni,
                "my_requests": my_requests,
            },
        )

    # =========================
    # ALUMNI
    # =========================
    elif request.user.role == "ALUMNI":

        mentorships = MentorshipRequest.objects.filter(
            alumni=request.user
        ).select_related("student").order_by("-requested_at")

        return render(
            request,
            "mentorship/list.html",
            {
                "mentorships": mentorships,
            },
        )

    # =========================
    # ADMIN / OTHER
    # =========================
    mentorships = MentorshipRequest.objects.all().select_related(
        "student",
        "alumni",
    ).order_by("-requested_at")

    return render(
        request,
        "mentorship/list.html",
        {
            "mentorships": mentorships,
        },
    )


@login_required
def request_mentorship(request, alumni_id):

    # Only students can request mentorship
    if request.user.role != "STUDENT":
        messages.error(
            request,
            "Only students can request mentorship."
        )
        return redirect("mentorship_list")

    alumni = get_object_or_404(
        User,
        id=alumni_id,
        role="ALUMNI",
    )

    # Check whether student already has a request
    existing = MentorshipRequest.objects.filter(
        student=request.user,
        alumni=alumni,
    ).first()

    if existing:
        messages.warning(
            request,
            "You have already requested mentorship from this alumni."
        )
        return redirect("mentorship_list")

    if request.method == "POST":

        message_text = request.POST.get(
            "message",
            ""
        ).strip()

        if not message_text:
            messages.error(
                request,
                "Please enter a message."
            )
            return render(
                request,
                "mentorship/request.html",
                {
                    "alumni": alumni,
                },
            )

        MentorshipRequest.objects.create(
            student=request.user,
            alumni=alumni,
            message=message_text,
            status="Pending",
        )

        messages.success(
            request,
            "Mentorship request sent successfully."
        )

        return redirect("mentorship_list")

    return render(
        request,
        "mentorship/request.html",
        {
            "alumni": alumni,
        },
    )


@login_required
def accept_mentorship(request, pk):

    mentorship = get_object_or_404(
        MentorshipRequest,
        pk=pk,
        alumni=request.user,
    )

    mentorship.status = "Accepted"
    mentorship.save()

    messages.success(
        request,
        "Mentorship request accepted."
    )

    return redirect("mentorship_list")


@login_required
def reject_mentorship(request, pk):

    mentorship = get_object_or_404(
        MentorshipRequest,
        pk=pk,
        alumni=request.user,
    )

    mentorship.status = "Rejected"
    mentorship.save()

    messages.success(
        request,
        "Mentorship request rejected."
    )

    return redirect("mentorship_list")

def index(request):
    return render(request, "mentorship/index.html")