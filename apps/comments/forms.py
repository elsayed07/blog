from __future__ import annotations

from django import forms


class CommentForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Share your thoughts..."}),
        max_length=2000,
        label="Comment",
    )
    guest_name = forms.CharField(max_length=100, required=False, label="Name")
    guest_email = forms.EmailField(required=False, label="Email")
    parent_id = forms.UUIDField(required=False, widget=forms.HiddenInput)

    def clean(self) -> dict:
        cleaned = super().clean()
        return cleaned
