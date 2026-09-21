from django.contrib.auth.decorators import user_passes_test


def alumni_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == "ALUMNI"
    )(view_func)


def student_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == "STUDENT"
    )(view_func)


def admin_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and (
            u.role == "ADMIN" or u.is_superuser
        )
    )(view_func)