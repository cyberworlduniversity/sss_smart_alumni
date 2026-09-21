from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


DEPARTMENT_CHOICES = (
    ("BSC_CS", "B.Sc. Computer Science"),
    ("BSC_AI", "B.Sc. Artificial Intelligence"),
    ("BCA", "B.C.A"),
    ("BCOM", "B.Com"),
    ("BCOM_CA", "B.Com. Computer Applications"),
    ("BA_ENGLISH", "B.A. English"),
    ("BA_TAMIL", "B.A. Tamil"),
    ("BBA", "B.B.A"),
    ("BSC_MATHS", "B.Sc. Mathematics"),
    ("BSC_PHYSICS", "B.Sc. Physics"),
    ("BSC_CHEMISTRY", "B.Sc. Chemistry"),
    ("BSC_BIOLOGY", "B.Sc. Biology"),
    ("BSC_BOTANY", "B.Sc. Botany"),
    ("BSC_ZOOLOGY", "B.Sc. Zoology"),
    ("OTHER", "Other"),
)


class RegistrationFieldsMixin:
    """Common required fields and Alumni-only validation for account creation."""

    first_name = forms.CharField(
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    last_name = forms.CharField(
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    username = forms.CharField(
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "required": True}),
    )
    phone = forms.CharField(
        required=True,
        label="Phone",
        widget=forms.TextInput(attrs={"class": "form-control", "required": True}),
    )
    graduation_year = forms.IntegerField(
        required=False,
        label="Graduation Year",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "e.g. 2026", "min": "1900", "max": "2100"}
        ),
    )
    current_job = forms.CharField(
        required=False,
        label="Current Job",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g. Software Developer"}
        ),
    )
    password1 = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": True}),
    )
    password2 = forms.CharField(
        required=True,
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control", "required": True}),
    )

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if role == "ALUMNI":
            if not cleaned.get("graduation_year"):
                self.add_error("graduation_year", "Graduation year is required for Alumni.")
            if not cleaned.get("current_job"):
                self.add_error("current_job", "Current job is required for Alumni.")
        else:
            # These fields are Alumni-only and must not be stored for other roles.
            cleaned["graduation_year"] = None
            cleaned["current_job"] = ""
        if not cleaned.get("phone"):
            self.add_error("phone", "Phone number is required.")
        return cleaned


class RegisterForm(RegistrationFieldsMixin, UserCreationForm):
    """Public registration: Student or Alumni only. Admin is never public."""

    PUBLIC_ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("ALUMNI", "Alumni"),
    )

    role = forms.ChoiceField(
        choices=PUBLIC_ROLE_CHOICES,
        initial="STUDENT",
        required=True,
        label="Role",
        widget=forms.Select(attrs={"class": "form-select", "required": True}),
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-select", "required": True}),
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "role", "department",
            "phone", "graduation_year", "current_job", "password1", "password2",
            "profile_picture", "bio", "skills", "linkedin", "github", "portfolio",
        )
        widgets = {
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "phone", "graduation_year", "current_job",
            "profile_picture", "bio", "skills", "linkedin", "github", "portfolio",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "graduation_year": forms.NumberInput(attrs={"class": "form-control", "min": "1900", "max": "2100"}),
            "current_job": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Software Developer"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }


class AdminUserCreateForm(RegistrationFieldsMixin, UserCreationForm):
    """Admin-only account creation for Student, Alumni, or Admin."""

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-select", "required": True}),
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        label="Role",
        widget=forms.Select(attrs={"class": "form-select", "required": True}),
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "role", "department",
            "phone", "graduation_year", "current_job", "password1", "password2",
            "profile_picture", "bio", "skills", "linkedin", "github", "portfolio",
        )
        widgets = {
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "skills": forms.TextInput(attrs={"class": "form-control"}),
            "linkedin": forms.URLInput(attrs={"class": "form-control"}),
            "github": forms.URLInput(attrs={"class": "form-control"}),
            "portfolio": forms.URLInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role == "ADMIN":
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        if commit:
            user.save()
        return user
