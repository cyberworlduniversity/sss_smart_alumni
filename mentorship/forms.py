from django import forms
from .models import MentorshipRequest


class MentorshipRequestForm(forms.ModelForm):

    class Meta:
        model = MentorshipRequest
        fields = [
            "alumni",
            "message",
        ]

        widgets = {
            "alumni": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write your mentorship request...",
                }
            ),
        }