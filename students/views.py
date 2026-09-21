from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from accounts.models import User


@login_required
def student_list(request):
    """Dynamic student directory based on registered User accounts."""
    search = request.GET.get("search", "").strip()
    students = User.objects.filter(role="STUDENT", is_active=True).order_by(
        "first_name", "last_name", "username"
    )

    if search:
        students = students.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(department__icontains=search)
            | Q(skills__icontains=search)
            | Q(bio__icontains=search)
        )

    return render(request, "students/list.html", {
        "students": students,
        "search": search,
        "total_count": students.count(),
    })
