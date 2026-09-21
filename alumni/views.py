from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from accounts.forms import DEPARTMENT_CHOICES
from accounts.models import User


@login_required
def alumni_list(request):
    """Responsive alumni directory with search and filters."""
    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "").strip()
    graduation_year = request.GET.get("graduation_year", "").strip()
    industry = request.GET.get("industry", "").strip()

    alumni_qs = User.objects.filter(role="ALUMNI", is_active=True).order_by(
        "first_name", "last_name", "username"
    )

    if search:
        alumni_qs = alumni_qs.filter(
            Q(first_name__icontains=search)
            | Q(last_name__icontains=search)
            | Q(username__icontains=search)
            | Q(email__icontains=search)
            | Q(department__icontains=search)
            | Q(company__icontains=search)
            | Q(designation__icontains=search)
            | Q(current_job__icontains=search)
            | Q(skills__icontains=search)
            | Q(bio__icontains=search)
        )

    if department:
        alumni_qs = alumni_qs.filter(department=department)

    if graduation_year:
        try:
            alumni_qs = alumni_qs.filter(graduation_year=int(graduation_year))
        except ValueError:
            pass

    if industry:
        alumni_qs = alumni_qs.filter(
            Q(current_job__icontains=industry)
            | Q(company__icontains=industry)
            | Q(designation__icontains=industry)
            | Q(skills__icontains=industry)
        )

    years = (
        User.objects.filter(role="ALUMNI", is_active=True, graduation_year__isnull=False)
        .values_list("graduation_year", flat=True)
        .distinct()
        .order_by("-graduation_year")
    )

    department_options = list(DEPARTMENT_CHOICES)

    paginator = Paginator(alumni_qs, 6)
    page_obj = paginator.get_page(request.GET.get("page", 1))

    return render(request, "alumni/alumni_list.html", {
        "alumni": page_obj.object_list,
        "page_obj": page_obj,
        "search": search,
        "total_count": alumni_qs.count(),
        "department_options": department_options,
        "years": years,
        "selected_department": department,
        "selected_year": graduation_year,
        "industry": industry,
    })


@login_required
def alumni_detail(request, pk):
    alumni = get_object_or_404(User, pk=pk, role="ALUMNI", is_active=True)
    return render(request, "alumni/alumni_detail.html", {"alumni": alumni})
