from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            "resume",
            "cover_letter",
        ]

        widgets = {
            "resume": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.doc,.docx",
                }
            ),

            "cover_letter": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your cover letter...",
                }
            ),
        }

        labels = {
            "resume": "Resume",
            "cover_letter": "Cover Letter",
        }